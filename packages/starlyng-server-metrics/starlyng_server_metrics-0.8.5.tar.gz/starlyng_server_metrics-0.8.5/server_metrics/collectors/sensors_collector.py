"""
sensors_collector.py
"""
import json
import logging
import subprocess
from utils.prom.sensors import create_sensors_prom_file
from utils.models import Server
from utils.ssh import build_ssh_command

def run_sensors(server: Server, prom_directory: str):
    """
    Gets sensors data from servers using sensors

    Args:
        ip (str):
        port (int):
        key_path (str):
        username (str):
    """
    try:
        # Command to connect via SSH and run sensors
        ssh_command = "sensors -j"
        result = subprocess.run(build_ssh_command(server, ssh_command), capture_output=True, text=True, check=False)

        if result.stdout:
            json_data = json.loads(result.stdout)
            create_sensors_prom_file(server.hostname, prom_directory, json_data)

        elif result.stderr:
            logging.error("Errors from %s:%s\n%s", server.ip, server.port, result.stderr)

    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.port, e)
