"""
Testing for parse_hostname module
"""
import pytest
from server_metrics.utils.parse_hostname import get_hostname

def test_get_hostname_private_ip():
    """
    Test hostnames for private ip addresses
    """
    assert get_hostname("192.168.10.10", 22) == "starlyng00"
    assert get_hostname("192.168.10.15", 22) == "starlyng05"
    assert get_hostname("192.168.10.30", 22) == "starlyng20"
    assert get_hostname("192.168.10.45", 22) == "starlyng35"

def test_get_hostname_public_ip():
    """
    Test hostnames for public ip addresses
    """
    assert get_hostname("10.0.0.1", 2200) == "starlyng00"
    assert get_hostname("172.16.0.1", 2290) == "starlyng90"

def test_get_hostname_invalid_port():
    """
    Test hostnames for invalid ports on public ip addresses
    """
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2100"):
        get_hostname("10.0.0.1", 2100)
    with pytest.raises(ValueError, match="Port number must be between 2200 and 2299: port = 2400"):
        get_hostname("10.0.0.1", 2400)

def test_get_hostname_invalid_ip_base_address_range():
    """
    Test hostnames for invalid base ip address on private ip addresses
    """
    with pytest.raises(ValueError, match="IP base address must be between 10 and 255: ip_base_address = 9"):
        get_hostname("192.168.10.9", 22)  # This IP would create a ip_base_address of 9
    with pytest.raises(ValueError, match="IP base address must be between 10 and 255: ip_base_address = 256"):
        get_hostname("192.168.10.256", 22)  # This IP would create a ip_base_address of 256
