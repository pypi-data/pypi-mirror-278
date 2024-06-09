"""
combine.py
"""

import os

def prom_files(directory, output_file):
    """
    Combines all .prom files in the specified directory into a single output file.

    Args:
        directory (str): The directory containing the .prom files to combine.
        output_file (str): The path to the output file where the combined contents will be saved.

    Returns:
        None
    """
    combined_data = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.prom'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_data.append(file.read())

    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("\n".join(combined_data))
