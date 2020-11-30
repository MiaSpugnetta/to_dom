from abstractions.configuration_path import get_config
from imap_tools import MailBox, AND


config = get_config('./config.json')  # Get sensitive data stored in separate file

# Values assigned to variables
password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']

# Create mailbox object
mailbox = MailBox(imap_server)


# Function to create the email dictionary
def fetch_msgs_from_email():#mailbox, email_list):
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
        mailbox.login(email, password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg  # Access email account
        for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
            if msg.from_ in email_list:  # If message from email addresses in the   email list
                msg_dict[msg.uid] = {
                    'subject': msg.subject,
                    'text': msg.text
                }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.
                mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder
        mailbox.logout()  # Logout from the email account

    # Prints number of email to the terminal
    print(f"There are {len(msg_dict)} messages")
    return msg_dict


# Function that composes the body of the email to send
def generate_text_message(parsed_dict):
    return_string = ''
    #{ TODO: format text in email (i.e. categories in bold)
    #start = "\033[1m"
    #end = "\033[0;0m" #}
    for subject in parsed_dict:  # For category in the dictionary:
        return_string += f"{subject}, number of mails: {len(parsed_dict[subject])}:\n\n"  # Append the name of the category and the number of messages that belong to that category.

        for content in parsed_dict[subject]:  # For each subdictionary:
            return_string += f"{content['id']}: {content['text']}\n"  # Append the id number (so to have a kind of chronological order) and the actual body to the message in the making.

        return_string += '_________________________\n\n\n'  # Add a separator after each category.

    return return_string  # Return composed message (text that goes in the body of the email)
