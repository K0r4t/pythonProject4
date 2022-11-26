from flask import Flask
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

load_dotenv()
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:14481337@localhost/mycinema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_request
def create_tables():
    #db.drop_all()
    db.create_all()
    db.session.commit()

db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

#import src.model.user
#import src.model.film
#import src.route.users
#import src.route.films


@app.route("/api/v1/hello-world-17")
@auth.login_required(role='admin')
def hello():
    return "Hello World 17"


if __name__ == "__app__":
    app.run()
