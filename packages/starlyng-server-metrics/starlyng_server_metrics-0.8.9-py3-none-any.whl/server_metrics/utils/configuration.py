"""
configuration.py
"""

from pathlib import Path
import os
import argparse
from dotenv import load_dotenv

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run server metrics collectors.")
    parser.add_argument('--servers', type=str, help="Comma-separated list of servers in the format ip:port.")
    parser.add_argument('--key_path', type=str, help="Path to the SSH key.")
    parser.add_argument('--username', type=str, help="SSH username.")
    parser.add_argument('--combined_metrics_dir', type=str, help="Directory for combined_metrics.prom")
    return parser.parse_args()

def load_env_variables(dotenv_path=None):
    """Load environment variables from a .env file if it exists."""
    if dotenv_path:
        load_dotenv(dotenv_path=dotenv_path)
    else:
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

def get_configuration(args):
    """Retrieve configuration details, prioritizing command-line arguments, then environment variables."""
    servers_str = args.servers or os.getenv('SERVERS')
    key_path = args.key_path or os.getenv('KEY_PATH')
    username = args.username or os.getenv('USERNAME')
    combined_metrics_dir = args.combined_metrics_dir or os.getenv('COMBINED_METRICS_DIR', None)

    if not servers_str or not key_path or not username:
        raise ValueError("Missing configuration: ensure servers, key_path, and username are provided.")

    servers = [tuple(server.split(':')) for server in servers_str.split(',')]
    servers = [(ip, int(port)) for ip, port in servers]

    return servers, key_path, username, combined_metrics_dir

def load_configuration(dotenv_path=None):
    """
    Loads configuration from command-line arguments, environment variables, and .env file if it exists.

    This function first attempts to load the server configuration, SSH key path, and username
    from command-line arguments. If they are not provided, it falls back to environment variables 
    or the .env file located in the current working directory or a provided path.

    Returns:
        tuple: A tuple containing:
            - servers (list of tuples): A list of (ip, port) tuples representing server addresses.
            - key_path (str): Path to the SSH key for authentication.
            - username (str): Username for SSH authentication.
            - combined_metrics_dir (str): Directory for combined_metrics.prom
    """
    args = parse_arguments()
    load_env_variables(dotenv_path=dotenv_path)
    return get_configuration(args)
