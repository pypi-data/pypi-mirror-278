"""
models.py
"""

from typing import Dict, NewType
from dataclasses import dataclass

Gpu = NewType('Gpu', Dict[str, any])

@dataclass
class Server:
    """
    Represents a server with an IP address, port, and hostname.

    Attributes:
        hostname (str): The hostname of the server.
        ip (str): The IP address of the server.
        key_path (str): The key path of the server.
        port (str): The port number of the server.
        username (str): The username that you want to log into on the server.
    """
    hostname: str
    ip: str
    key_path: str
    port: str
    username: str
