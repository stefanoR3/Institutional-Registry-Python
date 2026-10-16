from flask import Flask #from flask/__init__.py
import config #? how does he know location

#global dictionary-style object that holds all teh configurations/tools/rules to run the server.
 #name = module name(website), used to locate the actual files needed by flask (ex. templates, routes etc.)
app = Flask(__name__)

app.config.from_object(config.Config)

from app import routes #(routes.py)

#margin = outer space
#padding = inner space