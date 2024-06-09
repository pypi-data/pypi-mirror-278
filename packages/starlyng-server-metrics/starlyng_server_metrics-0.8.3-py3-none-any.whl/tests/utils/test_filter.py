"""
Testing for filter module
"""
from server_metrics.utils.filter import filter_dict_by_keys

def test_basic_functionality():
    """
    Test the function with a basic input where some keys are present.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    keys_to_filter = ['a', 'c']
    expected_output = {'a': 1, 'c': 3}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_keys_not_present():
    """
    Test the function with keys that are not present in the dictionary.
    The function should return an empty dictionary.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    keys_to_filter = ['d', 'e']
    expected_output = {}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_empty_dictionary():
    """
    Test the function with an empty dictionary.
    The function should return an empty dictionary regardless of the keys provided.
    """
    input_dict = {}
    keys_to_filter = ['a', 'b']
    expected_output = {}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_empty_keys():
    """
    Test the function with an empty list of keys.
    The function should return an empty dictionary.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    keys_to_filter = []
    expected_output = {}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_large_input():
    """
    Test the function with a large input dictionary and a large list of keys.
    This test checks the performance and correctness of the function.
    """
    input_dict = {f'key_{i}': i for i in range(1000)}
    keys_to_filter = [f'key_{i}' for i in range(500, 1000)]
    expected_output = {f'key_{i}': i for i in range(500, 1000)}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_mixed_keys():
    """
    Test the function with a mix of present and absent keys.
    The function should return a dictionary with only the present keys.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    keys_to_filter = ['a', 'c', 'e', 'f']
    expected_output = {'a': 1, 'c': 3}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_all_keys_present():
    """
    Test the function where all keys are present in the dictionary.
    The function should return the entire dictionary.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    keys_to_filter = ['a', 'b', 'c']
    expected_output = {'a': 1, 'b': 2, 'c': 3}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output

def test_all_keys_absent():
    """
    Test the function where none of the keys are present in the dictionary.
    The function should return an empty dictionary.
    """
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    keys_to_filter = ['x', 'y', 'z']
    expected_output = {}
    assert filter_dict_by_keys(input_dict, keys_to_filter) == expected_output
