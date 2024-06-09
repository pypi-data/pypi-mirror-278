"""Vehicle class tests."""

import sys
from datetime import datetime, timezone, timedelta

import pytest

from volkswagencarnet.vw_const import VehicleStatusParameter as P
from volkswagencarnet.vw_utilities import json_loads
from .fixtures.constants import status_report_json_file, MOCK_VIN

if sys.version_info >= (3, 8):
    # This won't work on python versions less than 3.8
    from unittest import IsolatedAsyncioTestCase
else:
    from unittest import TestCase

    class IsolatedAsyncioTestCase(TestCase):
        """Python 3.7 compatibility dummy class."""

        pass


from unittest.mock import MagicMock, patch

from aiohttp import ClientSession
from freezegun import freeze_time

from volkswagencarnet.vw_vehicle import (
    Vehicle,
    ENGINE_TYPE_ELECTRIC,
    ENGINE_TYPE_DIESEL,
    ENGINE_TYPE_GASOLINE,
)


class VehicleTest(IsolatedAsyncioTestCase):
    """Test Vehicle methods."""

    @freeze_time("2022-02-14 03:04:05")
    async def test_init(self):
        """Test __init__."""
        async with ClientSession() as conn:
            target_date = datetime.fromisoformat("2022-02-14 03:04:05")
            url = "https://foo.bar"
            vehicle = Vehicle(conn, url)
            self.assertEqual(conn, vehicle._connection)
            self.assertEqual(url, vehicle._url)
            self.assertEqual("https://msg.volkswagen.de", vehicle._homeregion)
            self.assertFalse(vehicle._discovered)
            self.assertEqual({}, vehicle._states)
            self.assertEqual(30, vehicle._climate_duration)
            self.assertDictEqual(
                {
                    "batterycharge": {"status": "", "timestamp": target_date},
                    "climatisation": {"status": "", "timestamp": target_date},
                    "departuretimer": {"status": "", "timestamp": target_date},
                    "latest": "",
                    "lock": {"status": "", "timestamp": target_date},
                    "preheater": {"status": "", "timestamp": target_date},
                    "refresh": {"status": "", "timestamp": target_date},
                    "remaining": -1,
                    "state": "",
                },
                vehicle._requests,
            )

            self.assertDictEqual(
                {
                    "carfinder_v1": {"active": False},
                    "rbatterycharge_v1": {"active": False},
                    "rclima_v1": {"active": False},
                    "rheating_v1": {"active": False},
                    "rhonk_v1": {"active": False},
                    "rlu_v1": {"active": False},
                    "statusreport_v1": {"active": False},
                    "timerprogramming_v1": {"active": False},
                    "trip_statistic_v1": {"active": False},
                },
                vehicle._services,
            )

    def test_str(self):
        """Test __str__."""
        vehicle = Vehicle(None, "XYZ1234567890")
        self.assertEqual("XYZ1234567890", vehicle.__str__())

    def test_discover(self):
        """Test the discovery process."""
        pass

    @pytest.mark.asyncio
    async def test_update_deactivated(self):
        """Test that calling update on a deactivated Vehicle does nothing."""
        vehicle = MagicMock(spec=Vehicle, name="MockDeactivatedVehicle")
        vehicle.update = lambda: Vehicle.update(vehicle)
        vehicle._discovered = True
        vehicle._deactivated = True

        await vehicle.update()

        vehicle.discover.assert_not_called()
        # Verify that no other methods were called
        self.assertEqual(0, vehicle.method_calls.__len__(), f"xpected none, got {vehicle.method_calls}")

    async def test_update(self):
        """Test that update calls the wanted methods and nothing else."""
        vehicle = MagicMock(spec=Vehicle, name="MockUpdateVehicle")
        vehicle.update = lambda: Vehicle.update(vehicle)

        vehicle._discovered = False
        vehicle.deactivated = False
        await vehicle.update()

        vehicle.discover.assert_called_once()
        vehicle.get_preheater.assert_called_once()
        vehicle.get_climater.assert_called_once()
        vehicle.get_trip_statistic.assert_called_once()
        vehicle.get_position.assert_called_once()
        vehicle.get_statusreport.assert_called_once()
        vehicle.get_charger.assert_called_once()
        vehicle.get_timerprogramming.assert_called_once()

        # Verify that only the expected functions above were called
        self.assertEqual(
            8, vehicle.method_calls.__len__(), f"Wrong number of methods called. Expected 8, got {vehicle.method_calls}"
        )


