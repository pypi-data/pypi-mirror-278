"""
parse_gpu_json.py
"""
from typing import Dict
from server_metrics.utils.conversion import (
    convert_frequency_to_number,
    convert_lanes_to_number,
    convert_memory_to_number,
    convert_percentage_to_number,
    convert_power_to_number,
    convert_temperature_to_number,
    convert_voltage_to_number
)
from server_metrics.utils.models import Gpu

def parse_gpu_json_to_dict(gpu_json: Dict[str, str]) -> Gpu:
    """
    Parses gpu json data to a dict that can be used to generate prometheus .prom file

    Args:
        gpu_json (Dict[str, str])

    Returns:
        Gpu
    """
    gpu_dict = {
        'product_name': gpu_json['product_name']['text'],
        'product_brand': gpu_json['product_brand']['text'],
        'product_architecture': gpu_json['product_architecture']['text'],
        'display_mode': gpu_json['display_mode']['text'],
        'display_active': gpu_json['display_active']['text'],
        'persistence_mode': gpu_json['persistence_mode']['text'],
        'serial': gpu_json['serial']['text'],
        'uuid': gpu_json['uuid']['text'],
        'minor_number': gpu_json['minor_number']['text'],
        'vbios_version': gpu_json['vbios_version']['text'],
        'board_id': gpu_json['board_id']['text'],
        'gpu_part_number': gpu_json['gpu_part_number']['text'],
        'gpu_module_id': gpu_json['gpu_module_id']['text'],
        'fan_speed': convert_percentage_to_number(gpu_json['fan_speed']['text']),
        'compute_mode': gpu_json['compute_mode']['text'],
    }

    # Define a mapping of keys to their corresponding parsing functions
    parse_functions = {
        'pci': _parse_pci_data,
        'fb_memory_usage': _parse_fb_memory_usage_data,
        'bar1_memory_usage': _parse_bar1_memory_usage_data,
        'cc_protected_memory_usage': _parse_cc_protected_memory_usage_data,
        'utilization': _parse_utilization_data,
        'encoder_stats': _parse_encoder_stats_data,
        'fbc_stats': _parse_fbc_stats_data,
        'temperature': _parse_temperature_data,
        'supported_gpu_target_temp': _parse_supported_gpu_target_temp_data,
        'gpu_power_readings': _parse_power_readings_data,
        'clocks': _parse_clocks_data,
        'max_clocks': _parse_max_clocks_data,
        'voltage': _parse_voltage_data,
    }

    # Iterate over the parse_functions and update gpu_dict if the key exists in gpu_json
    for key, parse_func in parse_functions.items():
        if key in gpu_json:
            gpu_dict.update(parse_func(gpu_json[key]))

    return gpu_dict

def _parse_pci_data(pci: Dict[str, str]) -> Dict[str, str]:
    """
    Parse pci data

    Args:
        pci (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """
    gpu_dict = {
        'pci_bus': pci['pci_bus']['text'],
        'pci_device': pci['pci_device']['text'],
        'pci_device_id': pci['pci_device_id']['text'],
        'pci_bus_id': pci['pci_bus_id']['text'],
        'pci_sub_system_id': pci['pci_sub_system_id']['text'],
    }

    if 'pci_gpu_link_info' in pci:
        pci_gpu_link_info = pci['pci_gpu_link_info']
        if 'pcie_gen' in pci_gpu_link_info:
            pcie_gen = pci_gpu_link_info['pcie_gen']
            gpu_dict['pci_gpu_link_info_pcie_gen_max_link_gen'] = int(pcie_gen['max_link_gen']['text'])
            gpu_dict['pci_gpu_link_info_pcie_gen_current_link_gen'] = int(pcie_gen['current_link_gen']['text'])
            gpu_dict['pci_gpu_link_info_pcie_gen_device_current_link_gen'] = int(pcie_gen['device_current_link_gen']['text'])
            gpu_dict['pci_gpu_link_info_pcie_gen_device_max_device_link_gen'] = int(pcie_gen['max_device_link_gen']['text'])
            gpu_dict['pci_gpu_link_info_pcie_gen_device_max_host_link_gen'] = int(pcie_gen['max_host_link_gen']['text'])

        if 'link_widths' in pci_gpu_link_info:
            link_widths = pci_gpu_link_info['link_widths']
            gpu_dict['pci_gpu_link_info_link_widths_max_link_width'] = convert_lanes_to_number(link_widths['max_link_width']['text'])
            gpu_dict['pci_gpu_link_info_link_widths_current_link_width'] = convert_lanes_to_number(link_widths['current_link_width']['text'])

    return gpu_dict

def _parse_fb_memory_usage_data(fb_memory_usage: Dict[str, str]) -> Dict[str, str]:
    """
    Parse fb_memory_usage data

    Args:
        fb_memory_usage (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'fb_memory_usage_total': convert_memory_to_number(fb_memory_usage['total']['text']),
        'fb_memory_usage_reserved': convert_memory_to_number(fb_memory_usage['reserved']['text']),
        'fb_memory_usage_used': convert_memory_to_number(fb_memory_usage['used']['text']),
        'fb_memory_usage_free': convert_memory_to_number(fb_memory_usage['free']['text']),
    }

def _parse_bar1_memory_usage_data(bar1_memory_usage: Dict[str, str]) -> Dict[str, str]:
    """
    Parse bar1_memory_usage data

    Args:
        bar1_memory_usage (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'bar1_memory_usage_total': convert_memory_to_number(bar1_memory_usage['total']['text']),
        'bar1_memory_usage_used': convert_memory_to_number(bar1_memory_usage['used']['text']),
        'bar1_memory_usage_free': convert_memory_to_number(bar1_memory_usage['free']['text']),
    }

