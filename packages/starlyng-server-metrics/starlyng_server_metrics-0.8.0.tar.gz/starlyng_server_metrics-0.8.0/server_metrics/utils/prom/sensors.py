"""
sensors.py
"""

import os
from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys

def create_sensors_prom_file(hostname: str, prom_directory: str, sensors_data: Dict[str, str]):
    """
    Creates a .prom file that will be processed by prometheus

    Args:
        ip (str):
        port (int):
        gpu_dict (Dict[int, Gpu]):
    """

    file_name = f'sensors_{hostname}_metrics.prom'
    file_path = os.path.join(prom_directory, file_name)
    file_contents = parse_sensors_json_for_prom(sensors_data, hostname)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_contents)

def parse_sensors_json_for_prom(sensors: Dict[str, str], hostname: str) -> str:
    """
    Args:
        machine (Dict[str, str]):
        hostname (str):

    Returns:
        str:
    """

    sensors_dict: Dict[str, int] = {}

    for key in sensors:
        if 'Tctl' in sensors[key]:
            # AMD Epyc CPU
            sensors_dict['cpu_temp'] = int(sensors[key]['Tctl']['temp1_input'])
        if 'Package id 0' in sensors[key]:
            # Intel CPU
            sensors_dict['cpu_temp'] = int(sensors[key]['Package id 0']['temp1_input'])

    expected_keys = [
        'cpu_temp',
    ]

    filtered_machine = filter_dict_by_keys(sensors_dict, expected_keys)

    return '\n'.join(f'node_exporter_sensors_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
