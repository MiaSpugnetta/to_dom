# Access email account, fetch messages, uploading to database, creating email report and send it
from json_methods import get_config
from imap_tools import MailBox
from dictionary_methods import create_dict, capitalise_dict_values, parse_dict
from database_methods import add_to_db
from email_methods import generate_message
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


config = get_config('config.json')  # Get sensitive data stored in separate file

# Values assigned to variables
password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']

# Create mailbox object
mailbox = MailBox(imap_server)



# Function to create the dictionary of messages. Adds messages to db. Returns a dict with capitalised subjects.
def get_dict_of_msg():#mailbox:MailBox, email:str, password:str, email_list:list, db):
    mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg  # Access email account
    msg_dict = create_dict(mailbox, email_list)  # Create dictionary with relevant emails
    dict_of_msgs = capitalise_dict_values(msg_dict)  # Capitalise the first letter of the subject of the email
    mailbox.logout()  # Logout from the email account

    add_to_db(dict_of_msgs)  # Add the messages to the db

    return dict_of_msgs  # Return the dictionary of emails


# Function that composes and sends the email report
def create_and_send_email():#mailbox, email, password, email_list, db):
    msg_dict = get_dict_of_msg()#mailbox, email, password, email_list, db)  # Create msg_dict

    context = ssl.create_default_context()  # Create a secure SSL context
    port = config['port']
    smtp_server = config['smtp_server']
    sender_email = config['sender_email']
    receiver_email = config['receiver_email']
    message = MIMEMultipart()  # Create message object
    message["Subject"] = "Daily report"  # Create subject of the email
    parsed_dict = parse_dict(msg_dict)  # Create parsed dictionary
    text_email = generate_message(parsed_dict)  # Create text that goes in the body of the email
    body_email = MIMEText(text_email)  # Create the body of the email
    message.attach(body_email)  # Attach the email body to the message
    # Send composed email
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:  # Makes sure that the connection is automatically closed at the end of the indented code block. If port is 0 or not specified, standard port for SMTP over SSL is 465.
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


# Set to True before running the script and email will be composed and sent
# Set to False before running the flask app
# If True, them email is composed and sent. Run external file (todom_active.py).
def send_mail(send_report=False):
    if send_report:
        create_and_send_email()#mailbox, email, password, email_list, db)  # Create email to be sent
        print("Email has been sent!")
