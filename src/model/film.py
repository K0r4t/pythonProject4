from src.app import db
from strenum import StrEnum
from sqlalchemy import Enum
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception

class State(StrEnum):
    Done = 'Done'
    InProduction = 'InProduction'

# class Status(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)
#
#     films = db.relationship('Film', backref='status')

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    duration = db.Column(db.String(45), nullable=False)
    state = db.Column(Enum(State), nullable=False)
    # status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    created_at = db.Column(db.Date)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'state': self.state,
            'created_at': self.created_at
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, film_id):
        return cls.query.filter_by(id=film_id).first()

    @classmethod
    def get_by_name(cls, film_name):
        return cls.query.filter_by(name=film_name).first()


    @classmethod
    def delete_by_id(cls, film_id):
        film = Film.get_by_id(film_id)

        if not film:
            return handle_error_format('Film with such id does not exist.',
                                       'Field \'FilmId\' in path parameters.'), 404

        film_json = Film.to_json(film)

        cls.query.filter_by(id=film_id).delete()
        db.session.commit()

        return film_json


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
