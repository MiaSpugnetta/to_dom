import json
#TODO: rename

# Function to get the config values from the Config file
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config
