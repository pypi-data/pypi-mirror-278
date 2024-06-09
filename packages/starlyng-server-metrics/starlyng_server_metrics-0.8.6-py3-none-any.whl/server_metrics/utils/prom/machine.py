"""
machine.py
"""

import os
from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys

def create_machine_prom_file(hostname: str, prom_directory: str, machine_json: Dict[str, str]):
    """
    Creates a .prom file that will be processed by prometheus

    Args:
        ip (str):
        port (int):
        gpu_dict (Dict[int, Gpu]):
    """

    file_name = f'machine_{hostname}_metrics.prom'
    file_path = os.path.join(prom_directory, file_name)
    file_contents = parse_machine_json_for_prom(machine_json, hostname)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_contents)

def parse_machine_json_for_prom(machine: Dict[str, str], hostname: str) -> str:
    """
    Args:
        machine (Dict[str, str]):
        hostname (str):

    Returns:
        str:
    """

    expected_keys = [
        'aer_error_count',
        'pending_updates_count',
    ]

    filtered_machine = filter_dict_by_keys(machine, expected_keys)

    return '\n'.join(f'node_exporter_machine_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
