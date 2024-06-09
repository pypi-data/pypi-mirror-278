"""
sensors json response for amd cpu
"""
from typing import Dict

cpu_intel_json_dict: Dict[str, str] = {
    'coretemp-isa-0000': {
        'Adapter': 'ISA adapter',
        'Package id 0': {
            'temp1_input': 44.0,
            'temp1_max': 82.0,
            'temp1_crit': 100.0,
            'temp1_crit_alarm': 0.0
        },
        'Core 0': {
            'temp2_input': 43.0,
            'temp2_max': 82.0,
            'temp2_crit': 100.0,
            'temp2_crit_alarm': 0.0
        },
        'Core 1': {
            'temp3_input': 42.0,
            'temp3_max': 82.0,
            'temp3_crit': 100.0,
            'temp3_crit_alarm': 0.0
        },
        'Core 2': {
            'temp4_input': 44.0,
            'temp4_max': 82.0,
            'temp4_crit': 100.0,
            'temp4_crit_alarm': 0.0
        },
        'Core 3': {
            'temp5_input': 43.0,
            'temp5_max': 82.0,
            'temp5_crit': 100.0,
            'temp5_crit_alarm': 0.0
        },
        'Core 4': {
            'temp6_input': 42.0,
            'temp6_max': 82.0,
            'temp6_crit': 100.0,
            'temp6_crit_alarm': 0.0
        },
        'Core 5': {
            'temp7_input': 43.0,
            'temp7_max': 82.0,
            'temp7_crit': 100.0,
            'temp7_crit_alarm': 0.0
        },
        'Core 6': {
            'temp8_input': 42.0,
            'temp8_max': 82.0,
            'temp8_crit': 100.0,
            'temp8_crit_alarm': 0.0
        },
        'Core 7': {
            'temp9_input': 42.0,
            'temp9_max': 82.0,
            'temp9_crit': 100.0,
            'temp9_crit_alarm': 0.0
        },
        'Core 8': {
            'temp10_input': 42.0,
            'temp10_max': 82.0,
            'temp10_crit': 100.0,
            'temp10_crit_alarm': 0.0
        },
        'Core 9': {
            'temp11_input': 43.0,
            'temp11_max': 82.0,
            'temp11_crit': 100.0,
            'temp11_crit_alarm': 0.0
        }
    },
    'acpitz-acpi-0': {
        'Adapter': 'ACPI interface',
        'temp1': {
            'temp1_input': 27.8,
            'temp1_crit': 105.0
        }
    },
    'iwlwifi_1-virtual-0': {
        'Adapter': 'Virtual device',
        'temp1': {

        }
    },
    'nvme-pci-0800': {
        'Adapter': 'PCI adapter',
        'Composite': {
            'temp1_input': 44.85,
            'temp1_max': 81.85,
            'temp1_min': -273.15,
            'temp1_crit': 84.85,
            'temp1_alarm': 0.0
        },
        'Sensor 1': {
            'temp2_input': 44.85,
            'temp2_max': 65261.85,
            'temp2_min': -273.15
        },
        'Sensor 2': {
            'temp3_input': 47.85,
            'temp3_max': 65261.85,
            'temp3_min': -273.15
        }
    }
}
