from flask import Flask
from flask_config import Config, server_name

# Create instance of a Flask class
app = Flask(__name__)  # The `__name__` variable passed to the Flask class is a Python predefined variable.

#####################################
# This section has been added after introducing wtf flask form. A secret key generated tokes is necessary to validate the forms.

app.config.from_object(Config)  # Import SECRET_KEY from Config class in config file.

######################################
# Import routes module
from app import routes