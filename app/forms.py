# Module to store web form classes
from flask_wtf import FlaskForm  # Package requires SECRET_KEY to configure the app and protect it from CSRF.
from wtforms import SubmitField


class ButtonInput(FlaskForm):
    refresh_button = SubmitField('Refresh from database')
    done_button = SubmitField('Mark as done')
