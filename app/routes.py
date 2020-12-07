from app import app, server_name
from flask import redirect, render_template, url_for
from abstractions.database import get_db_entries, get_entry, update_entry
from collections import defaultdict
from to_dom import get_dict_of_msg
from .forms import ButtonInput


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    all_entries = get_db_entries()
    button = ButtonInput()

    if button.validate_on_submit():

        get_dict_of_msg()

        print('Updated!')
        return redirect('index')#f"""You are the favourite and your database has been updated, refresh the page!"""

    return render_template("index.html", all_entries=all_entries, form=button)


# ToDO add 'done' button:
#1. Frontend, mke sure to render button for each entry
# 2. Button has to be connected to each entry
# write post that marks entries as done
# 3.1 add field to db: done =False
#. in post set done = True
#4. Make sure only tasks with done = False are shown in frontend
# 4.1. either via frontned (hack) or
#4.2. by only takind from the DB the entries that aren't done <_________________________________
# 5. bonus: Display how many tasks are in done status
#6. bonus: write unit tests for the above backend hndling stuff - importznt here to s you dont accidentally set the wrong task to done
#def mark_entry_as_done(entry_id):
#    in_db_mark_as_done(entry_id)


@app.route('/test', methods=['GET', 'POST'])
def test():
    list_of_entries = get_db_entries()  # Return a list of all the entries in db as dictionaries in the form of [{subject:<sub>, key:<key>, text:<text>}, {}, ... ].

    msg_dict = defaultdict(list)

    # Returns a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the key=subject.
        # msg_dict = { <subject1> : [{'key':<key>, 'text':<text>}, {}, ...],
        #              <subject2>: [{ }, {}, ...},
        #               ... }

    #list_of_subjects = []
    #for subject in msg_dict:
    #   list_of_subjects.append(subject)

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


    #for sub in list_of_subjects:
    #    mail_list = get_db_entries(sub)  # Fetch entries from db with specified subject
    #    dict_by_sub = {"subject":sub, "mails":mail_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
    #    entry_list.append(dict_by_sub)  # Append created dict to the list
    #    # Create a list structured as: [
    #    #                               {'subject':<subject>,
    #    #                                'mails':[
    #    #                                         {'key':<key>, 'subject':<subject>, 'text':<text>},
    #    #                                         {...},
    #    #                                         {...}
    #    #                                         ]
    #    #                                },
    #    #                                { 'subject':<subject2>, 'mails':[{}, {}, {}]}, ... ]
#
    return render_template("test.html", list_of_entries=entry_list)


@app.route('/test_2', methods=['GET', 'POST'])
def test_2():
    # TODO: get_db_entries doesn't work properly
    list_of_entries = get_db_entries()  # Return a list of all the entries in db as dictionaries in the form of [{subject:<sub>, key:<key>, text:<text>}, {}, ... ].

    msg_dict = defaultdict(list)
    number_of_msg = 0

    # Create a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the key=subject.
        # msg_dict = { <subject1> : [{'key':<key>, 'text':<text>}, {}, ...],
        #              <subject2>: [{ }, {}, ...},
        #               ... }

        if entry['done'] == False:
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

    #number_of_msg = len(get_db_entries(done=False))

    return render_template("test_2.html", list_of_entries=entry_list, number_of_msg=number_of_msg)


@app.route('/mark_as_done/<key>', methods=['GET', 'POST'])
def mark_as_done(key):

    entry = get_entry(key)

    assert entry['key'] == key, 'wrong item'
    update = {'done': True}
    update_entry(update, key)

    return redirect(url_for('test_2'))
    #return redirect(f'{server_name}/test_2')#("https://yi0xmp.deta.dev/test_2", code=302)#f'Entry {key} removed!'#redirect(app.config['SERVER_NAME']+ '/test_2')


@app.route('/done', methods=['GET', 'POST'])
def done():
    list_of_entries = get_db_entries(done=True)
    number_of_items = (len(list_of_entries))
    msg_dict = defaultdict(list)

    # Returns a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the

    entry_list = []

    for sub, msg_list in msg_dict.items():

        dict_by_sub = {'subject':sub, 'mails':msg_list}
        entry_list.append(dict_by_sub)

    return render_template("done.html", entry_list=entry_list, number_of_items=number_of_items)


@app.route('/mark_undone/<key>', methods=['GET', 'POST'])
def mark_undone(key):

    entry = get_entry(key)
    assert entry['key'] == key, 'wrong item'

    update = {'done': False}
    update_entry(update, key)

    return redirect(url_for('done'))

    #return redirect(f'{server_name}/done')#("https://yi0xmp.deta.dev/done", code=302)#f'Entry {key} restored!'
    #return redirect(url_for('done', _external=True))
