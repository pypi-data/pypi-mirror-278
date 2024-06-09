"""
machine_collector.py
"""
import logging
import subprocess
from utils.prom.machine import create_machine_prom_file
from utils.models import Server
from utils.ssh import build_ssh_command

def run_journalctl(server: Server, prom_directory: str):
    """
    Gets machine data from servers using various commands

    Args:
        ip (str):
        port (int):
        key_path (str):
        username (str):
    """
    try:
        # Command to connect via SSH and run journalctl and run apt-get -s upgrade
        commands = [
            "journalctl --since '24 hours ago' | grep -E 'AER:|Corrected|Uncorrected' | wc -l",
            "apt-get -s upgrade | grep -P 'Inst ' | wc -l"
        ]
        ssh_command = " && ".join(commands)
        result = subprocess.run(build_ssh_command(server, ssh_command), capture_output=True, text=True, check=False)

        if result.returncode == 0:
            outputs = result.stdout.strip().split('\n')
            if len(outputs) == len(commands):
                journalctl_output = int(outputs[0].strip())
                upgrade_output = int(outputs[1].strip())

                json_data = {
                    "aer_error_count": journalctl_output,
                    "pending_updates_count": upgrade_output,
                }
                create_machine_prom_file(server.hostname, prom_directory, json_data)
            else:
                logging.error("Unexpected output format from combined command on %s:%s", server.ip, server.port)
        else:
            logging.error("Command failed on %s:%s\n%s", server.ip, server.port, result.stderr)

    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.port, e)
