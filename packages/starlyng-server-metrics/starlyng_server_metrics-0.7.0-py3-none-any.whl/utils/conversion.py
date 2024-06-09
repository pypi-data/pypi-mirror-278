"""
conversion.py
"""
def convert_frequency_to_number(frequency_string: str):
    """
    Converts a frequency measurement string with a unit (e.g., "300 MHz") to an integer.
    
    Parameters:
    - frequency_string (str): The frequency measurement string to convert.
    
    Returns:
    - int: The numerical value of the frequency.
    """
    # Remove 'MHz' and any extra spaces, then convert to an integer
    numeric_value = int(frequency_string.replace('MHz', '').strip())
    return numeric_value

def convert_lanes_to_number(lane_string: str):
    """
    Converts a lane measurement string with a unit (e.g., "16x") to an integer.
    
    Parameters:
    - lane_string (str): The lane measurement string to convert.
    
    Returns:
    - int: The numerical value of the lane.
    """
    # Remove 'x' and any extra spaces, then convert to an integer
    numeric_value = int(lane_string.replace('x', '').strip())
    return numeric_value

def convert_memory_to_number(memory_string: str):
    """
    Converts a memory size string with a unit (e.g., "24576 MiB") to an integer.
    
    Parameters:
    - memory_string (str): The memory size string to convert.
    
    Returns:
    - int: The numerical value of the memory size.
    """
    # Remove 'MiB' and any extra spaces, then convert to an integer
    numeric_value = int(memory_string.replace('MiB', '').strip())
    return numeric_value

def convert_percentage_to_number(percentage_string: str):
    """
    Converts a percentage string (e.g., "0 %") to an integer.
    
    Parameters:
    - percentage_string (str): The percentage string to convert.
    
    Returns:
    - int: The numerical value of the percentage.
    """
    # Remove '%' and any extra spaces, then convert to an integer
    numeric_value = int(percentage_string.replace('%', '').strip())
    return numeric_value

def convert_power_to_number(power_string: str):
    """
    Converts a power measurement string with a unit (e.g., "42.65 W") to a float.
    
    Parameters:
    - power_string (str): The power measurement string to convert.
    
    Returns:
    - float: The numerical value of the power measurement.
    """
    # Remove 'W' and any extra spaces, then convert to a float
    numeric_value = float(power_string.replace('W', '').strip())
    return numeric_value

def convert_temperature_to_number(temperature_string: str):
    """
    Converts a temperature string with a unit (e.g., "41 C") to an integer.
    
    Parameters:
    - temperature_string (str): The temperature string to convert.
    
    Returns:
    - int: The numerical value of the temperature.
    """
    # Remove 'C' and any extra spaces, then convert to an integer
    numeric_value = int(temperature_string.replace('C', '').strip())
    return numeric_value

def convert_voltage_to_number(voltage_string: str):
    """
    Converts a voltage measurement string with a unit (e.g., "737.500 mV") to a float.
    
    Parameters:
    - voltage_string (str): The voltage measurement string to convert.
    
    Returns:
    - float: The numerical value of the voltage.
    """
    # Remove 'mV' and any extra spaces, then convert to a float
    numeric_value = float(voltage_string.replace('mV', '').strip())
    return numeric_value
