from app import app
from flask import redirect, render_template
from abstractions.database import get_db_entries, get_db_entries_by_category
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
    list_of_entries = get_db_entries()
    #parsed_dict = parse_dict(msg_dict)
    #msg_dict = defaultdict
    print(list_of_entries)
    print(type(list_of_entries))
    msg_dict = defaultdict(list)
    #msg_dict = {k:v for e in list_of_entries for k,v in e.items()}# for (k,v) in e.items()}

    #msg_dict = dict(enumerate(list_of_entries))

    #msg_dict=ChainMap(*list_of_entries)

    #msg_dict = { {get_key(): {k:v}} for e in list_of_entries for k,v in e.items()}

    #keys: ['mia','is','the','favourite']
    #values: [True, True, True, True]
    #new_dict = {k:v for k,v in zip(keys, values)} -> dictionary

    #for entry in list_of_entries:
    #    msg_dict.update(entry)

    #for entry in list_of_entries:
    #    key = entry['key']
    #    msg_dict[key] = entry

    # Returns a dictionary of dictionary from the list_of_entries
    for entry in list_of_entries:
        subject = entry.pop('subject')  # Pops the key from the inner dict, so that it's just the key and the dict is the value
        msg_dict[subject].append(entry)  # The entry becomes the value


    #dict[new_key] = new_value
    #list.append(new_value)

    #new_dict = { {entry[key]:entry} for entry in list_of_dicts }

    print("####################################")
    print(msg_dict)

    list_of_subjects = []
    for subject in msg_dict:
        list_of_subjects.append(subject)

    print(list_of_subjects)


    #parsed_dict = defaultdict(list)
    #for id in msg_dict:
    #    append_dict = {'id':id, 'text':msg_dict[id]['text']}
    #    parsed_dict[msg_dict[id]['subject']].append(append_dict)
    #print(parsed_dict)
#
    return render_template("test.html", msg_dict=msg_dict)

# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run