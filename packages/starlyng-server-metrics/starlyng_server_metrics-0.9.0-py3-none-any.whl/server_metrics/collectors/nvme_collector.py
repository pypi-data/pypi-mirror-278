"""
nvme_collector.py
"""

from server_metrics.utils.prom.nvme import parse_nvme_for_prom
from server_metrics.utils.models import Server
from server_metrics.utils.ssh import parse_result_json, run_subprocess

def run_nvme(server: Server) -> str:
    """
    Gets NVME data from servers using nvme smart-log

    Args:
        server (Server):

    Returns:
        str:
    """

    # Command to connect via SSH and run nvme smart-log
    ssh_command = "sudo nvme smart-log $(nvme list | awk '/nvme/ && NR>1 {print $1; exit}') -o json"
    result = run_subprocess(server, ssh_command)
    json_data = parse_result_json(result)
    return parse_nvme_for_prom(server.hostname, json_data)
