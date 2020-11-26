# Function to get the config values from the Config file
def get_config(path):
    with open(path, 'r') as config_file:
        config_str = config_file.read()
    config = json.loads(config_str)
    return config


# Function to create the email dictionary
def create_dict():
    global msg_dict, msg
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
        for msg in mailbox.fetch(AND(all=True)):  # For message in inbox
            if msg.from_ in email_list:  # If message from email addresses in the   email list
                msg_dict[msg.uid] = {
                    'subject': msg.subject,
                    'text': msg.text
                }  # Dictionary of dictionaries, key is id (identifiers number of the email) and value is a dictionary itself (in this items are subject (category) and body of the email.
                mailbox.copy(msg.uid, 'Read_these')  # Copy message from current folder (inbox) to "Read_these" folder
                # db.put(msg)
    # Prints number of email to the terminal
    print(f"There are {len(msg_dict)} messages")
    return msg_dict


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


# Function to add the messages to the database
def add_to_db(dict_of_msgs):
    for id, msg in dict_of_msgs.items():
        db.put(msg, key=str(id))


# Function that composes the body of the email to send
def generate_message(parsed_dict):
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


# Function that composes and sends the email report
def create_and_send_email():
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

