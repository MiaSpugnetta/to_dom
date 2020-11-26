from app import app
from flask import render_template
#from to_dom import text_email
#from deta import Deta
#from to_dom import db
from flask_config import db


@app.route('/')
@app.route('/index')
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
    return render_template("index.html", text_email=all_entries)


# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run