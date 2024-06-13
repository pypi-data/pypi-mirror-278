import json


def load_json(file_path):
    """
    Open a JSON file and load its content into a dictionary.

    :param file_path: The path to the JSON file to open.
    :return: The JSON data converted into a dictionary.
    """
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def save_to_json(data, file_path):
    """
    Save a dictionary as a JSON file.

    :param data: The dictionary data to save.
    :param file_path: The path to save the JSON file.
    """
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
