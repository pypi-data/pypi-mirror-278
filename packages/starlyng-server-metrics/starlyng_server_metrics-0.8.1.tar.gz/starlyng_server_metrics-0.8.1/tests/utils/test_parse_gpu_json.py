"""
Testing for parse_gpu_json module
"""
from server_metrics.utils.parse_gpu_json import parse_gpu_json_to_dict
from data.gpu_1_json import gpu_1_json_dict

def test_parse_gpu_json_to_dict_general():
    """
    Test general gpu data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['product_name'] == "NVIDIA GeForce RTX 3090"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['product_brand'] == "GeForce"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['product_architecture'] == "Ampere"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['display_mode'] == "Disabled"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['display_active'] == "Disabled"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['persistence_mode'] == "Enabled"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['serial'] == "1561121005298"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['uuid'] == "GPU-5c41118e-f6fa-9012-e7e9-397f50ac0515"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['minor_number'] == "0"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['vbios_version'] == "94.02.4B.00.0B"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['board_id'] == "0x100"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['gpu_part_number'] == "2204-300-A1"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['gpu_module_id'] == "1"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fan_speed'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['compute_mode'] == "Default"

def test_parse_gpu_json_to_dict_pci_general():
    """
    Test general pci data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_bus'] == "01"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_device'] == "00"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_device_id'] == "220410DE"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_bus_id'] == "00000000:01:00.0"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_sub_system_id'] == "147D10DE"

def test_parse_gpu_json_to_dict_pci_link_info():
    """
    Test pci link info data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_pcie_gen_max_link_gen'] == 3
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_pcie_gen_current_link_gen'] == 1
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_pcie_gen_device_current_link_gen'] == 1
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_pcie_gen_device_max_device_link_gen'] == 4
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_pcie_gen_device_max_host_link_gen'] == 3
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_link_widths_max_link_width'] == 16
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['pci_gpu_link_info_link_widths_current_link_width'] == 16

def test_parse_gpu_json_to_dict_fb_memory():
    """
    Test fb memory usage data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fb_memory_usage_total'] == 24576
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fb_memory_usage_reserved'] == 323
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fb_memory_usage_used'] == 1
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fb_memory_usage_free'] == 24251

def test_parse_gpu_json_to_dict_bar1_memory():
    """
    Test bar1 memory data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['bar1_memory_usage_total'] == 256
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['bar1_memory_usage_used'] == 2
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['bar1_memory_usage_free'] == 254

def test_parse_gpu_json_to_dict_cc_protected_memory():
    """
    Test cc protected memory data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['cc_protected_memory_usage_total'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['cc_protected_memory_usage_used'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['cc_protected_memory_usage_free'] == 0

def test_parse_gpu_json_to_dict_utilization():
    """
    Test utilization data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_gpu_util'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_memory_util'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_encoder_util'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_decoder_util'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_jpeg_util'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['utilization_ofa_util'] == 0

def test_parse_gpu_json_to_dict_encoder_stats():
    """
    Test encoder stats data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['encoder_stats_session_count'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['encoder_stats_average_fps'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['encoder_stats_average_latency'] == 0

def test_parse_gpu_json_to_dict_fcb_stats():
    """
    Test fcb stats data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fbc_stats_session_count'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fbc_stats_average_fps'] == 0
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['fbc_stats_average_latency'] == 0

def test_parse_gpu_json_to_dict_temperature():
    """
    Test temperature data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['temperature_gpu_temp'] == 45
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['temperature_gpu_temp_max_threshold'] == 98
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['temperature_gpu_temp_slow_threshold'] == 95
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['temperature_gpu_temp_max_gpu_threshold'] == 93
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['temperature_gpu_target_temperature'] == 83

def test_parse_gpu_json_to_dict_supported_gpu_target_temp():
    """
    Test supported gpu target temp data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['supported_gpu_target_temp_min'] == 65
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['supported_gpu_target_temp_max'] == 90

def test_parse_gpu_json_to_dict_gpu_power():
    """
    Test gpu power data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_power_state'] == "P8"
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_power_draw'] == 14.40
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_current_power_limit'] == 300.00
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_requested_power_limit'] == 300.00
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_default_power_limit'] == 350.00
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_min_power_limit'] == 100.00
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['power_readings_max_power_limit'] == 400.00

def test_parse_gpu_json_to_dict_clocks():
    """
    Test clocks data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['clocks_graphics_clock'] == 300
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['clocks_sm_clock'] == 300
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['clocks_mem_clock'] == 405
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['clocks_video_clock'] == 555

def test_parse_gpu_json_to_dict_max_clocks():
    """
    Test max clocks data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['max_clocks_graphics_clock'] == 2100
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['max_clocks_sm_clock'] == 2100
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['max_clocks_mem_clock'] == 9751
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['max_clocks_video_clock'] == 1950

def test_parse_gpu_json_to_dict_voltage():
    """
    Test voltage data
    """
    assert parse_gpu_json_to_dict(gpu_1_json_dict['gpu'])['voltage_graphics_volt'] == 737.500
