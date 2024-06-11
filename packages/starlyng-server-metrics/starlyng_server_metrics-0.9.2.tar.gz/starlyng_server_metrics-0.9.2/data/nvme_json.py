"""
nvme json response
"""
from typing import Dict

nvme_json_dict: Dict[str, str] = {
    "critical_warning": 0, 
    "temperature": 308,
    "avail_spare": 100,
    "spare_thresh": 10,
    "percent_used": 0,
    "endurance_grp_critical_warning_summary": 0,
    "data_units_read": 9486678,
    "data_units_written": 8437019,
    "host_read_commands": 103027886,
    "host_write_commands": 64802657,
    "controller_busy_time": 388,
    "power_cycles": 22,
    "power_on_hours": 393,
    "unsafe_shutdowns": 14,
    "media_errors": 0,
    "num_err_log_entries": 0,
    "warning_temp_time": 0,
    "critical_comp_time": 0,
    "temperature_sensor_1": 308,
    "temperature_sensor_2": 312,
    "thm_temp1_trans_count": 0,
    "thm_temp2_trans_count": 0,
    "thm_temp1_total_time": 0,
    "thm_temp2_total_time": 0
}
