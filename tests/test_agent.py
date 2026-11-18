"""Offline unit tests for the Python agent; no MQTT broker required."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

AGENT = Path(__file__).resolve().parents[1] / "agent" / "agent.py"
spec = importlib.util.spec_from_file_location("pcmon_agent", AGENT)
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


class DeviceIdentityTests(unittest.TestCase):
    def test_id_persists_across_runs(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(Path, "home", return_value=Path(temp)):
            first = agent.persistent_device_id()
            second = agent.persistent_device_id()
            self.assertEqual(first, second)
            self.assertRegex(first, r"^PC-[0-9a-f]{12}$")

    def test_cli_device_override(self):
        with patch.object(sys, "argv", ["agent.py", "--room", "lab_room01", "--device", "PC01"]):
            args = agent.parse_args()
            self.assertEqual(args.device, "PC01")

    def test_invalid_room_rejected(self):
        with patch.object(sys, "argv", ["agent.py", "--room", "bad!"]):
            with self.assertRaises(SystemExit):
                agent.parse_args()

    def test_invalid_interval_rejected(self):
        with patch.object(sys, "argv", ["agent.py", "--room", "lab_room01", "--interval", "nan"]):
            with self.assertRaises(SystemExit):
                agent.parse_args()


if __name__ == "__main__":
    unittest.main()
