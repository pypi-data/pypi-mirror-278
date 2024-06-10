"""
sensors_collector.py
"""

from server_metrics.utils.prom.sensors import parse_sensors_for_prom
from server_metrics.utils.models import Server
from server_metrics.utils.ssh import parse_result_json, run_subprocess

def run_sensors(server: Server) -> str:
    """
    Gets sensors data from servers using sensors

    Args:
        server (Server):

    Returns:
        str:
    """

    # Command to connect via SSH and run sensors
    ssh_command = "sensors -j"
    result = run_subprocess(server, ssh_command)
    json_data = parse_result_json(result)
    return parse_sensors_for_prom(server.hostname, json_data)
