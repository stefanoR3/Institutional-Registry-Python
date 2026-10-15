from flask import Flask #from flask/__init__.py
import config

app = Flask(__name__)
app.config.from_object(config.Config)

from app import routes #(routes.py)

