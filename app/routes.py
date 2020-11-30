from app import app
from flask import render_template
from flask_config import db
from to_dom import get_dict_of_msg
# from methods import add_to_db
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
    all_entries = list(db.fetch())

    print(all_entries)

    button = ButtonInput()
    if button.validate_on_submit():
        #dict_of_msgs = get_dict_of_msg()
        #add_to_db(dict_of_msgs)
        get_dict_of_msg()
        return f"""You are the favourite and your database has been updated, refresh the page!"""

    return render_template("index.html", all_entries=all_entries, form=button)


# TODO:
# refresh db(POST)
# if press button:
# to_dom.py run