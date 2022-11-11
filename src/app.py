from flask import Flask
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import src.model.user
import src.model.film
import src.route.users
import src.route.films


@app.before_request
def create_tables():
    db.create_all()

if __name__ == "__app__":
    app.run()
