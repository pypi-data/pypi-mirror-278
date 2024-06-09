"""
nvme_collector.py
"""
import json
import logging
import subprocess
from server_metrics.utils.prom.nvme import create_nvme_prom_file
from server_metrics.utils.models import Server
from server_metrics.utils.ssh import build_ssh_command

def run_nvme(server: Server, prom_directory: str):
    """
    Gets NVME data from servers using nvme smart-log

    Args:
        ip (str):
        port (int):
        key_path (str):
        username (str):
    """
    try:
        # Command to connect via SSH and run nvme smart-log
        ssh_command = "sudo nvme smart-log $(nvme list | awk '/nvme/ && NR>1 {print $1; exit}') -o json"
        result = subprocess.run(build_ssh_command(server, ssh_command), capture_output=True, text=True, check=False)

        if result.stdout:
            json_data = json.loads(result.stdout)
            create_nvme_prom_file(server.hostname, prom_directory, json_data)

        elif result.stderr:
            logging.error("Errors from %s:%s\n%s", server.ip, server.port, result.stderr)

    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.port, e)
