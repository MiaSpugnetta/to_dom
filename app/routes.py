from app import app
from flask import render_template
#from to_dom import text_email
#from deta import Deta
#from to_dom import db
from flask_config import db
#from to_dom import dict_of_msgs  # has to be in the code, but if uncommented to_dom.py runs every time the flask app run! SHIIIIIIIIIIIIIIIITTTTTTTTT
from to_dom import get_dict_of_msg
from methods import add_to_db
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
    #deta = Deta(project_key)
    all_entries = list(db.fetch())

    print(all_entries)
    #global dict_of_msgs
    #parsed_dictionary = parse_dict(dict_of_msgs)
    ##dict_msg = parse_dict(dict_of_msgs)
    #dict_msg = generate_message(parsed_dictionary)
    #text_email = generate_message(dict_msg)
    #print(text_email)

    button = ButtonInput()
    if button.validate_on_submit():
        dict_of_msgs = get_dict_of_msg()
        add_to_db(dict_of_msgs)
        return f"""You are the favourite and your database has been updated, refresh the page!"""

    return render_template("index.html", all_entries=all_entries, form=button)


# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run