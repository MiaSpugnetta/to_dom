from imap_tools import MailBox, AND
import json
from collections import defaultdict
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from simple_colors import *
from deta import Deta


# Function to import parameters from external json file
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config


config = get_config('config.json')  # Get sensitive data stored in separate file

password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']
project_key = config['project_key']

# Access email account
mailbox = MailBox(imap_server)
mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg


# Initialize with a Project Key
deta = Deta(project_key)

# This connects to (or creates) a database
db = deta.Base("test_emails_db")


# If False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable useful for debug
use_stale = False

if use_stale:  # (is True):
    msg_dict = {
                    '4': {
                            'subject': 'TEST',
                            'text': '-- \r\nThomas Rost\r\n'
                         },
                    '5': {
                            'subject': 'Test',
                            'text': 'This is a test.\r\n'
                         },
                    '6': {
                            'subject': 'Test 2',
                            'text': 'Mia is my favorite\r\n'
                         }
               }
else:
    msg_dict = {}
    for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
        if msg.from_ in email_list:  # If message from email addresses in the   email list
            msg_dict[msg.uid] = {
                            'subject': msg.subject,
                            'text': msg.text
                                }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.
            mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder
            #db.put(msg)
# Prints number of email to the terminal
print(f"There are {len(msg_dict)} messages")


# Function to parse the dictionary. ???
def parse_dict(msg_dict):
    assert type(msg_dict) == dict, f"dummy you're using a {type(msg_dict)}"  # Make sure that the dictionary containing the emails is indeed a dictionary.

    return_dict = defaultdict(list)  # If a key is not found in the dictionary, a new entry (of type list)# Prints number of email to the terminal is created.

    for id in msg_dict:  # For message in the dictionary:
        append_dict = {  # Create dictionary that contains
                    'id': id,  # Number that identify the email (id=1 for first email, increases regularly, by one - duh). Basically an index.
                    'text': msg_dict[id]['text']  # Object+body of the email at said index (id).
        }

        return_dict[msg_dict[id]['subject'].capitalize()].append(append_dict)  # TODO: understand what kind of magic happens here. Additionally all subject are capitalised.
    #print(return_dict)
    #print("####################")
    ##print(append_dict)

    # {TODO: find a way to replace "ressource" with "resource"
        #new_dict = defaultdict()
        ##replace = "Ressource"
        ##replace_with = "Resource"
        #new_dict = {i:j for i,j in return_dict.items() if i != "Ressource"}
        #new_dict["Resource"] = return_dict["Ressource"]

        #return_dict['Resource'] = return_dict.pop('Ressource')
        #return_dict['subject'] = "Resource"
        #}

    return return_dict  # Returns a dictionary of dictionaries where the key is the subject (category) of the email and the value is a list of dictionaries that have that category as subject. Each of these subdictionary seems to have id and text as key-value pairs.

##################
#return_dict = parse_dict(msg_dict)
print(msg_dict)
subjects = []
#for i,d in msg_dict.items():
#    for subject in d:
#        subjects.append(d['subject'].capitalize())
#print(subjects)
print("******************")
dict_of_msgs = msg_dict.copy()
for i,j in dict_of_msgs.items():
    for subject in j:
        j['subject'].replace(j['subject'], j['subject'].capitalize())
        #subjects.append(d['subject'])
print("#############")
#{i:j for i,j.capitalize() in msg_dict.items()}
print(dict_of_msgs)
#dict_of_msgs = msg_dict[id]['subject'].capitalize()
#print(msg_dict)
#for id, msg in msg_dict.items():
#    db.put(msg, key=str(id))


stories = db.fetch({'subject':'Stories'})
print(list(stories))

#after this everything is commented out, remove at the end of db attempt
## Function that composes the body of the email to send
#def generate_message(parsed_dict):
#    return_string = ''
#    #{ TODO: format text in email (i.e. categories in bold)
#    #start = "\033[1m"
#    #end = "\033[0;0m" #}
#    for subject in parsed_dict:  # For category in the dictionary:
#        return_string += f"{subject}, number of mails: {len(parsed_dict[subject])}:\n\n"  # Append the name of the category and the number of messages that belong to that category.
#
#        for content in parsed_dict[subject]:  # For each subdictionary:
#            return_string += f"{content['id']}: {content['text']}\n"  # Append the id number (so to have a kind of chronological order) and the actual body to the message in the making.
#
#        return_string += '_________________________\n\n\n'  # Add a separator after each category.
#
#    return return_string  # Return composed message
#
#
## Create parsed dictionary
#return_dict = parse_dict(msg_dict)
#
############################################
## Create email to be sent
#
#context = ssl.create_default_context()  # Create a secure SSL context
#
#port = config['port']
#smtp_server = config['smtp_server']
#sender_email = config['sender_email']
#receiver_email = config['receiver_email']
#
#message = MIMEMultipart()
#message["Subject"] = "Daily report"
#
#body_email_dict = parse_dict(msg_dict)
#body_email = generate_message(body_email_dict)
#first_crap = MIMEText(body_email)
#message.attach(first_crap)
#
#
## Send composed email
#with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:  # Makes sure that the connection is automatically closed at the end of the indented code block. If port is 0 or not specified, standard port for SMTP over SSL is 465.
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message.as_string())
#

# Log out from the email account
mailbox.logout()
