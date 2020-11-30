from app import app
from flask import redirect, render_template
from abstractions.database import get_db_entries
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
    pass

# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run