"""
gpu.py
"""

from typing import Dict
from server_metrics.utils.filter import filter_dict_by_keys
from server_metrics.utils.models import Gpu
from server_metrics.utils.parse_gpu_json import parse_gpu_json_to_dict

def create_gpu_prom_file(hostname: str, json_data: Dict[str, str]) -> str:
    """
    Creates the .prom file contents that will be processed by prometheus

    Args:
        hostname (int):
        json_data (Dict[str, str]):

    Returns:
        str:
    """

    prom_file_contents = []

    if "gpu" in json_data:
        gpu_dict: Dict[int, Gpu] = {}
        # Check the number of attached GPUs
        num_gpus = int(json_data["attached_gpus"]["text"])
        if num_gpus > 1:
            gpus = json_data["gpu"]
            for index, gpu in enumerate(gpus):
                gpu_dict[index] = parse_gpu_json_to_dict(gpu)
        else:
            gpu = json_data["gpu"]
            gpu_dict[0] = parse_gpu_json_to_dict(gpu)

        for key, gpu in gpu_dict.items():
            pci_bus = gpu.get('pci_bus', None)
            if pci_bus is not None:
                file_contents = parse_gpu_dict_for_prom(gpu, hostname, pci_bus)
                prom_file_contents.append(file_contents)
            else:
                raise KeyError(f"Key '{key}' does not exist or value is None")

    return '\n'.join(prom_file_contents)

def parse_gpu_dict_for_prom(gpu: Gpu, hostname: str, pci_bus: str) -> str:
    """
    Args:
        gpu (Gpu):
        hostname (str):
        pci_bus (str):

    Returns:
        str:
    """

    expected_keys = [
        'bar1_memory_usage_total',
        'bar1_memory_usage_used',
        'bar1_memory_usage_free',
        'cc_protected_memory_usage_total',
        'cc_protected_memory_usage_used',
        'cc_protected_memory_usage_free',
        'clocks_graphics_clock',
        'clocks_sm_clock',
        'clocks_mem_clock',
        'clocks_video_clock:',
        'encoder_stats_session_count',
        'encoder_stats_average_fps',
        'encoder_stats_average_latency',
        'fan_speed',
        'fb_memory_usage_total',
        'fb_memory_usage_reserved',
        'fb_memory_usage_used',
        'fb_memory_usage_free',
        'fbc_stats_session_count',
        'fbc_stats_average_fps',
        'fbc_stats_average_latency',
        'max_clocks_graphics_clock',
        'max_clocks_sm_clock',
        'max_clocks_mem_clock:',
        'max_clocks_video_clock',
        'pci_gpu_link_info_pcie_gen_max_link_gen:',
        'pci_gpu_link_info_pcie_gen_current_link_gen',
        'pci_gpu_link_info_pcie_gen_device_current_link_gen',
        'pci_gpu_link_info_pcie_gen_device_max_device_link_gen',
        'pci_gpu_link_info_pcie_gen_device_max_host_link_gen',
        'pci_gpu_link_info_link_widths_max_link_width',
        'pci_gpu_link_info_link_widths_current_link_width',
        'power_readings_power_draw',
        'power_readings_current_power_limit',
        'power_readings_requested_power_limit',
        'power_readings_default_power_limit',
        'power_readings_min_power_limit',
        'power_readings_max_power_limit',
        'supported_gpu_target_temp_min',
        'supported_gpu_target_temp_max',
        'temperature_gpu_temp',
        'temperature_gpu_temp_max_threshold',
        'temperature_gpu_temp_slow_threshold',
        'temperature_gpu_temp_max_gpu_threshold',
        'temperature_gpu_target_temperature',
        'utilization_gpu_util',
        'utilization_memory_util',
        'utilization_encoder_util',
        'utilization_decoder_util',
        'utilization_jpeg_util',
        'utilization_ofa_util',
        'voltage_graphics_volt',
    ]

    filtered_gpu = filter_dict_by_keys(gpu, expected_keys)

    return '\n'.join(f'node_exporter_gpu_{key}{{gpu="{pci_bus}",hostname="{hostname}"}} {value}' for key, value in filtered_gpu.items())
