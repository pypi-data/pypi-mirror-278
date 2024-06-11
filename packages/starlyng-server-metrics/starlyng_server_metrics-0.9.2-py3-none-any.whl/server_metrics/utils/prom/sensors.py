"""
sensors.py
"""

import logging
from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys

def parse_sensors_for_prom(hostname: str, sensors: Dict[str, str]) -> str:
    """
    Args:
        hostname (str):
        sensors (Dict[str, str]):

    Returns:
        str:
    """

    sensors_dict: Dict[str, int] = {
        'cpu_temp': 0
    }

    for key in sensors:
        if 'Tctl' in sensors[key]:
            # AMD Epyc CPU
            amd_cpu = sensors[key]['Tctl']
            if 'temp1_input' in amd_cpu:
                try:
                    sensors_dict['cpu_temp'] = int(amd_cpu['temp1_input'])
                except (ValueError, TypeError) as e:
                    logging.error("Error reading AMD CPU temp1_input: %s", e)
        if 'Package id 0' in sensors[key]:
            # Intel CPU
            intel_cpu = sensors[key]['Package id 0']
            if 'temp1_input' in intel_cpu:
                try:
                    sensors_dict['cpu_temp'] = int(intel_cpu['temp1_input'])
                except (ValueError, TypeError) as e:
                    logging.error("Error reading AMD CPU temp1_input: %s", e)

    expected_keys = [
        'cpu_temp',
    ]

    filtered_machine = filter_dict_by_keys(sensors_dict, expected_keys)

    return '\n'.join(f'node_exporter_sensors_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
