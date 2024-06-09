"""
ssh.py
"""
import threading
from server_metrics.collectors.gpu_collector import run_nvidia_smi
from server_metrics.collectors.machine_collector import run_journalctl
from server_metrics.collectors.nvme_collector import run_nvme
from server_metrics.collectors.sensors_collector import run_sensors
from server_metrics.utils.file import clear_directory, create_directory
from server_metrics.utils.models import Server
from server_metrics.utils.parse_hostname import get_hostname
from server_metrics.utils.prom.combine import prom_files

def create_combined_metrics_prom(directory: str, combined_metrics_dir: str):
    """
    Args:
        directory (str): _description_
    """
    node_exporter_directory = directory + '/node_exporter/'

    if combined_metrics_dir is not None:
        node_exporter_directory = combined_metrics_dir
    else:
         # Clear the data/prom directory
        clear_directory(node_exporter_directory)

        # Create the data/prom directory
        create_directory(node_exporter_directory)

    # Combine prom files and add to node exporter directory
    combined_file_name = node_exporter_directory + 'combined_metrics.prom'
    prom_files(directory, combined_file_name)

def run_collectors_for_server(directory: str, server: Server, threads: list):
    """
    Runs metric collectors for a selected server

    Args:
        directory (str): _description_
        server (Server): _description_
        threads (list): _description_
    """
    gpu_thread = threading.Thread(target=run_nvidia_smi, args=(server, directory))
    threads.append(gpu_thread)
    gpu_thread.start()

    machine_thread = threading.Thread(target=run_journalctl, args=(server, directory))
    threads.append(machine_thread)
    machine_thread.start()

    nvme_thread = threading.Thread(target=run_nvme, args=(server, directory))
    threads.append(nvme_thread)
    nvme_thread.start()

    sensors_thread = threading.Thread(target=run_sensors, args=(server, directory))
    threads.append(sensors_thread)
    sensors_thread.start()

def execute_commands_on_servers(servers, key_path, username, directory, combined_metrics_dir):
    """
    Execute various commands on a list of servers using threading.

    Args:
        servers (list): List of tuples containing server IP and port.
        key_path (str): Path to the SSH key.
        username (str): SSH username.
        directory (str): Directory where output should be stored.
    """

    threads = []
    for server_ip, server_port in servers:
        server_info = {
            'hostname': get_hostname(server_ip, server_port),
            'ip': server_ip,
            'key_path': key_path,
            'port': server_port,
            'username': username,
        }
        server = Server(**server_info)
        run_collectors_for_server(directory, server, threads)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    create_combined_metrics_prom(directory, combined_metrics_dir)
