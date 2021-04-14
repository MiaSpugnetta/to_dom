from app import app, server_name
from flask import redirect, render_template
from abstractions.database import get_db_entries, get_entry, update_entry
from collections import defaultdict
from to_dom import get_dict_of_msg
from .forms import ButtonInput


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    list_of_entries = get_db_entries()  # Return a list of all the entries in db as dictionaries in the form of [{subject:<sub>, key:<key>, text:<text>}, {}, ... ].

    msg_dict = defaultdict(list)
    number_of_msg = 0

    # Create a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the key=subject.
        # Dictionary structured as:
        # msg_dict = { <subject1> : [{'key':<key>, 'text':<text>}, {...}, {...}],
        #              <subject2>: [{...}, {...}],
        #               ... }

        if entry['done'] == False:  # Count the number of entries not marked as done
            number_of_msg += 1

    entry_list = []

    for sub, msg_list in msg_dict.items():
        dict_by_sub = {'subject': sub, 'mails': msg_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
        entry_list.append(dict_by_sub)  # Append created dict to the list
        # Create a list structured as: [
        #                               {'subject':<subject>,
        #                                'mails':[
        #                                         {'key':<key>, 'subject':<subject>, 'text':<text>},
        #                                         {...},
        #                                         {...}
        #                                         ]
        #                                },
        #                                { 'subject':<subject2>, 'mails':[{}, {}, {}]}, ... ]

    return render_template("index.html", list_of_entries=entry_list, number_of_msg=number_of_msg)


# Define how to mark  an entry in db as 'done'.
@app.route('/mark_as_done/<key>', methods=['GET', 'POST'])
def mark_as_done(key):  # Key to insure that it's the right entry

    entry = get_entry(key)  # Fetch the entry from db
    assert entry['key'] == key, 'wrong item'

    update = {'done': True}  # Assign to 'done' field value=True
    update_entry(update, key)  # Update the entry in db

    return redirect(f'{server_name}/index')  # Redirect to same page this action can be performed


@app.route('/done', methods=['GET', 'POST'])
def done():
    list_of_entries = get_db_entries(True)  # Fetch from db only the entries marked as 'done'
    number_of_items = (len(list_of_entries))  # Count the number of entries marked as 'done'

    msg_dict = defaultdict(list)

    # Create a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the

    entry_list = []
    for sub, msg_list in msg_dict.items():

        dict_by_sub = {'subject':sub, 'mails':msg_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
        entry_list.append(dict_by_sub)  # Append created dict to the list

    return render_template("done.html", entry_list=entry_list, number_of_items=number_of_items)


# Define how to mark  an entry in db as 'undone'.
@app.route('/mark_undone/<key>', methods=['GET', 'POST'])
def mark_undone(key):

    entry = get_entry(key)  # Fetch the entry from db
    assert entry['key'] == key, 'wrong item'  # Make sure is the right entry

    update = {'done': False}  # Update 'done' field
    update_entry(update, key)   # Update entry in db

    return redirect(f'{server_name}/done')  # Redirect to same page this action can be performed


@app.route('/test_2', methods=['GET', 'POST'])
def test_2():

    all_entries = get_db_entries()  # Get all entries from database
    button = ButtonInput()

    if button.validate_on_submit():  # Should fetch new messages and refresh db. Runs locally, Deta can't access email account

        get_dict_of_msg()  # Fetch new messages from email account and recreate dictionary of messages from the updated db

        # Print to the terminal
        print('Updated!')
        return redirect('test_2')

    return render_template("test_2.html", all_entries=all_entries, form=button)
