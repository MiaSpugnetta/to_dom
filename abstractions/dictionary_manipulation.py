#TODO: rename all methodds file and move to abstraction folder

from imap_tools import AND
from collections import defaultdict


## Function to create the email dictionary
## TODO: move it to email_methods
#def create_dict(mailbox, email_list):
## TODO: move login and logout in this function
#    # If False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable useful for debug
#    use_stale = False
#    if use_stale:  # (is True):
#        msg_dict = {
#            '4': {
#                'subject': 'TEST',
#                'text': '-- \r\nThomas Rost\r\n'
#            },
#            '5': {
#                'subject': 'test',
#                'text': 'This is a test.\r\n'
#            },
#            '6': {
#                'subject': 'Test 2',
#                'text': 'Mia is my favorite\r\n'
#            }
#        }
#        return msg_dict
#    else:
#        msg_dict = {}
#        mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg  # Access email account
#        for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
#            if msg.from_ in email_list:  # If message from email addresses in the   email list
#                msg_dict[msg.uid] = {
#                    'subject': msg.subject,
#                    'text': msg.text
#                }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.
#                mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder
#        mailbox.logout()  # Logout from the email account
#
#    # Prints number of email to the terminal
#    print(f"There are {len(msg_dict)} messages")
#    return msg_dict


# Function to capitalise subject values in the original dictionary {id: {'subject':subject, 'text':text}, ...}
# Necessary to sent to the database
def capitalise_dict_values(dict_of_msgs):
    final_dict = dict_of_msgs.copy()  # Create copy of original dictionary

    for id,msg in final_dict.items():  # For key, value (where key=id and vale={msg}) in dictionary of messages:
        for k,field in msg.items():  # For key, value (where key='subject', 'text and values are the subject and text of the msg) in msg subdictionary:
            if k in ['subject']:  # If key == the str 'subject' (or if the k is contained (is equal to on of the entries) in the list that contains the str 'subject':
                msg[k] = msg[k].capitalize()  # Capitalise the value of the key 'subject'.
            # (Can also be represented as:
            #  For relevant_entry in relevant_list: # relevant_list = ['this', 'that', 'those']
            #    If k == relevant_entry:
            #        Do your thing)

        final_dict[id] = msg  # Overwrite the original msg in the original dict with the msg that contains the capitalised subject values.

    return final_dict


# Function to parse the dictionary.
# Necessary to send the email
def parse_dict(msg_dict):
    assert type(msg_dict) == dict, f"dummy you're using a {type(msg_dict)}"  # Make sure that the dictionary containing the emails is indeed a dictionary.

    return_dict = defaultdict(list)  # If a key is not found in the dictionary, a new entry (of type list) is created.

    for id in msg_dict:  # For message in the dictionary:
        append_dict = {  # Create dictionary that contains
                    'id': id,  # Number that identify the email (id=1 for first email, increases regularly, by one - duh). Basically an index.
                    'text': msg_dict[id]['text']  # Object+body of the email at said index (id).
        }

        return_dict[msg_dict[id]['subject'].capitalize()].append(append_dict)  # Original dictionary was structured as:
        # { id: {
        #           'subject': msg.subject,
        #           'text': msg.text
        #       },
        #   id: {same}, ...
        #} dictionary where every k,v is made of k=id and v={dictionary}, in turn made of {keys=subjects, text}
        # Parsed dictionary is messages grouped by (capitalised) subject:
        # {subject: [
        #               {'id': id,
        #                'text': msg.text},
        #               {}
        #               ...
        #           ],
        # subject2: [list of dictionaries where every dictionary has keys id, text]
        #}

    return return_dict  # Returns a dictionary of dictionaries where the key is the subject (category) of the email and the value is a list of dictionaries that have that category as subject. Each of these subdictionary has then id and text as keys.
