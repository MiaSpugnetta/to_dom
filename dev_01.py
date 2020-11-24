import imaplib
import email
from imap_tools import MailBox, AND
import json
from collections import defaultdict
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from simple_colors import *

# get sensitive data stored in separate file
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config

config = get_config('config.json')

password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']

# access email account
mailbox = MailBox(imap_server)
mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg


# if False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable
use_stale = False

if  use_stale:
    msg_dict = {'4': {'subject': 'TEST', 'text': '-- \r\nThomas Rost\r\n'}, '5': {'subject': 'Test', 'text': 'This is a test.\r\n'}, '6': {'subject': 'Test 2', 'text': 'Mia is my favorite\r\n'}}
else:
    msg_dict = {}
    for msg in mailbox.fetch(AND(all=True)):
        if msg.from_ in email_list:
            msg_dict[msg.uid] = {
            'subject':msg.subject,
            'text':msg.text
            }
            mailbox.copy(msg.uid, 'Read_these')

# prints number of email to the terminal
print(f"There are {len(msg_dict)} messages")

# list of different email subjects
#list_of_subjects = [msg_dict[id]['subject'] for id in msg_dict]
#list_of_subjects = [subject.capitalize() for subject in list_of_subjects]
#list_of_subjects = ['Resource' if subject=='Ressource' else subject for subject in #list_of_subjects]
#print(list_of_subjects)


#def generate_message(list_of_subjects):
#    return_string = ''
#    for subject in set(list_of_subjects):
#            count = list_of_subjects.count(subject)
#            return_string += f"There are {count} {subject} emails \n"
#    return return_string

def parse_dict(msg_dict):
    assert type(msg_dict) == dict, f'dummy youre using a {type(msg_dict)}'
    return_dict = defaultdict(list)

    for id in msg_dict:
        append_dict = {
        'id':id,
        'text':msg_dict[id]['text']
        }
        return_dict[msg_dict[id]['subject'].capitalize()].append(append_dict)
    print(return_dict)
    #new_dict = defaultdict()
    ##replace = "Ressource"
    ##replace_with = "Resource"
    #new_dict = {i:j for i,j in return_dict.items() if i != "Ressource"}
    #new_dict["Resource"] = return_dict["Ressource"]



    #return_dict['Resource'] = return_dict.pop('Ressource')
        #return_dict['subject'] = "Resource"


    return return_dict


def generate_message(parsed_dict):
    return_string = ''
    #start = "\033[1m"
    #end = "\033[0;0m"
    for subject in parsed_dict:
        return_string += f"{subject}, number of mails: {len(parsed_dict[subject])}:\n\n"

        for content in parsed_dict[subject]:
            return_string += f"{content['id']}: {content['text']}\n"

        return_string += '_________________________\n\n\n'

    return return_string


    #{'TEST': [{'id': '4', 'text': '-- \r\nThomas Rost\r\n'}], 'Test': [{'id': '5', 'text': 'This is a test.\r\n'}], 'Test 2': [{'id': '6', 'text': 'Mia is my favorite\r\n'}]}

return_dict = parse_dict(msg_dict)

###########################################


context = ssl.create_default_context()

port = config['port']
smtp_server = config['smtp_server']
sender_email = config['sender_email']
receiver_email = config['receiver_email']

message = MIMEMultipart()
message["Subject"] = "Daily report"

body_email_dict = parse_dict(msg_dict)
body_email = generate_message(body_email_dict)
first_crap = MIMEText(body_email)
message.attach(first_crap)


with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())


mailbox.logout()
