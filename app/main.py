from flask import Flask, render_template
from waitress import serve
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///labdb.db"
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


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


@app.route('/user/<int:id>')
def user_info():
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route('/films')
def films_list():
    films = db.session.execute(db.select(Film).order_by(Film.name)).scalars()
    return render_template("film/list.html", films=films)


if __name__ == '__main__':
    serve(app)