class VehiclePropertyTest(IsolatedAsyncioTestCase):
    """Tests for properties in Vehicle."""

    async def test_is_last_connected_supported(self):
        """Test that parsing last connected works."""
        vehicle = Vehicle(conn=None, url="dummy34")

        vehicle._discovered = True

        with patch.dict(vehicle.attrs, {}):
            res = vehicle.is_last_connected_supported
            self.assertFalse(res, "Last connected supported returned True without attributes.")

        with patch.dict(vehicle.attrs, {"StoredVehicleDataResponse": {}}):
            res = vehicle.is_last_connected_supported
            self.assertFalse(res, "Last connected supported returned True without 'vehicleData'.")

        with patch.dict(vehicle.attrs, {"StoredVehicleDataResponse": {"vehicleData": {}}}):
            res = vehicle.is_last_connected_supported
            self.assertFalse(res, "Last connected supported returned True without 'vehicleData.data'.")

        with patch.dict(vehicle.attrs, {"StoredVehicleDataResponse": {"vehicleData": {"data": []}}}):
            res = vehicle.is_last_connected_supported
            self.assertFalse(res, "Last connected supported returned True without 'vehicleData.data[].field[]'.")

        # test with a "real" response
        with open(status_report_json_file) as f:
            data = json_loads(f.read())
        with patch.dict(vehicle.attrs, data):
            res = vehicle.is_last_connected_supported
            self.assertTrue(res, "Last connected supported returned False when it should have been True")

    async def test_last_connected(self):
        """
        Test that parsing last connected works.

        Data in json is: "tsCarSentUtc": "2022-02-14T00:00:45Z",
        and the function returns local time
        """
        vehicle = Vehicle(conn=None, url="dummy34")

        vehicle._discovered = True

        with open(status_report_json_file) as f:
            data = json_loads(f.read())
        with patch.dict(vehicle.attrs, data):
            res = vehicle.last_connected
            self.assertEqual(
                datetime.fromisoformat("2022-02-14T00:00:45+00:00").astimezone(None).strftime("%Y-%m-%d %H:%M:%S"), res
            )

    def test_requests_remaining(self):
        """Test requests remaining logic."""
        vehicle = Vehicle(conn=None, url="")
        with patch.dict(vehicle._requests, {"remaining": 22}):
            self.assertTrue(vehicle.is_requests_remaining_supported)
            self.assertEqual(22, vehicle.requests_remaining)
        # if remaining is missing _and_ attrs has no rate limit remaining attribute
        with patch.dict(vehicle._requests, {}):
            del vehicle._requests["remaining"]
            self.assertFalse(vehicle.is_requests_remaining_supported)
            with self.assertRaises(KeyError):
                vehicle.requests_remaining()

            # and with the attribute
            with patch.dict(vehicle._states, {"rate_limit_remaining": 99}):
                self.assertEqual(99, vehicle.requests_remaining)
                # attribute should be removed once read
                self.assertNotIn("rate_limit_remaining", vehicle.attrs)

    @freeze_time("2022-02-02 02:02:02", tz_offset=0)
    def test_requests_remaining_last_updated(self):
        """Test requests remaining logic."""
        vehicle = Vehicle(conn=None, url="")
        vehicle.requests_remaining = 4
        self.assertEqual(datetime.fromisoformat("2022-02-02T02:02:02"), vehicle.requests_remaining_last_updated)

    async def test_json(self):
        """Test JSON serialization of dict containing datetime."""
        vehicle = Vehicle(conn=None, url="dummy34")

        vehicle._discovered = True
        dtstring = "2022-02-22T02:22:20+02:00"
        d = datetime.fromisoformat(dtstring)

        with patch.dict(vehicle.attrs, {"a string": "yay", "some date": d}):
            res = f"{vehicle.json}"
            self.assertEqual('{\n    "a string": "yay",\n    "some date": "2022-02-22T02:22:20+02:00"\n}', res)

    async def test_lock_not_supported(self):
        """Test that remote locking throws exception if not supported."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._discovered = True
        vehicle._services["rlu_v1"] = {"active": False}
        try:
            await vehicle.set_lock("any", "")
        except Exception as ex:
            self.assertEqual("Remote lock/unlock is not supported.", ex.__str__())

    async def test_lock_supported(self):
        """Test that invalid locking action raises exception."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._discovered = True
        vehicle._services["rlu_v1"] = {"active": True}
        try:
            self.assertFalse(await vehicle.set_lock("any", ""))
        except Exception as ex:
            self.assertEqual(ex.__str__(), "Invalid lock action: any")

        # simulate request in progress
        vehicle._requests["lock"] = {"id": "Foo", "timestamp": datetime.now() - timedelta(seconds=20)}
        self.assertFalse(await vehicle.set_lock("lock", ""))

    async def test_in_progress(self):
        """Test that _in_progress works as expected."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._requests["timed_out"] = {"id": "1", "timestamp": datetime.now() - timedelta(minutes=20)}
        vehicle._requests["in_progress"] = {"id": 2, "timestamp": datetime.now() - timedelta(seconds=20)}
        vehicle._requests["unknown"] = {"id": "Foo"}
        self.assertFalse(vehicle._in_progress("timed_out"))
        self.assertTrue(vehicle._in_progress("in_progress"))
        self.assertFalse(vehicle._in_progress("not-defined"))
        self.assertTrue(vehicle._in_progress("unknown", 2))
        self.assertFalse(vehicle._in_progress("unknown", 4))

    async def test_is_primary_engine_electric(self):
        """Test primary electric engine."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._states["StoredVehicleDataResponseParsed"] = {P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC}}
        self.assertTrue(vehicle.is_primary_drive_electric())
        self.assertFalse(vehicle.is_primary_drive_combustion())

    async def test_is_primary_engine_combustion(self):
        """Test primary ICE."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._states["StoredVehicleDataResponseParsed"] = {
            P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_DIESEL},
            P.SECONDARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC},
        }
        self.assertTrue(vehicle.is_primary_drive_combustion())
        self.assertFalse(vehicle.is_primary_drive_electric())
        self.assertFalse(vehicle.is_secondary_drive_combustion())
        self.assertTrue(vehicle.is_secondary_drive_electric())

        # No secondary engine
        vehicle._states["StoredVehicleDataResponseParsed"] = {P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_GASOLINE}}
        self.assertTrue(vehicle.is_primary_drive_combustion())
        self.assertFalse(vehicle.is_secondary_drive_electric())

    async def test_has_combustion_engine(self):
        """Test check for ICE."""
        vehicle = Vehicle(conn=None, url="dummy34")
        vehicle._states["StoredVehicleDataResponseParsed"] = {
            P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_DIESEL},
            P.SECONDARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC},
        }
        self.assertTrue(vehicle.has_combustion_engine())

        # not sure if this exists, but :shrug:
        vehicle._states["StoredVehicleDataResponseParsed"] = {
            P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC},
            P.SECONDARY_DRIVE: {"value": ENGINE_TYPE_GASOLINE},
        }
        self.assertTrue(vehicle.has_combustion_engine())

        # not sure if this exists, but :shrug:
        vehicle._states["StoredVehicleDataResponseParsed"] = {
            P.PRIMARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC},
            P.SECONDARY_DRIVE: {"value": ENGINE_TYPE_ELECTRIC},
        }
        self.assertFalse(vehicle.has_combustion_engine())
