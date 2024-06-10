"""
ssh.py
"""

import json
import logging
import subprocess
from typing import Dict, List
from server_metrics.utils.models import Server

def build_ssh_command(server: Server, command: str) -> List[str]:
    """ Returns an ssh command that can be passed to subprocess.run

    Args:
        server (Server):
        command (str):

    Returns:
        List[str]:
    """
    return [
        "ssh",
        "-i", server.key_path,
        "-p", str(server.port),
        f"{server.username}@{server.ip}",
        f"{command}",
    ]

def run_subprocess(server: Server, command: str) -> subprocess.CompletedProcess:
    """
    Executes a command on a remote server via SSH and logs any errors.

    Args:
        server (Any): An instance containing the server's connection details.
        command (str): The command to execute on the remote server.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess run, containing information about the executed command.

    Logs:
        Logs errors if the command execution fails or if there is any error output from the command.
    """
    try:
        result = subprocess.run(build_ssh_command(server, command), capture_output=True, text=True, check=False)
        if result.stderr:
            logging.error("run_subprocess: Errors from %s:%s:%s\n%s", server.ip, server.port, command, result.stderr)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to execute on %s:%s: %s", server.ip, server.port, e)
        result = subprocess.CompletedProcess(args=command, returncode=e.returncode, stdout='', stderr=str(e))
    return result

def parse_result_json(result: subprocess.CompletedProcess) -> Dict:
    """
    Parses the JSON output from a subprocess result.

    Args:
        result (subprocess.CompletedProcess): The result of a subprocess run containing the command output.

    Returns:
        Union[str, dict]: A dictionary parsed from JSON if successful, otherwise an empty string.

    Logs:
        Logs an error message if JSON decoding fails.
    """
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON: %s", e)

    return {}
