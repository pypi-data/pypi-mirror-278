# """
# Testing for gpu_collector module
# """
# from unittest.mock import patch, MagicMock
# from server_metrics.collectors.gpu_collector import run_nvidia_smi
# from server_metrics.utils.xml_parser import xml_to_json
# from server_metrics.utils.parse_gpu_json import parse_gpu_json_to_dict
# from server_metrics.utils.prom_gpu import create_gpu_prom_file

# # Mock data for the tests
# mock_ip = "192.168.1.1"
# mock_port = 22
# mock_key_path = "/path/to/key"
# mock_username = "user"
# mock_gpu_xml = "<nvidia_smi_log><attached_gpus>1</attached_gpus><gpu><product_name>Test GPU</product_name></gpu></nvidia_smi_log>"
# mock_gpu_json = {"attached_gpus": {"text": "1"}, "gpu": {"product_name": {"text": "Test GPU"}}}
# mock_gpu_dict = {0: {"product_name": "Test GPU"}}  # Adjust this according to the Gpu class implementation

# def test_run_nvidia_smi_success(mocker):
#     with patch('subprocess.run') as mocked_run:
#         # Mock the subprocess run method
#         mocked_result = MagicMock()
#         mocked_result.stdout = mock_gpu_xml
#         mocked_result.stderr = ""
#         mocked_run.return_value = mocked_result

#         # Create mock objects for the functions
#         with patch.object(xml_to_json, '__call__', return_value=mock_gpu_json) as mock_xml_to_json, \
#              patch.object(parse_gpu_json_to_dict, '__call__', return_value=mock_gpu_dict[0]) as mock_parse_gpu_json_to_dict, \
#              patch.object(create_gpu_prom_file, '__call__') as mock_create_gpu_prom_file:

#             run_nvidia_smi(mock_ip, mock_port, mock_key_path, mock_username)

#             # Check that subprocess.run was called with the correct arguments
#             mocked_run.assert_called_once_with(
#                 ["ssh", "-i", mock_key_path, "-p", str(mock_port), f"{mock_username}@{mock_ip}", "nvidia-smi -q -x"],
#                 capture_output=True, text=True, check=False
#             )

#             # Check that xml_to_json was called with the correct XML
#             mock_xml_to_json.assert_called_once_with(mock_gpu_xml)

#             # Check that parse_gpu_json_to_dict was called
#             mock_parse_gpu_json_to_dict.assert_called_once_with(mock_gpu_json["gpu"])

#             # Check that create_gpu_prom_file was called with the correct arguments
#             mock_create_gpu_prom_file.assert_called_once_with(mock_ip, mock_port, {0: mock_gpu_dict[0]})

# def test_run_nvidia_smi_no_output(mocker):
#     with patch('subprocess.run') as mocked_run:
#         # Mock the subprocess run method
#         mocked_result = MagicMock()
#         mocked_result.stdout = ""
#         mocked_result.stderr = "Some error"
#         mocked_run.return_value = mocked_result

#         # Create mock objects for the functions
#         with patch.object(xml_to_json, '__call__', return_value=mock_gpu_json) as mock_xml_to_json, \
#              patch.object(parse_gpu_json_to_dict, '__call__', return_value=mock_gpu_dict[0]) as mock_parse_gpu_json_to_dict, \
#              patch.object(create_gpu_prom_file, '__call__') as mock_create_gpu_prom_file:

#             run_nvidia_smi(mock_ip, mock_port, mock_key_path, mock_username)

#             # Check that subprocess.run was called with the correct arguments
#             mocked_run.assert_called_once_with(
#                 ["ssh", "-i", mock_key_path, "-p", str(mock_port), f"{mock_username}@{mock_ip}", "nvidia-smi -q -x"],
#                 capture_output=True, text=True, check=False
#             )

#             # Check that xml_to_json, parse_gpu_json_to_dict, and create_gpu_prom_file were not called
#             mock_xml_to_json.assert_not_called()
#             mock_parse_gpu_json_to_dict.assert_not_called()
#             mock_create_gpu_prom_file.assert_not_called()
