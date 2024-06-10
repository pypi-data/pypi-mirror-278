"""
Testing for conversion module
"""
import pytest
from server_metrics.utils.conversion import (
    convert_frequency_to_number,
    convert_lanes_to_number,
    convert_memory_to_number,
    convert_percentage_to_number,
    convert_power_to_number,
    convert_temperature_to_number,
    convert_voltage_to_number
)

def test_convert_frequency_to_number():
    """
    Tests converting MHz to number
    """
    assert convert_frequency_to_number("300 MHz") == 300
    assert convert_frequency_to_number("  5000   MHz  ") == 5000
    with pytest.raises(ValueError):
        convert_frequency_to_number("invalid")

def test_convert_lanes_to_number():
    """
    Tests converting 16x to number
    """
    assert convert_lanes_to_number("16x") == 16
    assert convert_lanes_to_number("  8   x  ") == 8
    with pytest.raises(ValueError):
        convert_lanes_to_number("invalid")

def test_convert_memory_to_number():
    """
    Tests converting MiB to number
    """
    assert convert_memory_to_number("24576 MiB") == 24576
    assert convert_memory_to_number("  1024   MiB  ") == 1024
    with pytest.raises(ValueError):
        convert_memory_to_number("invalid")

def test_convert_percentage_to_number():
    """
    Tests converting percentage to number
    """
    assert convert_percentage_to_number("0 %") == 0
    assert convert_percentage_to_number("  75   %  ") == 75
    with pytest.raises(ValueError):
        convert_percentage_to_number("invalid")

def test_convert_power_to_number():
    """
    Tests converting W (watts) to number
    """
    assert convert_power_to_number("42.65 W") == 42.65
    assert convert_power_to_number("  100.5   W  ") == 100.5
    with pytest.raises(ValueError):
        convert_power_to_number("invalid")

def test_convert_temperature_to_number():
    """
    Tests converting C (celcius) to number
    """
    assert convert_temperature_to_number("41 C") == 41
    assert convert_temperature_to_number("  100   C  ") == 100
    with pytest.raises(ValueError):
        convert_temperature_to_number("invalid")

def test_convert_voltage_to_number():
    """
    Tests converting mV (voltage) to number
    """
    assert convert_voltage_to_number("737.500 mV") == 737.5
    assert convert_voltage_to_number("  1000.0   mV  ") == 1000.0
    with pytest.raises(ValueError):
        convert_voltage_to_number("invalid")
