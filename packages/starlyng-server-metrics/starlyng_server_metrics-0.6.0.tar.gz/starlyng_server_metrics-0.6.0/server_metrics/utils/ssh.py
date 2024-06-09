"""
ssh.py
"""

from server_metrics.utils.models import Server

def build_ssh_command(server: Server, command: str) -> list[str]:
    """ Returns an ssh command that can be passed to subprocess.run

    Args:
        server (Server):
        command (str):

    Returns:
        list[str]:
    """
    return [
        "ssh",
        "-i", server.key_path,
        "-p", str(server.port),
        f"{server.username}@{server.ip}",
        f"{command}"
    ]
