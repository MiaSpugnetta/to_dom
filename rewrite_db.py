# Rewrite all entries in db with the actual emails because I'm an idiot and messed up the keys numbers
from abstractions.database import remove_all_entries, add_to_db
from abstractions.email import fetch_all_relevant_emails
from abstractions.message_manipulation import capitalise_dict_values
from abstractions.external_files import overwrite_file


# Fetch all relevant emails from email folder
msg_dict = fetch_all_relevant_emails()


# Overwrite json dict file that contains all the relevant messages
overwrite_file('local_dict.json', msg_dict)


# Capitalise all messages subjects
dict_of_msgs = capitalise_dict_values(msg_dict)


# Print to the terminal
print(f'There are {len(dict_of_msgs)} relevant messages')


# Erase the database entries
remove_all_entries()


# Restore the database
add_to_db(dict_of_msgs)
