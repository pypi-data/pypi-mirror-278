"""
filter.py
"""

def filter_dict_by_keys(input_dict, keys_to_filter):
    """
    Args:
        input_dict (_type_):
        keys_to_filter (_type_):

    Returns:
        _type_:
    """
    return {k: input_dict[k] for k in keys_to_filter if k in input_dict}
