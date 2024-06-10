"""
machine.py
"""

from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys

def parse_machine_for_prom(hostname: str, machine: Dict[str, str]) -> str:
    """
    Args:
        hostname (str):
        machine (Dict[str, str]):

    Returns:
        str:
    """

    expected_keys = [
        'aer_error_count',
        'pending_updates_count',
    ]

    filtered_machine = filter_dict_by_keys(machine, expected_keys)

    return '\n'.join(f'node_exporter_machine_{key}{{hostname="{hostname}"}} {value}' for key, value in filtered_machine.items())
