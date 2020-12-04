# Access email account, fetch messages, uploading to database, creating email report and send it
from abstractions.dictionary_manipulation import capitalise_dict_values, parse_dict, generate_text_message
from abstractions.database import add_to_db, get_db_entries
from abstractions.email import fetch_new_msgs_from_email, compose_msg, send_email
#from abstractions.configuration_path import load_from_file


# Function to create the dictionary of messages. Fetches new emails. Capitalises subjects. Adds messages to db. Returns a dict.
def get_dict_of_msg():
    # This is to add new emails to db
    msg_dict_new = fetch_new_msgs_from_email()  # Create dict with new emails
    dict_of_msgs = capitalise_dict_values(msg_dict_new)  # Capitalise the first letter of the subject of the email
    add_to_db(dict_of_msgs)  # Add the messages to the db

    ###############################
    # This is to create the dict from db entries
    dict_from_db = {}
    entries_from_db = get_db_entries()  # List that contains all the db entries

    # Print number of entries in db to the terminal
    print(f'there are {len(entries_from_db)} entries in db')

    # Create dictionary with all the entries
    for entry in entries_from_db:
        dict_from_db[entry['key']] = {'subject': entry['subject'], 'text': entry['text'], 'date': entry['date']}

    return dict_from_db


# Function that composes and sends the email report.
def create_and_send_email():
    msg_dict = get_dict_of_msg()  # Create msg_dict from db entries

    parsed_dict = parse_dict(msg_dict)  # Create parsed dictionary

    text_email = generate_text_message(parsed_dict)  # Create text that goes in the body of the email

    message = compose_msg(text_email)  # Create actual email to be sent (email body, subject)

    send_email(message)  # Send composed email


# Set to True before running the script and email will be composed and sent
# Set to False before running the flask app
# If True, them email is composed and sent. Run external file (todom_active.py).
def send_report(send_report=False):
    if send_report:
        create_and_send_email()  # Create email to be sent and send it
        print("Email has been sent!")
