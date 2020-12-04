import json


# Function to get the config values from the Config file.
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)

    return config


# Function to write to json file
def write_to_file(path, msg):
    with open(path, 'r') as file:
        data = json.load(file)

        data[msg.uid] = {'subject': msg.subject, 'text': msg.text, 'date': msg.date_str}

    with open(path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


# Function to load the dict from file
def load_from_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
        print(f"There are {len(data)} messages")

        return data


# Function to overwrite json file
def rewrite_new_file(path, dictionary):
    with open(path, 'w') as file:
        json.dump(dictionary, file, indent=4, sort_keys=True)