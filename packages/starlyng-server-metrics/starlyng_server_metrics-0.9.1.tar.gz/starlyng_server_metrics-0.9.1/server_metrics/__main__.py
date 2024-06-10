"""
main.py
"""

from server_metrics.utils.configuration import load_configuration
from server_metrics.utils.execute import execute_commands_on_servers

def main():
    """
    Runs the metric collectors for each listed server
    """
    # Load configuration
    servers, key_path, username, combined_metrics_dir = load_configuration()

    # Execute ssh commands on servers
    execute_commands_on_servers(servers, key_path, username, combined_metrics_dir)

if __name__ == "__main__":
    main()
