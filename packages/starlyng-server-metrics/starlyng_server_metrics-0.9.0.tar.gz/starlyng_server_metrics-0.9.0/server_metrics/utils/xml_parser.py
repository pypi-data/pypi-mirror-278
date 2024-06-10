"""
xml_parser.py
"""
import xml.etree.ElementTree as ET
from typing import Dict, List

def xml_to_json(xml_data: str) -> Dict[str, any]:
    """
    Converts xml to json

    Args:
        xml_data (str):

    Returns:
        Dict[str, any]:
    """
    root = ET.fromstring(xml_data)
    def recurse_node(node):
        result = {}
        if node.text and node.text.strip():
            result['text'] = node.text.strip()
        for child in node:
            child_result = recurse_node(child)
            if child.tag in result:
                if isinstance(result[child.tag], List):
                    result[child.tag].append(child_result)
                else:
                    result[child.tag] = [result[child.tag], child_result]
            else:
                result[child.tag] = child_result
        return result
    return recurse_node(root)
