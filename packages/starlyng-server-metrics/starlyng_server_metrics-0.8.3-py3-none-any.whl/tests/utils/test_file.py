"""
Testing for file module
"""

import os
import shutil
import pytest

from server_metrics.utils.file import clear_directory, ClearDirectoryError, create_directory, CreateDirectoryError

@pytest.fixture
def setup_test_directory(tmp_path):
    """Fixture to create a temporary directory for testing."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True, exist_ok=True)
    # Create some test files and directories
    (test_dir / "test_file.txt").write_text("This is a test file.")
    (test_dir / "subdir").mkdir()
    (test_dir / "subdir" / "sub_file.txt").write_text("This is a subdirectory test file.")
    return test_dir

def test_clear_directory(setup_test_directory):
    """Test clearing the specified directory."""
    test_dir = setup_test_directory
    assert os.path.exists(test_dir)

    clear_directory(directory=str(test_dir))

    assert not os.path.exists(test_dir)

def test_clear_directory_no_exist(tmp_path):
    """Test clearing the specified directory when it does not exist."""
    test_dir = tmp_path / "test_dir"

    # Ensure the directory does not exist
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # Should not raise any exceptions
    clear_directory(directory=str(test_dir))

    # Ensure it still does not exist
    assert not os.path.exists(test_dir)

def test_clear_directory_error(mocker, tmp_path):
    """Test that an error during deletion raises ClearDirectoryError."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True, exist_ok=True)

    mocker.patch("shutil.rmtree", side_effect=Exception("Mocked deletion error"))

    with pytest.raises(ClearDirectoryError, match="Failed to clear the directory .* Reason: Mocked deletion error"):
        clear_directory(directory=str(test_dir))

def test_create_new_directory(tmp_path):
    """
    Test that a new directory is created successfully.

    This test uses pytest's tmp_path fixture to create a temporary directory path.
    It asserts that the directory does not exist before the function call, then
    calls the create_directory function, and finally checks that the directory was created.
    """
    # Create a temporary directory path
    new_dir = tmp_path / "new_directory"

    # Ensure the directory does not exist before the test
    assert not new_dir.exists()

    # Call the function to create the directory
    create_directory(str(new_dir))

    # Check that the directory was created
    assert new_dir.exists()

def test_create_existing_directory(tmp_path):
    """
    Test that the function behaves correctly when the directory already exists.

    This test creates a directory beforehand and asserts that it exists.
    It then calls the create_directory function and checks that the directory still exists.
    """
    # Create a temporary directory
    existing_dir = tmp_path / "existing_directory"
    os.makedirs(existing_dir)

    # Ensure the directory exists before the test
    assert existing_dir.exists()

    # Call the function to create the directory (which already exists)
    create_directory(str(existing_dir))

    # Check that the directory still exists
    assert existing_dir.exists()

def test_create_directory_error(monkeypatch):
    """
    Test that the function raises a DirectoryCreationError when an error occurs.

    This test uses pytest's monkeypatch fixture to simulate an error during directory creation.
    It asserts that calling create_directory raises DirectoryCreationError and checks
    that the raised exception contains the correct error message.
    """
    # Use monkeypatch to simulate an error during directory creation
    def mock_makedirs(path):
        raise OSError("Mocked error")

    monkeypatch.setattr(os, "makedirs", mock_makedirs)

    # Attempt to create a directory and expect a DirectoryCreationError
    with pytest.raises(CreateDirectoryError) as excinfo:
        create_directory("/path/to/error_directory")

    # Check that the exception message is correct
    assert "Mocked error" in str(excinfo.value)
