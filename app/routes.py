from app import app
from flask import redirect, render_template, url_for
from abstractions.database import get_db_entries, add_field, get_entry, mark_as_undone
from abstractions.dictionary_manipulation import parse_dict
from collections import defaultdict, ChainMap
from to_dom import get_dict_of_msg
from .forms import ButtonInput

#{TODO: link displayed in html
# from flask import Markup
#
#
#def linkify(text):
#    return Markup(re.sub(r'@([a-zA-Z0-9_]+)', r'<a href="/\1">@\1</a>', text))
#}

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #all_entries = list(db.fetch())

    #print(all_entries)
    #toDo: move db.fetch() to get_db_entries()-> List() in order to abstract this operation and avoid having to load db from database.py at all. This abstraction shou;d pn;y return a list of dicts (not a list of list of dictioaries)
    #all_entries = list(db.fetch())
#
    #for entry in all_entries:
    #    for dict in entry:
    #        print(dict)
    all_entries = get_db_entries()
    print(all_entries)

    button = ButtonInput()
    if button.validate_on_submit():
        #dict_of_msgs = get_dict_of_msg()
        #add_to_db(dict_of_msgs)
        get_dict_of_msg()
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
#4.2. by only takind from the DB the entries that aren't done
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

    list_of_subjects = []
    for subject in msg_dict:
       list_of_subjects.append(subject)


    entry_list = []

    for sub in list_of_subjects:
        mail_list = get_db_entries(sub)  # Fetch entries from db with specified subject
        dict_by_sub = {"subject":sub, "mails":mail_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
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


    print("THIS ##################################")
    print(entry_list)

    return render_template("test.html", list_of_entries=entry_list)

# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run


@app.route('/test_2', methods=['GET', 'POST'])
def test_2():
    list_of_entries = get_db_entries()  # Return a list of all the entries in db as dictionaries in the form of [{subject:<sub>, key:<key>, text:<text>}, {}, ... ].

    msg_dict = defaultdict(list)

    # Returns a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the

    list_of_subjects = []
    for subject in msg_dict:
        list_of_subjects.append(subject)

    entry_list = []

    for sub in list_of_subjects:
        mail_list = get_db_entries(sub)  # Fetch entries from db with specified subject
        dict_by_sub = {"subject": sub, "mails": mail_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
        entry_list.append(dict_by_sub)  # Append created dict to the list

    return render_template("test_2.html", list_of_entries=entry_list)


@app.route('/mark_as_done/<key>', methods=['GET', 'POST'])
def mark_as_done(key):
    #list_of_entries = get_db_entries()
    #for entry in list_of_entries:
    #    if entry['key'] == key:
    #            add_field(key)
    #add_field(key)
    entry = get_entry(key)
    #print(entry)
    assert entry['key'] == key, 'wrong item'
    add_field(key)
    #print(f'this is the key: {key}')
    #print(entry['subject'])
    #print(entry)

    return redirect(url_for('test_2'))


@app.route('/done', methods=['GET', 'POST'])
def done():
    list_of_entries = get_db_entries(done=True)
    #print(list_of_entries)
    msg_dict = defaultdict(list)

    # Returns a dictionary of dictionaries from the list_of_entries.
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, returns the value
        msg_dict[subject].append(entry)  # The entry becomes the value of the

    #print("^^^^^^^^^^^^^^^^^^^")
    #print(msg_dict)
    #list_of_subjects = []
    #for subject in msg_dict:
    #    list_of_subjects.append(subject)
#
    entry_list = []
    #print(list_of_subjects)
#
    for sub, msg_list in msg_dict.items():
        #print(f'this is sub {sub}, this is list {msg_list}')
        dict_by_sub = {'subject':sub, 'mails':msg_list}
        entry_list.append(dict_by_sub)
        #print(f'this is the dict {dict_by_sub}, \n \n\nthis is the list{entry_list}')
        #for mail_list
        #for

#    for sub in list_of_subjects:
#        mail_list = get_db_entries(sub)  # Fetch entries from db with specified subject
#        dict_by_sub = {"subject": sub, "mails": mail_list}  # Create dict with key:sub and key:[list of all {entries} that have that subject]
#        entry_list.append(dict_by_sub)  # Append created dict to the list
#    #print(entry_list)
#    #for entry in entry_list:
#        #print(entry)

    return render_template("done.html", entry_list=entry_list)


@app.route('/mark_as_undone/<key>', methods=['GET', 'POST'])
def mark_as_undone(key):

    entry = get_entry(key)
    #print(entry)
    assert entry['key'] == key, 'wrong item'
    print(entry)
    print(key)
    mark_as_undone(key)
    #print(f'this is the key: {key}')
    #print(entry['subject'])
    #print(entry)

    return redirect(url_for('done'))