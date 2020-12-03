from abstractions.configuration_path import get_config, write_to_file, load_from_file
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

# Create mailbox object
mailbox = MailBox(imap_server)


# Function to create the email dictionary. Login into email account. If new relevant emails, add to dict_file. Copy email to folder1 and move email to folder2. Logout from account. Print # of new messages fetched, create dict to be returned from file. Return dict.
def fetch_msgs_from_email():
    # If False, fetches emails from inbox and creates dictionary. Else uses simulated, less complex one stored as variable useful for debug
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
        mailbox = MailBox(imap_server)
        with mailbox.login(email, password, initial_folder='INBOX') as mailbox:
        #mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg  # Access email account
            for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
                if msg.from_ in email_list:  # If message from email addresses in the   email list
                    msg_dict[msg.uid] = {
                        'subject': msg.subject,
                        'text': msg.text
                    }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.

                    write_to_file('./msg_dict.json', msg)  # Add msg to the json dict file

                    mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder

                    mailbox.move(msg.uid, 'Already_read')  # Move message from inbox to "Already_read" folder

        #mailbox.logout()  # Logout from the email account

    # Print number of new email to the terminal
    print(f"There are {len(msg_dict)} new messages")

    use_this_dict = load_from_file('./msg_dict.json')  # Loads the dict from json file

    return use_this_dict #msg_dict



def compose_msg(text_email):
    message = MIMEMultipart()  # Create message object
    message["Subject"] = "Daily report"  # Create subject of the email
    body_email = MIMEText(text_email)  # Create the body of the email
    message.attach(body_email)  # Attach the email body to the message

    return message  # Return composed email


def send_email(message):
    context = ssl.create_default_context()  # Create a secure SSL context
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:  # Makes sure that the connection is automatically closed at the end of the indented code block. If port is 0 or not specified, standard port for SMTP over SSL is 465.
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
