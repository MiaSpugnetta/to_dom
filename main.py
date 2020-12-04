# File necessary for Deta deployment, exp_app.py copy
# Import all the application instance
from app import app

app.config["DEBUG"] = True #'https://yi0xmp.deta.dev/'


# Fully working, basic web app structured as following:

# exp_app\
#    virtualenv\ here absent because created with conda
#    app\
#       __init__.py
#       routes.py
#    exp_app.py (main.py)

