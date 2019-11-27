from flask import Flask
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

server = Flask(__name__)
api = Flask(__name__)
#app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

from backend import routes
