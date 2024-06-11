"""
nvidia-smi json response with 4 GPUs
"""
from typing import Dict

gpu_4_json_dict: Dict[str, str] = {
    "timestamp": {
        "text": "Sun Jun  2 01:20:18 2024"
    },
    "driver_version": {
        "text": "550.54.15"
    },
    "cuda_version": {
        "text": "12.4"
    },
    "attached_gpus": {
        "text": "4"
    },
    "gpu": [
        {
            "product_name": {
                "text": "NVIDIA GeForce RTX 3090"
            },
            "product_brand": {
                "text": "GeForce"
            },
            "product_architecture": {
                "text": "Ampere"
            },
            "display_mode": {
                "text": "Disabled"
            },
            "display_active": {
                "text": "Disabled"
            },
            "persistence_mode": {
                "text": "Enabled"
            },
            "addressing_mode": {
                "text": "None"
            },
            "mig_mode": {
                "current_mig": {
                    "text": "N/A"
                },
                "pending_mig": {
                    "text": "N/A"
                }
            },
            "mig_devices": {
                "text": "None"
            },
            "accounting_mode": {
                "text": "Disabled"
            },
            "accounting_mode_buffer_size": {
                "text": "4000"
            },
            "driver_model": {
                "current_dm": {
                    "text": "N/A"
                },
                "pending_dm": {
                    "text": "N/A"
                }
            },
            "serial": {
                "text": "N/A"
            },
            "uuid": {
                "text": "GPU-817285e3-758e-25e4-3b80-d38475e31dd6"
            },
            "minor_number": {
                "text": "3"
            },
            "vbios_version": {
                "text": "94.02.42.C0.05"
            },
            "multigpu_board": {
                "text": "No"
            },
            "board_id": {
                "text": "0x100"
            },
            "board_part_number": {
                "text": "N/A"
            },
            "gpu_part_number": {
                "text": "2204-300-A1"
            },
            "gpu_fru_part_number": {
                "text": "N/A"
            },
            "gpu_module_id": {
                "text": "1"
            },
            "inforom_version": {
                "img_version": {
                    "text": "G001.0000.03.03"
                },
                "oem_object": {
                    "text": "2.0"
                },
                "ecc_object": {
                    "text": "N/A"
                },
                "pwr_object": {
                    "text": "N/A"
                }
            },
            "inforom_bbx_flush": {
                "latest_timestamp": {
                    "text": "N/A"
                },
                "latest_duration": {
                    "text": "N/A"
                }
            },
            "gpu_operation_mode": {
                "current_gom": {
                    "text": "N/A"
                },
                "pending_gom": {
                    "text": "N/A"
                }
            },
            "c2c_mode": {
                "text": "N/A"
            },
            "gpu_virtualization_mode": {
                "virtualization_mode": {
                    "text": "None"
                },
                "host_vgpu_mode": {
                    "text": "N/A"
                },
                "vgpu_heterogeneous_mode": {
                    "text": "N/A"
                }
            },
            "gpu_reset_status": {
                "reset_required": {
                    "text": "No"
                },
                "drain_and_reset_recommended": {
                    "text": "N/A"
                }
            },
            "gsp_firmware_version": {
                "text": "N/A"
            },
            "ibmnpu": {
                "relaxed_ordering_mode": {
                    "text": "N/A"
                }
            },
            "pci": {
                "pci_bus": {
                    "text": "01"
                },
                "pci_device": {
                    "text": "00"
                },
                "pci_domain": {
                    "text": "0000"
                },
                "pci_base_class": {
                    "text": "3"
                },
                "pci_sub_class": {
                    "text": "0"
                },
                "pci_device_id": {
                    "text": "220410DE"
                },
                "pci_bus_id": {
                    "text": "00000000:01:00.0"
                },
                "pci_sub_system_id": {
                    "text": "39823842"
                },
                "pci_gpu_link_info": {
                    "pcie_gen": {
                        "max_link_gen": {
                            "text": "4"
                        },
                        "current_link_gen": {
                            "text": "1"
                        },
                        "device_current_link_gen": {
                            "text": "1"
                        },
                        "max_device_link_gen": {
                            "text": "4"
                        },
                        "max_host_link_gen": {
                            "text": "4"
                        }
                    },
                    "link_widths": {
                        "max_link_width": {
                            "text": "16x"
                        },
                        "current_link_width": {
                            "text": "16x"
                        }
                    }
                },
                "pci_bridge_chip": {
                    "bridge_chip_type": {
                        "text": "N/A"
                    },
                    "bridge_chip_fw": {
                        "text": "N/A"
                    }
                },
                "replay_counter": {
                    "text": "0"
                },
                "replay_rollover_counter": {
                    "text": "0"
                },
                "tx_util": {
                    "text": "0 KB/s"
                },
                "rx_util": {
                    "text": "0 KB/s"
                },
                "atomic_caps_inbound": {
                    "text": "N/A"
                },
                "atomic_caps_outbound": {
                    "text": "N/A"
                }
            },
            "fan_speed": {
                "text": "0 %"
            },
            "performance_state": {
                "text": "P8"
            },
            "clocks_event_reasons": {
                "clocks_event_reason_gpu_idle": {
                    "text": "Active"
                },
                "clocks_event_reason_applications_clocks_setting": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_power_cap": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_power_brake_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sync_boost": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_display_clocks_setting": {
                    "text": "Not Active"
                }
            },
            "sparse_operation_mode": {
                "text": "N/A"
            },
            "fb_memory_usage": {
                "total": {
                    "text": "24576 MiB"
                },
                "reserved": {
                    "text": "323 MiB"
                },
                "used": {
                    "text": "1 MiB"
                },
                "free": {
                    "text": "24251 MiB"
                }
            },
            "bar1_memory_usage": {
                "total": {
                    "text": "256 MiB"
                },
                "used": {
                    "text": "2 MiB"
                },
                "free": {
                    "text": "254 MiB"
                }
            },
            "cc_protected_memory_usage": {
                "total": {
                    "text": "0 MiB"
                },
                "used": {
                    "text": "0 MiB"
                },
                "free": {
                    "text": "0 MiB"
                }
            },
            "compute_mode": {
                "text": "Default"
            },
            "utilization": {
                "gpu_util": {
                    "text": "0 %"
                },
                "memory_util": {
                    "text": "0 %"
                },
                "encoder_util": {
                    "text": "0 %"
                },
                "decoder_util": {
                    "text": "0 %"
                },
                "jpeg_util": {
                    "text": "0 %"
                },
                "ofa_util": {
                    "text": "0 %"
                }
            },
            "encoder_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "fbc_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "ecc_mode": {
                "current_ecc": {
                    "text": "N/A"
                },
                "pending_ecc": {
                    "text": "N/A"
                }
            },
            "ecc_errors": {
                "volatile": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    }
                },
                "aggregate": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    },
                    "sram_threshold_exceeded": {
                        "text": "N/A"
                    }
                },
                "aggregate_uncorrectable_sram_sources": {
                    "sram_l2": {
                        "text": "N/A"
                    },
                    "sram_sm": {
                        "text": "N/A"
                    },
                    "sram_microcontroller": {
                        "text": "N/A"
                    },
                    "sram_pcie": {
                        "text": "N/A"
                    },
                    "sram_other": {
                        "text": "N/A"
                    }
                }
            },
            "retired_pages": {
                "multiple_single_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "double_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "pending_blacklist": {
                    "text": "N/A"
                },
                "pending_retirement": {
                    "text": "N/A"
                }
            },
            "remapped_rows": {
                "text": "N/A"
            },
            "temperature": {
                "gpu_temp": {
                    "text": "39 C"
                },
                "gpu_temp_tlimit": {
                    "text": "N/A"
                },
                "gpu_temp_max_threshold": {
                    "text": "98 C"
                },
                "gpu_temp_slow_threshold": {
                    "text": "95 C"
                },
                "gpu_temp_max_gpu_threshold": {
                    "text": "93 C"
                },
                "gpu_target_temperature": {
                    "text": "83 C"
                },
                "memory_temp": {
                    "text": "N/A"
                },
                "gpu_temp_max_mem_threshold": {
                    "text": "N/A"
                }
            },
            "supported_gpu_target_temp": {
                "gpu_target_temp_min": {
                    "text": "65 C"
                },
                "gpu_target_temp_max": {
                    "text": "91 C"
                }
            },
            "gpu_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "42.41 W"
                },
                "current_power_limit": {
                    "text": "300.00 W"
                },
                "requested_power_limit": {
                    "text": "300.00 W"
                },
                "default_power_limit": {
                    "text": "420.00 W"
                },
                "min_power_limit": {
                    "text": "100.00 W"
                },
                "max_power_limit": {
                    "text": "450.00 W"
                }
            },
            "gpu_memory_power_readings": {
                "power_draw": {
                    "text": "N/A"
                }
            },
            "module_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "N/A"
                },
                "current_power_limit": {
                    "text": "N/A"
                },
                "requested_power_limit": {
                    "text": "N/A"
                },
                "default_power_limit": {
                    "text": "N/A"
                },
                "min_power_limit": {
                    "text": "N/A"
                },
                "max_power_limit": {
                    "text": "N/A"
                }
            },
            "clocks": {
                "graphics_clock": {
                    "text": "300 MHz"
                },
                "sm_clock": {
                    "text": "300 MHz"
                },
                "mem_clock": {
                    "text": "405 MHz"
                },
                "video_clock": {
                    "text": "555 MHz"
                }
            },
            "applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "default_applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "deferred_clocks": {
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "max_clocks": {
                "graphics_clock": {
                    "text": "2100 MHz"
                },
                "sm_clock": {
                    "text": "2100 MHz"
                },
                "mem_clock": {
                    "text": "9751 MHz"
                },
                "video_clock": {
                    "text": "1950 MHz"
                }
            },
            "max_customer_boost_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                }
            },
            "clock_policy": {
                "auto_boost": {
                    "text": "N/A"
                },
                "auto_boost_default": {
                    "text": "N/A"
                }
            },
            "voltage": {
                "graphics_volt": {
                    "text": "737.500 mV"
                }
            },
            "fabric": {
                "state": {
                    "text": "N/A"
                },
                "status": {
                    "text": "N/A"
                },
                "cliqueId": {
                    "text": "N/A"
                },
                "clusterUuid": {
                    "text": "N/A"
                },
                "health": {
                    "bandwidth": {
                        "text": "N/A"
                    }
                }
            },
            "supported_clocks": {
                "supported_mem_clock": [
                    {
                        "value": {
                            "text": "9751 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "9501 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "5001 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "810 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "405 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    }
                ]
            },
            "processes": {},
            "accounted_processes": {}
        },
        {
            "product_name": {
                "text": "NVIDIA GeForce RTX 3090"
            },
            "product_brand": {
                "text": "GeForce"
            },
            "product_architecture": {
                "text": "Ampere"
            },
            "display_mode": {
                "text": "Disabled"
            },
            "display_active": {
                "text": "Disabled"
            },
            "persistence_mode": {
                "text": "Enabled"
            },
            "addressing_mode": {
                "text": "None"
            },
            "mig_mode": {
                "current_mig": {
                    "text": "N/A"
                },
                "pending_mig": {
                    "text": "N/A"
                }
            },
            "mig_devices": {
                "text": "None"
            },
            "accounting_mode": {
                "text": "Disabled"
            },
            "accounting_mode_buffer_size": {
                "text": "4000"
            },
            "driver_model": {
                "current_dm": {
                    "text": "N/A"
                },
                "pending_dm": {
                    "text": "N/A"
                }
            },
            "serial": {
                "text": "N/A"
            },
            "uuid": {
                "text": "GPU-86b6053d-d745-10c3-41e5-e7da92904013"
            },
            "minor_number": {
                "text": "2"
            },
            "vbios_version": {
                "text": "94.02.26.80.C8"
            },
            "multigpu_board": {
                "text": "No"
            },
            "board_id": {
                "text": "0x4500"
            },
            "board_part_number": {
                "text": "N/A"
            },
            "gpu_part_number": {
                "text": "2204-300-A1"
            },
            "gpu_fru_part_number": {
                "text": "N/A"
            },
            "gpu_module_id": {
                "text": "1"
            },
            "inforom_version": {
                "img_version": {
                    "text": "G001.0000.03.03"
                },
                "oem_object": {
                    "text": "2.0"
                },
                "ecc_object": {
                    "text": "N/A"
                },
                "pwr_object": {
                    "text": "N/A"
                }
            },
            "inforom_bbx_flush": {
                "latest_timestamp": {
                    "text": "N/A"
                },
                "latest_duration": {
                    "text": "N/A"
                }
            },
            "gpu_operation_mode": {
                "current_gom": {
                    "text": "N/A"
                },
                "pending_gom": {
                    "text": "N/A"
                }
            },
            "c2c_mode": {
                "text": "N/A"
            },
            "gpu_virtualization_mode": {
                "virtualization_mode": {
                    "text": "None"
                },
                "host_vgpu_mode": {
                    "text": "N/A"
                },
                "vgpu_heterogeneous_mode": {
                    "text": "N/A"
                }
            },
            "gpu_reset_status": {
                "reset_required": {
                    "text": "No"
                },
                "drain_and_reset_recommended": {
                    "text": "N/A"
                }
            },
            "gsp_firmware_version": {
                "text": "N/A"
            },
            "ibmnpu": {
                "relaxed_ordering_mode": {
                    "text": "N/A"
                }
            },
            "pci": {
                "pci_bus": {
                    "text": "45"
                },
                "pci_device": {
                    "text": "00"
                },
                "pci_domain": {
                    "text": "0000"
                },
                "pci_base_class": {
                    "text": "3"
                },
                "pci_sub_class": {
                    "text": "0"
                },
                "pci_device_id": {
                    "text": "220410DE"
                },
                "pci_bus_id": {
                    "text": "00000000:45:00.0"
                },
                "pci_sub_system_id": {
                    "text": "38841462"
                },
                "pci_gpu_link_info": {
                    "pcie_gen": {
                        "max_link_gen": {
                            "text": "4"
                        },
                        "current_link_gen": {
                            "text": "1"
                        },
                        "device_current_link_gen": {
                            "text": "1"
                        },
                        "max_device_link_gen": {
                            "text": "4"
                        },
                        "max_host_link_gen": {
                            "text": "4"
                        }
                    },
                    "link_widths": {
                        "max_link_width": {
                            "text": "16x"
                        },
                        "current_link_width": {
                            "text": "16x"
                        }
                    }
                },
                "pci_bridge_chip": {
                    "bridge_chip_type": {
                        "text": "N/A"
                    },
                    "bridge_chip_fw": {
                        "text": "N/A"
                    }
                },
                "replay_counter": {
                    "text": "0"
                },
                "replay_rollover_counter": {
                    "text": "0"
                },
                "tx_util": {
                    "text": "0 KB/s"
                },
                "rx_util": {
                    "text": "0 KB/s"
                },
                "atomic_caps_inbound": {
                    "text": "N/A"
                },
                "atomic_caps_outbound": {
                    "text": "N/A"
                }
            },
            "fan_speed": {
                "text": "0 %"
            },
            "performance_state": {
                "text": "P8"
            },
            "clocks_event_reasons": {
                "clocks_event_reason_gpu_idle": {
                    "text": "Active"
                },
                "clocks_event_reason_applications_clocks_setting": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_power_cap": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_power_brake_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sync_boost": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_display_clocks_setting": {
                    "text": "Not Active"
                }
            },
            "sparse_operation_mode": {
                "text": "N/A"
            },
            "fb_memory_usage": {
                "total": {
                    "text": "24576 MiB"
                },
                "reserved": {
                    "text": "323 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "24248 MiB"
                }
            },
            "bar1_memory_usage": {
                "total": {
                    "text": "256 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "253 MiB"
                }
            },
            "cc_protected_memory_usage": {
                "total": {
                    "text": "0 MiB"
                },
                "used": {
                    "text": "0 MiB"
                },
                "free": {
                    "text": "0 MiB"
                }
            },
            "compute_mode": {
                "text": "Default"
            },
            "utilization": {
                "gpu_util": {
                    "text": "0 %"
                },
                "memory_util": {
                    "text": "0 %"
                },
                "encoder_util": {
                    "text": "0 %"
                },
                "decoder_util": {
                    "text": "0 %"
                },
                "jpeg_util": {
                    "text": "0 %"
                },
                "ofa_util": {
                    "text": "0 %"
                }
            },
            "encoder_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "fbc_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "ecc_mode": {
                "current_ecc": {
                    "text": "N/A"
                },
                "pending_ecc": {
                    "text": "N/A"
                }
            },
            "ecc_errors": {
                "volatile": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    }
                },
                "aggregate": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    },
                    "sram_threshold_exceeded": {
                        "text": "N/A"
                    }
                },
                "aggregate_uncorrectable_sram_sources": {
                    "sram_l2": {
                        "text": "N/A"
                    },
                    "sram_sm": {
                        "text": "N/A"
                    },
                    "sram_microcontroller": {
                        "text": "N/A"
                    },
                    "sram_pcie": {
                        "text": "N/A"
                    },
                    "sram_other": {
                        "text": "N/A"
                    }
                }
            },
            "retired_pages": {
                "multiple_single_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "double_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "pending_blacklist": {
                    "text": "N/A"
                },
                "pending_retirement": {
                    "text": "N/A"
                }
            },
            "remapped_rows": {
                "text": "N/A"
            },
            "temperature": {
                "gpu_temp": {
                    "text": "34 C"
                },
                "gpu_temp_tlimit": {
                    "text": "N/A"
                },
                "gpu_temp_max_threshold": {
                    "text": "98 C"
                },
                "gpu_temp_slow_threshold": {
                    "text": "95 C"
                },
                "gpu_temp_max_gpu_threshold": {
                    "text": "93 C"
                },
                "gpu_target_temperature": {
                    "text": "83 C"
                },
                "memory_temp": {
                    "text": "N/A"
                },
                "gpu_temp_max_mem_threshold": {
                    "text": "N/A"
                }
            },
            "supported_gpu_target_temp": {
                "gpu_target_temp_min": {
                    "text": "65 C"
                },
                "gpu_target_temp_max": {
                    "text": "91 C"
                }
            },
            "gpu_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "21.28 W"
                },
                "current_power_limit": {
                    "text": "300.00 W"
                },
                "requested_power_limit": {
                    "text": "300.00 W"
                },
                "default_power_limit": {
                    "text": "370.00 W"
                },
                "min_power_limit": {
                    "text": "100.00 W"
                },
                "max_power_limit": {
                    "text": "380.00 W"
                }
            },
            "gpu_memory_power_readings": {
                "power_draw": {
                    "text": "N/A"
                }
            },
            "module_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "N/A"
                },
                "current_power_limit": {
                    "text": "N/A"
                },
                "requested_power_limit": {
                    "text": "N/A"
                },
                "default_power_limit": {
                    "text": "N/A"
                },
                "min_power_limit": {
                    "text": "N/A"
                },
                "max_power_limit": {
                    "text": "N/A"
                }
            },
            "clocks": {
                "graphics_clock": {
                    "text": "300 MHz"
                },
                "sm_clock": {
                    "text": "300 MHz"
                },
                "mem_clock": {
                    "text": "405 MHz"
                },
                "video_clock": {
                    "text": "555 MHz"
                }
            },
            "applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "default_applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "deferred_clocks": {
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "max_clocks": {
                "graphics_clock": {
                    "text": "2115 MHz"
                },
                "sm_clock": {
                    "text": "2115 MHz"
                },
                "mem_clock": {
                    "text": "9751 MHz"
                },
                "video_clock": {
                    "text": "1950 MHz"
                }
            },
            "max_customer_boost_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                }
            },
            "clock_policy": {
                "auto_boost": {
                    "text": "N/A"
                },
                "auto_boost_default": {
                    "text": "N/A"
                }
            },
            "voltage": {
                "graphics_volt": {
                    "text": "737.500 mV"
                }
            },
            "fabric": {
                "state": {
                    "text": "N/A"
                },
                "status": {
                    "text": "N/A"
                },
                "cliqueId": {
                    "text": "N/A"
                },
                "clusterUuid": {
                    "text": "N/A"
                },
                "health": {
                    "bandwidth": {
                        "text": "N/A"
                    }
                }
            },
            "supported_clocks": {
                "supported_mem_clock": [
                    {
                        "value": {
                            "text": "9751 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "9501 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "5001 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "810 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "405 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    }
                ]
            },
            "processes": {},
            "accounted_processes": {}
        },
        {
            "product_name": {
                "text": "NVIDIA GeForce RTX 3090"
            },
            "product_brand": {
                "text": "GeForce"
            },
            "product_architecture": {
                "text": "Ampere"
            },
            "display_mode": {
                "text": "Disabled"
            },
            "display_active": {
                "text": "Disabled"
            },
            "persistence_mode": {
                "text": "Enabled"
            },
            "addressing_mode": {
                "text": "None"
            },
            "mig_mode": {
                "current_mig": {
                    "text": "N/A"
                },
                "pending_mig": {
                    "text": "N/A"
                }
            },
            "mig_devices": {
                "text": "None"
            },
            "accounting_mode": {
                "text": "Disabled"
            },
            "accounting_mode_buffer_size": {
                "text": "4000"
            },
            "driver_model": {
                "current_dm": {
                    "text": "N/A"
                },
                "pending_dm": {
                    "text": "N/A"
                }
            },
            "serial": {
                "text": "N/A"
            },
            "uuid": {
                "text": "GPU-6a236775-624a-2c84-38fd-451c90ab3679"
            },
            "minor_number": {
                "text": "1"
            },
            "vbios_version": {
                "text": "94.02.42.C0.10"
            },
            "multigpu_board": {
                "text": "No"
            },
            "board_id": {
                "text": "0x8100"
            },
            "board_part_number": {
                "text": "N/A"
            },
            "gpu_part_number": {
                "text": "2204-300-A1"
            },
            "gpu_fru_part_number": {
                "text": "N/A"
            },
            "gpu_module_id": {
                "text": "1"
            },
            "inforom_version": {
                "img_version": {
                    "text": "G001.0000.03.03"
                },
                "oem_object": {
                    "text": "2.0"
                },
                "ecc_object": {
                    "text": "N/A"
                },
                "pwr_object": {
                    "text": "N/A"
                }
            },
            "inforom_bbx_flush": {
                "latest_timestamp": {
                    "text": "N/A"
                },
                "latest_duration": {
                    "text": "N/A"
                }
            },
            "gpu_operation_mode": {
                "current_gom": {
                    "text": "N/A"
                },
                "pending_gom": {
                    "text": "N/A"
                }
            },
            "c2c_mode": {
                "text": "N/A"
            },
            "gpu_virtualization_mode": {
                "virtualization_mode": {
                    "text": "None"
                },
                "host_vgpu_mode": {
                    "text": "N/A"
                },
                "vgpu_heterogeneous_mode": {
                    "text": "N/A"
                }
            },
            "gpu_reset_status": {
                "reset_required": {
                    "text": "No"
                },
                "drain_and_reset_recommended": {
                    "text": "N/A"
                }
            },
            "gsp_firmware_version": {
                "text": "N/A"
            },
            "ibmnpu": {
                "relaxed_ordering_mode": {
                    "text": "N/A"
                }
            },
            "pci": {
                "pci_bus": {
                    "text": "81"
                },
                "pci_device": {
                    "text": "00"
                },
                "pci_domain": {
                    "text": "0000"
                },
                "pci_base_class": {
                    "text": "3"
                },
                "pci_sub_class": {
                    "text": "0"
                },
                "pci_device_id": {
                    "text": "220410DE"
                },
                "pci_bus_id": {
                    "text": "00000000:81:00.0"
                },
                "pci_sub_system_id": {
                    "text": "39753842"
                },
                "pci_gpu_link_info": {
                    "pcie_gen": {
                        "max_link_gen": {
                            "text": "4"
                        },
                        "current_link_gen": {
                            "text": "1"
                        },
                        "device_current_link_gen": {
                            "text": "1"
                        },
                        "max_device_link_gen": {
                            "text": "4"
                        },
                        "max_host_link_gen": {
                            "text": "4"
                        }
                    },
                    "link_widths": {
                        "max_link_width": {
                            "text": "16x"
                        },
                        "current_link_width": {
                            "text": "16x"
                        }
                    }
                },
                "pci_bridge_chip": {
                    "bridge_chip_type": {
                        "text": "N/A"
                    },
                    "bridge_chip_fw": {
                        "text": "N/A"
                    }
                },
                "replay_counter": {
                    "text": "0"
                },
                "replay_rollover_counter": {
                    "text": "0"
                },
                "tx_util": {
                    "text": "0 KB/s"
                },
                "rx_util": {
                    "text": "0 KB/s"
                },
                "atomic_caps_inbound": {
                    "text": "N/A"
                },
                "atomic_caps_outbound": {
                    "text": "N/A"
                }
            },
            "fan_speed": {
                "text": "0 %"
            },
            "performance_state": {
                "text": "P8"
            },
            "clocks_event_reasons": {
                "clocks_event_reason_gpu_idle": {
                    "text": "Active"
                },
                "clocks_event_reason_applications_clocks_setting": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_power_cap": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_power_brake_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sync_boost": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_display_clocks_setting": {
                    "text": "Not Active"
                }
            },
            "sparse_operation_mode": {
                "text": "N/A"
            },
            "fb_memory_usage": {
                "total": {
                    "text": "24576 MiB"
                },
                "reserved": {
                    "text": "323 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "24248 MiB"
                }
            },
            "bar1_memory_usage": {
                "total": {
                    "text": "256 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "253 MiB"
                }
            },
            "cc_protected_memory_usage": {
                "total": {
                    "text": "0 MiB"
                },
                "used": {
                    "text": "0 MiB"
                },
                "free": {
                    "text": "0 MiB"
                }
            },
            "compute_mode": {
                "text": "Default"
            },
            "utilization": {
                "gpu_util": {
                    "text": "0 %"
                },
                "memory_util": {
                    "text": "0 %"
                },
                "encoder_util": {
                    "text": "0 %"
                },
                "decoder_util": {
                    "text": "0 %"
                },
                "jpeg_util": {
                    "text": "0 %"
                },
                "ofa_util": {
                    "text": "0 %"
                }
            },
            "encoder_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "fbc_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "ecc_mode": {
                "current_ecc": {
                    "text": "N/A"
                },
                "pending_ecc": {
                    "text": "N/A"
                }
            },
            "ecc_errors": {
                "volatile": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    }
                },
                "aggregate": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    },
                    "sram_threshold_exceeded": {
                        "text": "N/A"
                    }
                },
                "aggregate_uncorrectable_sram_sources": {
                    "sram_l2": {
                        "text": "N/A"
                    },
                    "sram_sm": {
                        "text": "N/A"
                    },
                    "sram_microcontroller": {
                        "text": "N/A"
                    },
                    "sram_pcie": {
                        "text": "N/A"
                    },
                    "sram_other": {
                        "text": "N/A"
                    }
                }
            },
            "retired_pages": {
                "multiple_single_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "double_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "pending_blacklist": {
                    "text": "N/A"
                },
                "pending_retirement": {
                    "text": "N/A"
                }
            },
            "remapped_rows": {
                "text": "N/A"
            },
            "temperature": {
                "gpu_temp": {
                    "text": "37 C"
                },
                "gpu_temp_tlimit": {
                    "text": "N/A"
                },
                "gpu_temp_max_threshold": {
                    "text": "98 C"
                },
                "gpu_temp_slow_threshold": {
                    "text": "95 C"
                },
                "gpu_temp_max_gpu_threshold": {
                    "text": "93 C"
                },
                "gpu_target_temperature": {
                    "text": "83 C"
                },
                "memory_temp": {
                    "text": "N/A"
                },
                "gpu_temp_max_mem_threshold": {
                    "text": "N/A"
                }
            },
            "supported_gpu_target_temp": {
                "gpu_target_temp_min": {
                    "text": "65 C"
                },
                "gpu_target_temp_max": {
                    "text": "91 C"
                }
            },
            "gpu_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "39.38 W"
                },
                "current_power_limit": {
                    "text": "300.00 W"
                },
                "requested_power_limit": {
                    "text": "300.00 W"
                },
                "default_power_limit": {
                    "text": "350.00 W"
                },
                "min_power_limit": {
                    "text": "100.00 W"
                },
                "max_power_limit": {
                    "text": "366.00 W"
                }
            },
            "gpu_memory_power_readings": {
                "power_draw": {
                    "text": "N/A"
                }
            },
            "module_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "N/A"
                },
                "current_power_limit": {
                    "text": "N/A"
                },
                "requested_power_limit": {
                    "text": "N/A"
                },
                "default_power_limit": {
                    "text": "N/A"
                },
                "min_power_limit": {
                    "text": "N/A"
                },
                "max_power_limit": {
                    "text": "N/A"
                }
            },
            "clocks": {
                "graphics_clock": {
                    "text": "300 MHz"
                },
                "sm_clock": {
                    "text": "300 MHz"
                },
                "mem_clock": {
                    "text": "405 MHz"
                },
                "video_clock": {
                    "text": "555 MHz"
                }
            },
            "applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "default_applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "deferred_clocks": {
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "max_clocks": {
                "graphics_clock": {
                    "text": "2130 MHz"
                },
                "sm_clock": {
                    "text": "2130 MHz"
                },
                "mem_clock": {
                    "text": "9751 MHz"
                },
                "video_clock": {
                    "text": "1950 MHz"
                }
            },
            "max_customer_boost_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                }
            },
            "clock_policy": {
                "auto_boost": {
                    "text": "N/A"
                },
                "auto_boost_default": {
                    "text": "N/A"
                }
            },
            "voltage": {
                "graphics_volt": {
                    "text": "743.750 mV"
                }
            },
            "fabric": {
                "state": {
                    "text": "N/A"
                },
                "status": {
                    "text": "N/A"
                },
                "cliqueId": {
                    "text": "N/A"
                },
                "clusterUuid": {
                    "text": "N/A"
                },
                "health": {
                    "bandwidth": {
                        "text": "N/A"
                    }
                }
            },
            "supported_clocks": {
                "supported_mem_clock": [
                    {
                        "value": {
                            "text": "9751 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2130 MHz"
                            },
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "9501 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2130 MHz"
                            },
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "5001 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2130 MHz"
                            },
                            {
                                "text": "2115 MHz"
                            },
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "810 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "405 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    }
                ]
            },
            "processes": {},
            "accounted_processes": {}
        },
        {
            "product_name": {
                "text": "NVIDIA GeForce RTX 3090"
            },
            "product_brand": {
                "text": "GeForce"
            },
            "product_architecture": {
                "text": "Ampere"
            },
            "display_mode": {
                "text": "Disabled"
            },
            "display_active": {
                "text": "Disabled"
            },
            "persistence_mode": {
                "text": "Enabled"
            },
            "addressing_mode": {
                "text": "None"
            },
            "mig_mode": {
                "current_mig": {
                    "text": "N/A"
                },
                "pending_mig": {
                    "text": "N/A"
                }
            },
            "mig_devices": {
                "text": "None"
            },
            "accounting_mode": {
                "text": "Disabled"
            },
            "accounting_mode_buffer_size": {
                "text": "4000"
            },
            "driver_model": {
                "current_dm": {
                    "text": "N/A"
                },
                "pending_dm": {
                    "text": "N/A"
                }
            },
            "serial": {
                "text": "N/A"
            },
            "uuid": {
                "text": "GPU-cfa52b35-b988-42cb-3791-a901ce72ef52"
            },
            "minor_number": {
                "text": "0"
            },
            "vbios_version": {
                "text": "94.02.42.C0.05"
            },
            "multigpu_board": {
                "text": "No"
            },
            "board_id": {
                "text": "0xc100"
            },
            "board_part_number": {
                "text": "N/A"
            },
            "gpu_part_number": {
                "text": "2204-300-A1"
            },
            "gpu_fru_part_number": {
                "text": "N/A"
            },
            "gpu_module_id": {
                "text": "1"
            },
            "inforom_version": {
                "img_version": {
                    "text": "G001.0000.03.03"
                },
                "oem_object": {
                    "text": "2.0"
                },
                "ecc_object": {
                    "text": "N/A"
                },
                "pwr_object": {
                    "text": "N/A"
                }
            },
            "inforom_bbx_flush": {
                "latest_timestamp": {
                    "text": "N/A"
                },
                "latest_duration": {
                    "text": "N/A"
                }
            },
            "gpu_operation_mode": {
                "current_gom": {
                    "text": "N/A"
                },
                "pending_gom": {
                    "text": "N/A"
                }
            },
            "c2c_mode": {
                "text": "N/A"
            },
            "gpu_virtualization_mode": {
                "virtualization_mode": {
                    "text": "None"
                },
                "host_vgpu_mode": {
                    "text": "N/A"
                },
                "vgpu_heterogeneous_mode": {
                    "text": "N/A"
                }
            },
            "gpu_reset_status": {
                "reset_required": {
                    "text": "No"
                },
                "drain_and_reset_recommended": {
                    "text": "N/A"
                }
            },
            "gsp_firmware_version": {
                "text": "N/A"
            },
            "ibmnpu": {
                "relaxed_ordering_mode": {
                    "text": "N/A"
                }
            },
            "pci": {
                "pci_bus": {
                    "text": "C1"
                },
                "pci_device": {
                    "text": "00"
                },
                "pci_domain": {
                    "text": "0000"
                },
                "pci_base_class": {
                    "text": "3"
                },
                "pci_sub_class": {
                    "text": "0"
                },
                "pci_device_id": {
                    "text": "220410DE"
                },
                "pci_bus_id": {
                    "text": "00000000:C1:00.0"
                },
                "pci_sub_system_id": {
                    "text": "39823842"
                },
                "pci_gpu_link_info": {
                    "pcie_gen": {
                        "max_link_gen": {
                            "text": "4"
                        },
                        "current_link_gen": {
                            "text": "1"
                        },
                        "device_current_link_gen": {
                            "text": "1"
                        },
                        "max_device_link_gen": {
                            "text": "4"
                        },
                        "max_host_link_gen": {
                            "text": "4"
                        }
                    },
                    "link_widths": {
                        "max_link_width": {
                            "text": "16x"
                        },
                        "current_link_width": {
                            "text": "16x"
                        }
                    }
                },
                "pci_bridge_chip": {
                    "bridge_chip_type": {
                        "text": "N/A"
                    },
                    "bridge_chip_fw": {
                        "text": "N/A"
                    }
                },
                "replay_counter": {
                    "text": "0"
                },
                "replay_rollover_counter": {
                    "text": "0"
                },
                "tx_util": {
                    "text": "0 KB/s"
                },
                "rx_util": {
                    "text": "0 KB/s"
                },
                "atomic_caps_inbound": {
                    "text": "N/A"
                },
                "atomic_caps_outbound": {
                    "text": "N/A"
                }
            },
            "fan_speed": {
                "text": "0 %"
            },
            "performance_state": {
                "text": "P8"
            },
            "clocks_event_reasons": {
                "clocks_event_reason_gpu_idle": {
                    "text": "Active"
                },
                "clocks_event_reason_applications_clocks_setting": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_power_cap": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_hw_power_brake_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sync_boost": {
                    "text": "Not Active"
                },
                "clocks_event_reason_sw_thermal_slowdown": {
                    "text": "Not Active"
                },
                "clocks_event_reason_display_clocks_setting": {
                    "text": "Not Active"
                }
            },
            "sparse_operation_mode": {
                "text": "N/A"
            },
            "fb_memory_usage": {
                "total": {
                    "text": "24576 MiB"
                },
                "reserved": {
                    "text": "323 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "24248 MiB"
                }
            },
            "bar1_memory_usage": {
                "total": {
                    "text": "256 MiB"
                },
                "used": {
                    "text": "3 MiB"
                },
                "free": {
                    "text": "253 MiB"
                }
            },
            "cc_protected_memory_usage": {
                "total": {
                    "text": "0 MiB"
                },
                "used": {
                    "text": "0 MiB"
                },
                "free": {
                    "text": "0 MiB"
                }
            },
            "compute_mode": {
                "text": "Default"
            },
            "utilization": {
                "gpu_util": {
                    "text": "0 %"
                },
                "memory_util": {
                    "text": "0 %"
                },
                "encoder_util": {
                    "text": "0 %"
                },
                "decoder_util": {
                    "text": "0 %"
                },
                "jpeg_util": {
                    "text": "0 %"
                },
                "ofa_util": {
                    "text": "0 %"
                }
            },
            "encoder_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "fbc_stats": {
                "session_count": {
                    "text": "0"
                },
                "average_fps": {
                    "text": "0"
                },
                "average_latency": {
                    "text": "0"
                }
            },
            "ecc_mode": {
                "current_ecc": {
                    "text": "N/A"
                },
                "pending_ecc": {
                    "text": "N/A"
                }
            },
            "ecc_errors": {
                "volatile": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    }
                },
                "aggregate": {
                    "sram_correctable": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_parity": {
                        "text": "N/A"
                    },
                    "sram_uncorrectable_secded": {
                        "text": "N/A"
                    },
                    "dram_correctable": {
                        "text": "N/A"
                    },
                    "dram_uncorrectable": {
                        "text": "N/A"
                    },
                    "sram_threshold_exceeded": {
                        "text": "N/A"
                    }
                },
                "aggregate_uncorrectable_sram_sources": {
                    "sram_l2": {
                        "text": "N/A"
                    },
                    "sram_sm": {
                        "text": "N/A"
                    },
                    "sram_microcontroller": {
                        "text": "N/A"
                    },
                    "sram_pcie": {
                        "text": "N/A"
                    },
                    "sram_other": {
                        "text": "N/A"
                    }
                }
            },
            "retired_pages": {
                "multiple_single_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "double_bit_retirement": {
                    "retired_count": {
                        "text": "N/A"
                    },
                    "retired_pagelist": {
                        "text": "N/A"
                    }
                },
                "pending_blacklist": {
                    "text": "N/A"
                },
                "pending_retirement": {
                    "text": "N/A"
                }
            },
            "remapped_rows": {
                "text": "N/A"
            },
            "temperature": {
                "gpu_temp": {
                    "text": "49 C"
                },
                "gpu_temp_tlimit": {
                    "text": "N/A"
                },
                "gpu_temp_max_threshold": {
                    "text": "98 C"
                },
                "gpu_temp_slow_threshold": {
                    "text": "95 C"
                },
                "gpu_temp_max_gpu_threshold": {
                    "text": "93 C"
                },
                "gpu_target_temperature": {
                    "text": "83 C"
                },
                "memory_temp": {
                    "text": "N/A"
                },
                "gpu_temp_max_mem_threshold": {
                    "text": "N/A"
                }
            },
            "supported_gpu_target_temp": {
                "gpu_target_temp_min": {
                    "text": "65 C"
                },
                "gpu_target_temp_max": {
                    "text": "91 C"
                }
            },
            "gpu_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "57.97 W"
                },
                "current_power_limit": {
                    "text": "300.00 W"
                },
                "requested_power_limit": {
                    "text": "300.00 W"
                },
                "default_power_limit": {
                    "text": "420.00 W"
                },
                "min_power_limit": {
                    "text": "100.00 W"
                },
                "max_power_limit": {
                    "text": "450.00 W"
                }
            },
            "gpu_memory_power_readings": {
                "power_draw": {
                    "text": "N/A"
                }
            },
            "module_power_readings": {
                "power_state": {
                    "text": "P8"
                },
                "power_draw": {
                    "text": "N/A"
                },
                "current_power_limit": {
                    "text": "N/A"
                },
                "requested_power_limit": {
                    "text": "N/A"
                },
                "default_power_limit": {
                    "text": "N/A"
                },
                "min_power_limit": {
                    "text": "N/A"
                },
                "max_power_limit": {
                    "text": "N/A"
                }
            },
            "clocks": {
                "graphics_clock": {
                    "text": "300 MHz"
                },
                "sm_clock": {
                    "text": "300 MHz"
                },
                "mem_clock": {
                    "text": "405 MHz"
                },
                "video_clock": {
                    "text": "555 MHz"
                }
            },
            "applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "default_applications_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                },
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "deferred_clocks": {
                "mem_clock": {
                    "text": "N/A"
                }
            },
            "max_clocks": {
                "graphics_clock": {
                    "text": "2100 MHz"
                },
                "sm_clock": {
                    "text": "2100 MHz"
                },
                "mem_clock": {
                    "text": "9751 MHz"
                },
                "video_clock": {
                    "text": "1950 MHz"
                }
            },
            "max_customer_boost_clocks": {
                "graphics_clock": {
                    "text": "N/A"
                }
            },
            "clock_policy": {
                "auto_boost": {
                    "text": "N/A"
                },
                "auto_boost_default": {
                    "text": "N/A"
                }
            },
            "voltage": {
                "graphics_volt": {
                    "text": "725.000 mV"
                }
            },
            "fabric": {
                "state": {
                    "text": "N/A"
                },
                "status": {
                    "text": "N/A"
                },
                "cliqueId": {
                    "text": "N/A"
                },
                "clusterUuid": {
                    "text": "N/A"
                },
                "health": {
                    "bandwidth": {
                        "text": "N/A"
                    }
                }
            },
            "supported_clocks": {
                "supported_mem_clock": [
                    {
                        "value": {
                            "text": "9751 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "9501 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "5001 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "810 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "2100 MHz"
                            },
                            {
                                "text": "2085 MHz"
                            },
                            {
                                "text": "2070 MHz"
                            },
                            {
                                "text": "2055 MHz"
                            },
                            {
                                "text": "2040 MHz"
                            },
                            {
                                "text": "2025 MHz"
                            },
                            {
                                "text": "2010 MHz"
                            },
                            {
                                "text": "1995 MHz"
                            },
                            {
                                "text": "1980 MHz"
                            },
                            {
                                "text": "1965 MHz"
                            },
                            {
                                "text": "1950 MHz"
                            },
                            {
                                "text": "1935 MHz"
                            },
                            {
                                "text": "1920 MHz"
                            },
                            {
                                "text": "1905 MHz"
                            },
                            {
                                "text": "1890 MHz"
                            },
                            {
                                "text": "1875 MHz"
                            },
                            {
                                "text": "1860 MHz"
                            },
                            {
                                "text": "1845 MHz"
                            },
                            {
                                "text": "1830 MHz"
                            },
                            {
                                "text": "1815 MHz"
                            },
                            {
                                "text": "1800 MHz"
                            },
                            {
                                "text": "1785 MHz"
                            },
                            {
                                "text": "1770 MHz"
                            },
                            {
                                "text": "1755 MHz"
                            },
                            {
                                "text": "1740 MHz"
                            },
                            {
                                "text": "1725 MHz"
                            },
                            {
                                "text": "1710 MHz"
                            },
                            {
                                "text": "1695 MHz"
                            },
                            {
                                "text": "1680 MHz"
                            },
                            {
                                "text": "1665 MHz"
                            },
                            {
                                "text": "1650 MHz"
                            },
                            {
                                "text": "1635 MHz"
                            },
                            {
                                "text": "1620 MHz"
                            },
                            {
                                "text": "1605 MHz"
                            },
                            {
                                "text": "1590 MHz"
                            },
                            {
                                "text": "1575 MHz"
                            },
                            {
                                "text": "1560 MHz"
                            },
                            {
                                "text": "1545 MHz"
                            },
                            {
                                "text": "1530 MHz"
                            },
                            {
                                "text": "1515 MHz"
                            },
                            {
                                "text": "1500 MHz"
                            },
                            {
                                "text": "1485 MHz"
                            },
                            {
                                "text": "1470 MHz"
                            },
                            {
                                "text": "1455 MHz"
                            },
                            {
                                "text": "1440 MHz"
                            },
                            {
                                "text": "1425 MHz"
                            },
                            {
                                "text": "1410 MHz"
                            },
                            {
                                "text": "1395 MHz"
                            },
                            {
                                "text": "1380 MHz"
                            },
                            {
                                "text": "1365 MHz"
                            },
                            {
                                "text": "1350 MHz"
                            },
                            {
                                "text": "1335 MHz"
                            },
                            {
                                "text": "1320 MHz"
                            },
                            {
                                "text": "1305 MHz"
                            },
                            {
                                "text": "1290 MHz"
                            },
                            {
                                "text": "1275 MHz"
                            },
                            {
                                "text": "1260 MHz"
                            },
                            {
                                "text": "1245 MHz"
                            },
                            {
                                "text": "1230 MHz"
                            },
                            {
                                "text": "1215 MHz"
                            },
                            {
                                "text": "1200 MHz"
                            },
                            {
                                "text": "1185 MHz"
                            },
                            {
                                "text": "1170 MHz"
                            },
                            {
                                "text": "1155 MHz"
                            },
                            {
                                "text": "1140 MHz"
                            },
                            {
                                "text": "1125 MHz"
                            },
                            {
                                "text": "1110 MHz"
                            },
                            {
                                "text": "1095 MHz"
                            },
                            {
                                "text": "1080 MHz"
                            },
                            {
                                "text": "1065 MHz"
                            },
                            {
                                "text": "1050 MHz"
                            },
                            {
                                "text": "1035 MHz"
                            },
                            {
                                "text": "1020 MHz"
                            },
                            {
                                "text": "1005 MHz"
                            },
                            {
                                "text": "990 MHz"
                            },
                            {
                                "text": "975 MHz"
                            },
                            {
                                "text": "960 MHz"
                            },
                            {
                                "text": "945 MHz"
                            },
                            {
                                "text": "930 MHz"
                            },
                            {
                                "text": "915 MHz"
                            },
                            {
                                "text": "900 MHz"
                            },
                            {
                                "text": "885 MHz"
                            },
                            {
                                "text": "870 MHz"
                            },
                            {
                                "text": "855 MHz"
                            },
                            {
                                "text": "840 MHz"
                            },
                            {
                                "text": "825 MHz"
                            },
                            {
                                "text": "810 MHz"
                            },
                            {
                                "text": "795 MHz"
                            },
                            {
                                "text": "780 MHz"
                            },
                            {
                                "text": "765 MHz"
                            },
                            {
                                "text": "750 MHz"
                            },
                            {
                                "text": "735 MHz"
                            },
                            {
                                "text": "720 MHz"
                            },
                            {
                                "text": "705 MHz"
                            },
                            {
                                "text": "690 MHz"
                            },
                            {
                                "text": "675 MHz"
                            },
                            {
                                "text": "660 MHz"
                            },
                            {
                                "text": "645 MHz"
                            },
                            {
                                "text": "630 MHz"
                            },
                            {
                                "text": "615 MHz"
                            },
                            {
                                "text": "600 MHz"
                            },
                            {
                                "text": "585 MHz"
                            },
                            {
                                "text": "570 MHz"
                            },
                            {
                                "text": "555 MHz"
                            },
                            {
                                "text": "540 MHz"
                            },
                            {
                                "text": "525 MHz"
                            },
                            {
                                "text": "510 MHz"
                            },
                            {
                                "text": "495 MHz"
                            },
                            {
                                "text": "480 MHz"
                            },
                            {
                                "text": "465 MHz"
                            },
                            {
                                "text": "450 MHz"
                            },
                            {
                                "text": "435 MHz"
                            },
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    },
                    {
                        "value": {
                            "text": "405 MHz"
                        },
                        "supported_graphics_clock": [
                            {
                                "text": "420 MHz"
                            },
                            {
                                "text": "405 MHz"
                            },
                            {
                                "text": "390 MHz"
                            },
                            {
                                "text": "375 MHz"
                            },
                            {
                                "text": "360 MHz"
                            },
                            {
                                "text": "345 MHz"
                            },
                            {
                                "text": "330 MHz"
                            },
                            {
                                "text": "315 MHz"
                            },
                            {
                                "text": "300 MHz"
                            },
                            {
                                "text": "285 MHz"
                            },
                            {
                                "text": "270 MHz"
                            },
                            {
                                "text": "255 MHz"
                            },
                            {
                                "text": "240 MHz"
                            },
                            {
                                "text": "225 MHz"
                            },
                            {
                                "text": "210 MHz"
                            }
                        ]
                    }
                ]
            },
            "processes": {},
            "accounted_processes": {}
        }
    ]
}
