# test/test_utils.py
from src.utils import Utils

utils = Utils()

def test_is_running_in_kubernetes():
    assert utils.is_running_in_kubernetes() is False

def test_get_ip_addresses():
    ip_addresses = utils.get_ip_addresses("example.com")
    assert isinstance(ip_addresses, list)
    assert len(ip_addresses) > 0

def test_is_valid_ip():
    assert utils.is_valid_ip("127.0.0.1") is True
    assert utils.is_valid_ip("invalid_ip") is False