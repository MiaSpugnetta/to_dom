from abstractions.external_files import get_config, write_to_file
from imap_tools import MailBox, AND
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


config = get_config('./config.json')  # Get sensitive data stored in separate file

# Values assigned to variables.
# Access account to fetch
password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']

# Access account to send
port = config['port']
smtp_server = config['smtp_server']
sender_email = config['sender_email']
receiver_email = config['receiver_email']


# Function to create the email dictionary. Login into email account. If new relevant emails, add to dict_file. Copy email to folder1 and move email to folder2. Logout from account. Print # of new messages fetched, create dict to be returned from file. Return dict.
def fetch_new_msgs_from_email():
    # If False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable - useful for debug
    use_stale = False
    if use_stale:  # (is True):
        msg_dict = {
            '4': {
                'subject': 'TEST',
                'text': '-- \r\nThomas Rost\r\n'
            },
            '5': {
                'subject': 'test',
                'text': 'This is a test.\r\n'
            },
            '6': {
                'subject': 'Test 2',
                'text': 'Mia is my favorite\r\n'
            }
        }
        return msg_dict
    else:
        msg_dict = {}
        mailbox = MailBox(imap_server)  # Create mailbox object
        with mailbox.login(email, password, initial_folder='INBOX') as mailbox:  # Access email account
            for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
                # TODO: rewrite this, it works but it's stupid
                if msg.from_ in email_list[0]:
                    msg_dict[msg.uid] = {
                        'subject': msg.subject,
                        'text': msg.text,
                        'date': msg.date_str,
                        'user': 'T'
                    }

                    write_to_file('./local_dict.json', msg)
                    mailbox.copy(msg.uid, 'Read_these')
                    mailbox.move(msg.uid, 'Already_read')

                elif msg.from_ in email_list[1]:
                    msg_dict[msg.uid] = {
                        'subject': msg.subject,
                        'text': msg.text,
                        'date': msg.date_str,
                        'user': 'M'
                    }

                    write_to_file('./local_dict.json', msg)
                    mailbox.copy(msg.uid, 'Read_these')
                    mailbox.move(msg.uid, 'Already_read')

                elif msg.from_ in email_list:  # If message from email addresses in the email list
                    msg_dict[msg.uid] = {
                        'subject': msg.subject,
                        'text': msg.text,
                        'date': msg.date_str
                    }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category), date and body of the email.

                    ###############################################
                    # Useful for debugging, not relevant for to_dom
                    write_to_file('./local_dict.json', msg)

                    ###############################################

                    mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder

                    mailbox.move(msg.uid, 'Already_read')  # Move message from inbox to "Already_read" folder

    # Print number of new email to the terminal
    # I PRINT STATEMENT
    print(f"There are {len(msg_dict)} new messages")

    return msg_dict


# Function to create an email dictionary with all the relevant emails.
# Only relevant if db needs updating, not used in to_dom
def fetch_all_relevant_emails():
    msg_dict = {}
    mailbox = MailBox(imap_server)  # Create mailbox object
    with mailbox.login(email, password, initial_folder='Already_read') as mailbox:  # Access email account
        for msg in mailbox.fetch(AND(all=True)):  # For message in folder with relevant emails
            msg_dict[msg.uid] = {
                'subject': msg.subject,
                'text': msg.text,
                'date': msg.date_str
            }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category), body of the email and date.

    print(f"There are {len(msg_dict)} relevant emails")

    return msg_dict


# Function to compose the email.
def compose_msg(text_email):
    message = MIMEMultipart()  # Create message object
    message["Subject"] = "Daily report"  # Create subject of the email
    body_email = MIMEText(text_email)  # Create the body of the email
    message.attach(body_email)  # Attach the email body to the message

    return message  # Return composed email


# Function to send the email.
def send_email(message):
    context = ssl.create_default_context()  # Create a secure SSL context
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:  # Make sure that the connection is automatically closed at the end of the indented code block. If port is 0 or not specified, standard port for SMTP over SSL is 465.
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
