import sys
import json
import click
import os

def read_json(input=None):
    if input:
        json_input = input.read()
    else:
        # Read JSON input from stdin
        json_input = sys.stdin.read()
    try:
        data = json.loads(json_input)
        return data
    except json.JSONDecodeError:
        raise click.ClickException("Invalid JSON input.")
    
def read_json_file(filepath):
    """
    Read the JSON data from the specified file.
    """
    with open(filepath, 'r') as file:
        return json.load(file)
    
def get_template_by_type(json_type, template_path="templates"):
    """
    Get the template JSON file based on the 'type' field.
    """

    template_path = os.path.join(template_path, f"{json_type}.json")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file for type '{template_path}' not found.")
    
    return read_json_file(template_path)

def del_safe(_dict, key):
    """
    Delete a key from the dictionary if it exists.
    """
    try:
        _dict.pop(key)
    except KeyError:
        pass

def duration_to_str(duration):
    """
    Convert a duration in seconds to a string in the format "dd:HH:MM:SS".
    """
    time_names = ["day", "hour", "minute", "second"]
    result = ""
    for i, d in enumerate(duration.split(":")):
        if d != "00":
            result += f"{d} {time_names[i]}"
            if int(d) > 1:
                result += "s"
            result += ", "
    return result[:-2]