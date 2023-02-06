from flask import Flask

from lib.config import Config

app = Flask(__name__)
Config.setup("flask")
app.config.update(Config.service)

from app import routes
