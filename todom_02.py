from methods import get_config, create_and_send_email#, get_dict_of_msg
#from to_dom_copy import get_dict_of_msg, create_and_send_email
from imap_tools import MailBox
from deta import Deta


config = get_config('config.json')  # Get sensitive data stored in separate file

# Values assigned to variables
password = config['password']
email = config['email']
email_list = config['email_list']
imap_server = config['imap_server']
project_key = config['project_key']

# Create mailbox object
mailbox = MailBox(imap_server)

# Initialize with a Project Key
deta = Deta(project_key)
# This connects to (or creates) a database
db = deta.Base("test_emails_db")





# Set to True before running the script and email will be composed and sent
# Set to False before running the flask app
# If True, them email is composed and sent
def send_mail(send_report=False):
    #global mailbox, email, password
    if send_report:
        create_and_send_email(mailbox, email, password, email_list, db)  # Create email to be sent and send it
        print("Email has been sent!")