def _parse_cc_protected_memory_usage_data(cc_protected_memory_usage: Dict[str, str]) -> Dict[str, str]:
    """
    Parse cc_protected_memory_usage data

    Args:
        cc_protected_memory_usage (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'cc_protected_memory_usage_total': convert_memory_to_number(cc_protected_memory_usage['total']['text']),
        'cc_protected_memory_usage_used': convert_memory_to_number(cc_protected_memory_usage['used']['text']),
        'cc_protected_memory_usage_free': convert_memory_to_number(cc_protected_memory_usage['free']['text']),
    }

def _parse_utilization_data(utilization: Dict[str, str]) -> Dict[str, str]:
    """
    Parse utilization data

    Args:
        utilization (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'utilization_gpu_util': convert_percentage_to_number(utilization['gpu_util']['text']),
        'utilization_memory_util': convert_percentage_to_number(utilization['memory_util']['text']),
        'utilization_encoder_util': convert_percentage_to_number(utilization['encoder_util']['text']),
        'utilization_decoder_util': convert_percentage_to_number(utilization['decoder_util']['text']),
        'utilization_jpeg_util': convert_percentage_to_number(utilization['jpeg_util']['text']),
        'utilization_ofa_util': convert_percentage_to_number(utilization['ofa_util']['text']),
    }

def _parse_encoder_stats_data(encoder_stats: Dict[str, str]) -> Dict[str, str]:
    """
    Parse encoder_stats data

    Args:
        encoder_stats (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'encoder_stats_session_count': int(encoder_stats['session_count']['text']),
        'encoder_stats_average_fps': int(encoder_stats['average_fps']['text']),
        'encoder_stats_average_latency': int(encoder_stats['average_latency']['text']),
    }

def _parse_fbc_stats_data(fbc_stats: Dict[str, str]) -> Dict[str, str]:
    """
    Parse fbc_stats data

    Args:
        fbc_stats (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'fbc_stats_session_count': int(fbc_stats['session_count']['text']),
        'fbc_stats_average_fps': int(fbc_stats['average_fps']['text']),
        'fbc_stats_average_latency': int(fbc_stats['average_latency']['text']),
    }

def _parse_temperature_data(temperature: Dict[str, str]) -> Dict[str, str]:
    """
    Parse temperature data

    Args:
        temperature (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'temperature_gpu_temp': convert_temperature_to_number(temperature['gpu_temp']['text']),
        'temperature_gpu_temp_max_threshold': convert_temperature_to_number(temperature['gpu_temp_max_threshold']['text']),
        'temperature_gpu_temp_slow_threshold': convert_temperature_to_number(temperature['gpu_temp_slow_threshold']['text']),
        'temperature_gpu_temp_max_gpu_threshold': convert_temperature_to_number(temperature['gpu_temp_max_gpu_threshold']['text']),
        'temperature_gpu_target_temperature': convert_temperature_to_number(temperature['gpu_target_temperature']['text']),
    }

def _parse_supported_gpu_target_temp_data(supported_gpu_target_temp: Dict[str, str]) -> Dict[str, str]:
    """
    Parse supported_gpu_target_temp data

    Args:
        supported_gpu_target_temp (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'supported_gpu_target_temp_min': convert_temperature_to_number(supported_gpu_target_temp['gpu_target_temp_min']['text']),
        'supported_gpu_target_temp_max': convert_temperature_to_number(supported_gpu_target_temp['gpu_target_temp_max']['text']),
    }

def _parse_power_readings_data(power_readings: Dict[str, str]) -> Dict[str, str]:
    """
    Parse power_readings data
    Do not include gpu_ before power_readings_ in keyname for better .prom file formatting.

    Args:
        power_readings (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'power_readings_power_state': power_readings['power_state']['text'],
        'power_readings_power_draw': convert_power_to_number(power_readings['power_draw']['text']),
        'power_readings_current_power_limit': convert_power_to_number(power_readings['current_power_limit']['text']),
        'power_readings_requested_power_limit': convert_power_to_number(power_readings['requested_power_limit']['text']),
        'power_readings_default_power_limit': convert_power_to_number(power_readings['default_power_limit']['text']),
        'power_readings_min_power_limit': convert_power_to_number(power_readings['min_power_limit']['text']),
        'power_readings_max_power_limit': convert_power_to_number(power_readings['max_power_limit']['text']),
    }

def _parse_clocks_data(clocks: Dict[str, str]) -> Dict[str, str]:
    """
    Parse clocks data

    Args:
        clocks (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'clocks_graphics_clock': convert_frequency_to_number(clocks['graphics_clock']['text']),
        'clocks_sm_clock': convert_frequency_to_number(clocks['sm_clock']['text']),
        'clocks_mem_clock': convert_frequency_to_number(clocks['mem_clock']['text']),
        'clocks_video_clock': convert_frequency_to_number(clocks['video_clock']['text']),
    }

def _parse_max_clocks_data(max_clocks: Dict[str, str]) -> Dict[str, str]:
    """
    Parse max_clocks data

    Args:
        max_clocks (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'max_clocks_graphics_clock': convert_frequency_to_number(max_clocks['graphics_clock']['text']),
        'max_clocks_sm_clock': convert_frequency_to_number(max_clocks['sm_clock']['text']),
        'max_clocks_mem_clock': convert_frequency_to_number(max_clocks['mem_clock']['text']),
        'max_clocks_video_clock': convert_frequency_to_number(max_clocks['video_clock']['text']),
    }

def _parse_voltage_data(voltage: Dict[str, str]) -> Dict[str, str]:
    """
    Parse voltage data

    Args:
        voltage (Dict[str, str]):

    Returns:
        Dict[str, str]:
    """

    return {
        'voltage_graphics_volt': convert_voltage_to_number(voltage['graphics_volt']['text']),
    }
