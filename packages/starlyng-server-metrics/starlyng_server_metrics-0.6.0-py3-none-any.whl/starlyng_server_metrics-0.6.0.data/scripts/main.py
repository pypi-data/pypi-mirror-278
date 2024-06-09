"""
main.py
"""

from server_metrics.utils.configuration import load_configuration
from server_metrics.utils.file import clear_directory, create_directory
from server_metrics.utils.execute import execute_commands_on_servers

def main():
    """
    Runs the metric collectors for each listed server
    """
    directory = 'data/prom'

    # Clear the data/prom directory
    clear_directory(directory)

    # Create the data/prom directory
    create_directory(directory)

    # Load configuration
    servers, key_path, username, combined_metrics_dir = load_configuration()

    # Execute ssh commands on servers
    execute_commands_on_servers(servers, key_path, username, directory, combined_metrics_dir)

if __name__ == "__main__":
    main()
