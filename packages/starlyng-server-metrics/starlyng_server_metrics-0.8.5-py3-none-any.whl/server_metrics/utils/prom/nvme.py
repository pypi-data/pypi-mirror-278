"""
nvme.py
"""

import os
from typing import Dict
from utils.filter import filter_dict_by_keys

def create_nvme_prom_file(hostname: str, prom_directory: str, nvme_data: Dict[str, str]):
    """
    Creates a .prom file that will be processed by prometheus

    Args:
        ip (str):
        port (int):
        gpu_dict (Dict[int, Gpu]):
    """

    file_name = f'nvme_{hostname}_metrics.prom'
    file_path = os.path.join(prom_directory, file_name)
    file_contents = parse_nvme_json_for_prom(nvme_data, hostname)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_contents)

def parse_nvme_json_for_prom(machine: Dict[str, str], hostname: str) -> str:
    """
    Args:
        machine (Dict[str, str]):
        hostname (str):

    Returns:
        str:
    """

    expected_keys = [
        'critical_comp_time',
        'media_errors',
        'power_cycles',
        'power_on_hours',
        'temperature',
        'temperature_sensor_1',
        'temperature_sensor_2',
        'unsafe_shutdowns',
        'warning_temp_time',
    ]

    filtered_machine = filter_dict_by_keys(machine, expected_keys)

    return '\n'.join(f'node_exporter_nvme_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
