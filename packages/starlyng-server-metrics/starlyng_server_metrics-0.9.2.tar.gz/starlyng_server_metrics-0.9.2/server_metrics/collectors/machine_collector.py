"""
machine_collector.py
"""
import logging
from server_metrics.utils.prom.machine import parse_machine_for_prom
from server_metrics.utils.models import Server
from server_metrics.utils.ssh import run_subprocess

def run_machine_commands(server: Server) -> str:
    """
    Gets machine data from servers using various commands

    Args:
        server (Server):

    Returns:
        str:
    """

    # Command to connect via SSH and run journalctl and run apt-get -s upgrade
    commands = [
        "journalctl --since '24 hours ago' | grep -E 'AER:|Corrected|Uncorrected' | wc -l",
        "apt-get -s upgrade | grep -P 'Inst ' | wc -l"
    ]
    ssh_command = " && ".join(commands)
    result = run_subprocess(server, ssh_command)

    prom_file_contents = ""
    if result.returncode == 0:
        outputs = result.stdout.strip().split('\n')
        if len(outputs) == len(commands):
            try:
                journalctl_output = int(outputs[0].strip())
                upgrade_output = int(outputs[1].strip())
                json_data = {
                    "aer_error_count": journalctl_output,
                    "pending_updates_count": upgrade_output,
                }
                prom_file_contents = parse_machine_for_prom(server.hostname, json_data)
            except ValueError as e:
                logging.error("Failed to parse command outputs on %s:%s: %s", server.ip, server.port, e)
        else:
            logging.error("Unexpected output format from combined command on %s:%s", server.ip, server.port)
    else:
        logging.error("Command failed on %s:%s\n%s", server.ip, server.port, result.stderr)

    return prom_file_contents
