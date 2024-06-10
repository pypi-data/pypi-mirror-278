"""
ssh.py
"""
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
from server_metrics.collectors.gpu_collector import run_nvidia_smi
from server_metrics.collectors.machine_collector import run_machine_commands
from server_metrics.collectors.nvme_collector import run_nvme
from server_metrics.collectors.sensors_collector import run_sensors
from server_metrics.utils.models import Server
from server_metrics.utils.parse_hostname import get_hostname

class MetricCollectorError(Exception):
    """Custom exception for metric collector errors."""

    def __init__(self, message, original_exception):
        super().__init__(message)
        self.original_exception = original_exception

def create_combined_metrics_prom(combined_metrics_dir: str, combined_results: str):
    """
    Args:
        directory (str): _description_
    """

    file_name = 'combined_metrics.prom'
    file_path = os.path.join(combined_metrics_dir, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(combined_results)

def run_collectors_for_server(server: Server) -> List[str]:
    """
    Runs various metric collectors for a specified server in parallel.

    Args:
        directory (str): The directory where the output should be stored.
        server (Server): An instance of the Server class containing server information.

    Returns:
        list: A list of results from the metric collectors.
    """
    collectors = [
        (run_nvidia_smi, server),
        (run_machine_commands, server),
        (run_nvme, server),
        (run_sensors, server),
    ]

    results = []
    with ThreadPoolExecutor() as executor:
        future_to_collector = {executor.submit(func, server): func for func, server in collectors}

        for future in as_completed(future_to_collector):
            func = future_to_collector[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                logging.error("Error in %s: %s", func.__name__, exc)
                raise MetricCollectorError(f"{func.__name__} raised an exception", exc) from exc

    return results

def execute_commands_on_servers(servers: List[Tuple[str, int]], key_path: str, username: str, combined_metrics_dir: str):
    """
    Executes various commands on a list of servers using threading for concurrency.

    Args:
        servers (list): A list of tuples, each containing a server IP and port.
        key_path (str): The path to the SSH key.
        username (str): The SSH username.
        combined_metrics_dir (str): The directory where combined metrics output should be stored.

    Returns:
        None
    """
    all_results = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for server_ip, server_port in servers:
            try:
                server_info = {
                    'hostname': get_hostname(server_ip, server_port),
                    'ip': server_ip,
                    'key_path': key_path,
                    'port': server_port,
                    'username': username,
                }
                server = Server(**server_info)
                futures.append(executor.submit(run_collectors_for_server, server))
            except Exception as exc:
                logging.error("Error initializing server %s: %s", server_ip, exc)
                raise MetricCollectorError(f"Error initializing server {server_ip}", exc) from exc

        for future in as_completed(futures):
            try:
                result = future.result()
                all_results.extend(result)
            except MetricCollectorError as exc:
                logging.error("MetricCollectorError: %s", exc)

    # Combine all results into a single string
    combined_results = '\n'.join(all_results)

    create_combined_metrics_prom(combined_metrics_dir, combined_results)
