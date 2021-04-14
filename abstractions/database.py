from abstractions.external_files import get_config
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


# Function to fetch entries from db. If parameter specified, filtered. If not, returns all entries.
def get_db_entries(discriminant=None):  # Default = returns all
    if type(discriminant) is bool:
        entries = list(db.fetch({"done":discriminant}))[0]

    elif type(discriminant) is str:
        entries = list(db.fetch({"subject":discriminant}))[0]

    else:
        entries = list(db.fetch({}))[0]

    return entries


# Function to retrieve an entry.
def get_entry(key:str):
    entry = db.get(key)

    return entry


# Function to update an entry
def update_entry(updates:dict, key:str):

    db.update(updates, key)


# Function to remove an entry.
def remove_entry(key):

    db.delete(key)


# Function to remove all entries.
def remove_all_entries():
    all_entries = list(db.fetch())[0]

    for entry in all_entries:
        db.delete(entry['key'])
