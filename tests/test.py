import contextlib
import io
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'agent'))
import agent


def parse(*argv):
    with patch.object(sys, 'argv', ['agent.py', *argv]):
        with contextlib.redirect_stderr(io.StringIO()):
            return agent.parse_args()


class ParseArgsTest(unittest.TestCase):
    def test_valid_args(self):
        a = parse('--room', 'ABC123', '--device', 'PC01')
        self.assertEqual(a.room, 'ABC123')
        self.assertEqual(a.device, 'PC01')
        self.assertEqual(a.interval, 3)

    def test_room_too_short(self):
        with self.assertRaises(SystemExit):
            parse('--room', 'abc', '--device', 'PC01')

    def test_room_cannot_inject_topic(self):
        for bad in ('ABC/123', 'ABC#123', 'ABC+123', 'ABC 123'):
            with self.assertRaises(SystemExit):
                parse('--room', bad, '--device', 'PC01')

    def test_device_invalid(self):
        for bad in ('PC/01', 'PC.01', ''):
            with self.assertRaises(SystemExit):
                parse('--room', 'ABC123', '--device', bad)

    def test_interval_invalid(self):
        for bad in ('0.5', 'nan', 'inf', '-1'):
            with self.assertRaises(SystemExit):
                parse('--room', 'ABC123', '--device', 'PC01', '--interval', bad)


if __name__ == '__main__':
    unittest.main()