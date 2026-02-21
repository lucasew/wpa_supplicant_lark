import os
import sys

# Add parent directory to path to import parser.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser import parse


def test_simple_config():
    config = """
network={
    ssid="test"
    psk="password"
}
ctrl_interface=/var/run/wpa_supplicant
"""
    result = parse(config)
    # If parser returns a tuple for single item (bug?), we might need to handle it or use multi-item config.
    # But let's see if 2 items return the expected dict.
    if isinstance(result, dict):
        assert result["networks"]["test"]["psk"] == "password"  # nosec
        assert result["props"]["ctrl_interface"] == "/var/run/wpa_supplicant"  # nosec
    else:
        # Fail if it's not a dict, because the parser claims to return a dict structure in start()
        raise AssertionError(
            f"Parser returned {type(result)} instead of dict: {result}"
        )  # nosec
