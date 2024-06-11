"""
nvme.py
"""

from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys

def parse_nvme_for_prom(hostname: str, nvme: Dict[str, str]) -> str:
    """
    Args:
        hostname (str):
        nvme (Dict[str, str]):

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

    filtered_machine = filter_dict_by_keys(nvme, expected_keys)

    return '\n'.join(f'node_exporter_nvme_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
