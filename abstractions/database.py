from abstractions.configuration_path import get_config
from deta import Deta


config = get_config('./config.json')  # Get sensitive data stored in separate file

project_key = config['project_key']

# Initialize with a Project Key
deta = Deta(project_key)
# This connects to (or creates) a database
db = deta.Base("test_emails_db")


# Function to add the messages to the database.
def add_to_db(dict_of_msgs):
    for id, msg in dict_of_msgs.items():
        db.put(msg, key=str(id))


# Function to fetch the entries in the db.
def get_db_entries():
    all_entries = list(db.fetch())[0]

    return all_entries


# Function to fetch entries grouped by subject.
def get_db_entries_by_category(subject:str):
    entries_of_subject = list(db.fetch(subject))

    return entries_of_subject