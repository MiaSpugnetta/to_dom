# Access email account, fetch messages, uploading to database, creating email report and send it
from abstractions.dictionary_manipulation import capitalise_dict_values, parse_dict, generate_text_message
from abstractions.database import add_to_db, get_db_entries, update_entry
from abstractions.email import fetch_new_msgs_from_email, compose_msg, send_email


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
    # II PRINT STATEMENT
    print(f'there is a total of {len(entries_from_db)} entries in db')

    number_undone_entries = 0

    # Create dictionary with all the entries
    for entry in entries_from_db:
        # Add 'done' field to db for new entries
        if 'done' not in entry:
            update = {'done': False}
            update_entry(update, entry['key'])
            number_undone_entries += 1

        # Add entry to dict only if entry not marked as 'done'
        elif not entry['done']:
            dict_from_db[entry['key']] = {'subject': entry['subject'], 'text': entry['text'], 'date': entry['date']}
            number_undone_entries += 1

    # Print number of entries that will be sent in the report
    # III PRINT STATEMENT
    print(f'there are {number_undone_entries} relevant entries in db')

    return dict_from_db


# Function that composes and sends the email report.
def create_and_send_email():
    msg_dict = get_dict_of_msg()  # Create msg_dict from db entries

    parsed_dict = parse_dict(msg_dict)  # Create parsed dictionary (grouped by subject)

    text_email = generate_text_message(parsed_dict)  # Create text that goes in the body of the email

    message = compose_msg(text_email)  # Create actual email to be sent (email body, subject)

    send_email(message)  # Send composed email


# Run external file (todom_active.py) where function is called so not to have to modify this file.
def send_report(send_report=False):
    if send_report:
        create_and_send_email()  # Create email to be sent and send it
        print("Email has been sent!")
