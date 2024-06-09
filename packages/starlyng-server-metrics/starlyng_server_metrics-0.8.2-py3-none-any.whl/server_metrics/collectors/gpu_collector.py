"""
gpu_collector.py
"""
import json
import logging
import subprocess
from utils.prom.gpu import create_gpu_prom_file
from utils.models import Server
from utils.ssh import build_ssh_command
from utils.xml_parser import xml_to_json

def run_nvidia_smi(server: Server, prom_directory: str):
    """
    Gets GPU data from servers using nvidia-smi

    Args:
        ip (str):
        port (int):
        key_path (str):
        username (str):
    """
    try:
        # Command to connect via SSH and run nvidia-smi
        ssh_command = "nvidia-smi -q -x"
        result = subprocess.run(build_ssh_command(server, ssh_command), capture_output=True, text=True, check=False)

        if result.stdout:
            json_output = json.dumps(xml_to_json(result.stdout), indent=4)
            json_data = json.loads(json_output)
            create_gpu_prom_file(server.hostname, prom_directory, json_data)

        elif result.stderr:
            logging.error("Errors from %s:%s\n%s", server.ip, server.port, result.stderr)

    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.port, e)
