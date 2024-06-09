"""
Testing for configuration module
"""

import os
import pytest
from server_metrics.utils.configuration import load_configuration, parse_arguments, load_env_variables, get_configuration

# Constants
CMD_ARGS = [
    '--servers',
    '192.168.0.1:22,192.168.0.2:23',
    '--key_path',
    '/path/to/key',
    '--username',
    'testuser',
    '--combined_metrics_dir', '/path/to/metrics'
]
ENV_VARS = {
    'SERVERS': '192.168.0.3:24,192.168.0.4:25',
    'KEY_PATH': '/path/to/env_key',
    'USERNAME': 'envuser',
    'COMBINED_METRICS_DIR': '/path/to/metrics/envuser'
}
ENV_FILE_CONTENT = (
    "SERVERS=192.168.0.5:26,192.168.0.6:27\n"
    "KEY_PATH=/path/to/env_file_key\n"
    "USERNAME=fileuser\n"
    "COMBINED_METRICS_DIR=/path/to/metrics/fileuser"
)
ENV_FILE_VARS = {
    'SERVERS': '192.168.0.5:26,192.168.0.6:27',
    'KEY_PATH': '/path/to/env_file_key',
    'USERNAME': 'fileuser',
    'COMBINED_METRICS_DIR': '/path/to/metrics/fileuser'
}

@pytest.fixture
def mock_load_dotenv(mocker, tmp_path):
    """Fixture to mock loading environment variables from a temporary .env file."""
    env_file = tmp_path / '.env'
    env_file.write_text(ENV_FILE_CONTENT)

    def mock_load_dotenv_func(dotenv_path=None):
        if dotenv_path == str(env_file):
            os.environ.update(ENV_FILE_VARS)

    mocker.patch('dotenv.load_dotenv', side_effect=mock_load_dotenv_func)
    return env_file

def test_parse_arguments(mocker):
    """Test command-line argument parsing."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)
    args = parse_arguments()

    assert args.servers == '192.168.0.1:22,192.168.0.2:23'
    assert args.key_path == '/path/to/key'
    assert args.username == 'testuser'
    assert args.combined_metrics_dir == '/path/to/metrics'

def test_load_env_variables(mock_load_dotenv, monkeypatch):
    """Test loading environment variables from a .env file."""

    # Ensure no pre-existing environment variables interfere with the test
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

    # Mock the load_dotenv call to use the path to the temp .env file
    load_env_variables(dotenv_path=str(mock_load_dotenv))

    # Assert that the environment variables are set correctly
    assert os.getenv('SERVERS') == '192.168.0.5:26,192.168.0.6:27'
    assert os.getenv('KEY_PATH') == '/path/to/env_file_key'
    assert os.getenv('USERNAME') == 'fileuser'
    assert os.getenv('COMBINED_METRICS_DIR') == '/path/to/metrics/fileuser'

    # Cleanup environment variables
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

def test_get_configuration_cmd_args(mocker):
    """Test getting configuration from command-line arguments."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)
    args = parse_arguments()

    servers, key_path, username, combined_metrics_dir = get_configuration(args)

    assert servers == [('192.168.0.1', 22), ('192.168.0.2', 23)]
    assert key_path == '/path/to/key'
    assert username == 'testuser'
    assert combined_metrics_dir == '/path/to/metrics'

def test_get_configuration_env_vars(mocker):
    """Test getting configuration from environment variables."""
    mocker.patch.dict(os.environ, ENV_VARS)
    mocker.patch('sys.argv', ['configuration.py'])
    args = parse_arguments()

    servers, key_path, username, combined_metrics_dir = get_configuration(args)

    assert servers == [('192.168.0.3', 24), ('192.168.0.4', 25)]
    assert key_path == '/path/to/env_key'
    assert username == 'envuser'
    assert combined_metrics_dir == '/path/to/metrics/envuser'

def test_load_configuration_cmd_args(mocker):
    """Test loading configuration from command-line arguments."""
    mocker.patch('sys.argv', ['configuration.py'] + CMD_ARGS)

    servers, key_path, username, combined_metrics_dir = load_configuration()

    assert servers == [('192.168.0.1', 22), ('192.168.0.2', 23)]
    assert key_path == '/path/to/key'
    assert username == 'testuser'
    assert combined_metrics_dir == '/path/to/metrics'

def test_load_configuration_env_vars(mocker):
    """Test loading configuration from environment variables."""
    mocker.patch.dict(os.environ, ENV_VARS)
    mocker.patch('sys.argv', ['configuration.py'])

    servers, key_path, username, combined_metrics_dir = load_configuration()

    assert servers == [('192.168.0.3', 24), ('192.168.0.4', 25)]
    assert key_path == '/path/to/env_key'
    assert username == 'envuser'
    assert combined_metrics_dir == '/path/to/metrics/envuser'

def test_load_configuration_env_file(mocker, mock_load_dotenv, monkeypatch):
    """Test loading configuration from a .env file."""
    # Mock sys.argv to simulate no command-line arguments
    mocker.patch('sys.argv', ['configuration.py'])

    # Mock Path.exists to return True for the .env file path
    mocker.patch('pathlib.Path.exists', return_value=True)

    # Ensure no pre-existing environment variables interfere with the test
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)

    # Load the configuration using the temporary .env file path
    servers, key_path, username, combined_metrics_dir = load_configuration(dotenv_path=str(mock_load_dotenv))

    # Assert the configuration values
    assert servers == [('192.168.0.5', 26), ('192.168.0.6', 27)]
    assert key_path == '/path/to/env_file_key'
    assert username == 'fileuser'
    assert combined_metrics_dir == '/path/to/metrics/fileuser'

    # Cleanup environment variables
    monkeypatch.delenv('SERVERS', raising=False)
    monkeypatch.delenv('KEY_PATH', raising=False)
    monkeypatch.delenv('USERNAME', raising=False)
    monkeypatch.delenv('COMBINED_METRICS_DIR', raising=False)
