from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)

from views import *

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8888)