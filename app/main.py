from flask import Flask, render_template
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from passlib.hash import pbkdf2_sha256 as sha256
from src.error_handler.exception_wrapper import handle_error_format

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///labdb.db"
db.init_app(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(user):
            return {
                'id': user.id,
                'username': user.username,
                'first name': user.firstname,
                'last name': user.lastname,
                'email': user.email,
                'password': user.password,
            }

        return {'users': [to_json(user) for user in User.query.all()]}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, userId):
        return User.query.filter_by(id=userId).first()

    @classmethod
    def delete_by_id(cls, userId):
        try:
            user = User.get_by_id(userId)

            for playlist in user.playlists:
                playlist.delete_by_id(playlist.id)

            user_json = User.to_json(user)
            User.query.filter_by(id=userId).delete()
            db.session.commit()
            return user_json
        except AttributeError:
            return handle_error_format('User with such id does not exist.',
                                       'Field \'userId\' in path parameters.'), 404


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    duration = db.Column(db.String, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    created_at = db.Column(db.Date)

    dates = db.relationship('Schedule', backref='film')

    def __repr__(self):
        return f'<Film "{self.name}">'


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    films = db.relationship('Film', backref='status')


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/api/v1/hello-world-17')
def hello_world():
    return "Hello World 17"


@app.route('/film/<>')


@app.route('/films')
def films_list():
    films = db.session.execute(db.select(Film).order_by(Film.name)).scalars()
    return render_template("film/list.html", films=films)


if __name__ == '__main__':
    # serve(app)
    app.run(Debug=True)
