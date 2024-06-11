"""
Testing for xml_parser module
"""
from server_metrics.utils.xml_parser import xml_to_json

def test_empty_xml():
    """
    Tests for empty xml
    """
    xml_data = "<root></root>"
    expected_output = {}
    assert xml_to_json(xml_data) == expected_output

def test_single_element():
    """
    Tests for single element
    """
    xml_data = "<root><child>value</child></root>"
    expected_output = {'child': {'text': 'value'}}
    assert xml_to_json(xml_data) == expected_output

def test_multiple_elements():
    """
    Tests for multiple elements
    """
    xml_data = "<root><child1>value1</child1><child2>value2</child2></root>"
    expected_output = {
        'child1': {'text': 'value1'},
        'child2': {'text': 'value2'}
    }
    assert xml_to_json(xml_data) == expected_output

def test_nested_elements():
    """
    Tests for nexted element
    """
    xml_data = "<root><parent><child>value</child></parent></root>"
    expected_output = {'parent': {'child': {'text': 'value'}}}
    assert xml_to_json(xml_data) == expected_output

def test_repeated_elements():
    """
    Tests for repeated element
    """
    xml_data = "<root><child>value1</child><child>value2</child></root>"
    expected_output = {
        'child': [{'text': 'value1'}, {'text': 'value2'}]
    }
    assert xml_to_json(xml_data) == expected_output

def test_text_and_child_elements():
    """
    Tests for text and child elements
    """
    xml_data = "<root><parent>text<child>value</child></parent></root>"
    expected_output = {'parent': {'text': 'text', 'child': {'text': 'value'}}}
    assert xml_to_json(xml_data) == expected_output

def test_element_with_attributes():
    """
    Tests for element with attributes
    """
    xml_data = '<root><child attribute="value">text</child></root>'
    expected_output = {'child': {'text': 'text'}}
    assert xml_to_json(xml_data) == expected_output

def test_complex_structure():
    """
    Tests for complex structure
    """
    xml_data = """
    <root>
        <parent1>
            <child1>value1</child1>
            <child2>value2</child2>
        </parent1>
        <parent2>
            <child3>value3</child3>
            <child4>
                <grandchild>value4</grandchild>
            </child4>
        </parent2>
    </root>
    """
    expected_output = {
        'parent1': {
            'child1': {'text': 'value1'},
            'child2': {'text': 'value2'}
        },
        'parent2': {
            'child3': {'text': 'value3'},
            'child4': {'grandchild': {'text': 'value4'}}
        }
    }
    assert xml_to_json(xml_data) == expected_output
