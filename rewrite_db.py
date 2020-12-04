# rewrite all entries in db with the actual emails because I'm an idiot and messed up the keys numbers
from abstractions.database import remove_all_entries, add_to_db
from abstractions.email import fetch_all_relevant_emails
from abstractions.dictionary_manipulation import capitalise_dict_values
from abstractions.configuration_path import rewrite_new_file, write_to_file

# remove all entries
# fetch emails from the folder with all the relevant emails
# add the emails to db


msg_dict = fetch_all_relevant_emails()

rewrite_new_file('local_dict.json', msg_dict)

dict_of_msgs = capitalise_dict_values(msg_dict)

print(dict_of_msgs)
print(len(dict_of_msgs))


remove_all_entries()

add_to_db(dict_of_msgs)
#add_to_db(msg_dict)

