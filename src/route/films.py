from src.app import app, auth
from src.model.user import User
from src.model.film import State, Film
from flask_restful import reqparse
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


@app.route('/film/<userId>', methods=['POST'])
@auth.login_required(role='admin')
@handle_server_exception
def create_film(userId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('duration', help='duration cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.Done)
    parser.add_argument('created_at', help='creation date cannot be blank', required=True)

    data = parser.parse_args()
    name = data['name']
    state = State(data['state'])
    duration = data['duration']
    created_at = data['created_at']

    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 400

    film = Film(
        name=name,
        # userId=userId,
        duration=duration,
        state=state,
        created_at=created_at
    )

    try:
        film.save_to_db()

        return {'message': 'Film was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/film/<filmId>', methods=['DELETE'])
@auth.login_required(role='admin')
@handle_server_exception
def delete_film_by_id(filmId: int):
    return Film.delete_by_id(filmId)


@app.route('/film/<filmId>', methods=['GET'])
@auth.login_required(role='user')
@handle_server_exception
def get_film_by_id(filmId: int):
    film = Film.get_by_id(filmId)

    if not film:
        return handle_error_format('Film with such id does not exist.',
                                   'Field \'filmId\' in path parameters.'), 404

    return Film.to_json(film)


@app.route('/film/<filmId>', methods=['PUT'])
@auth.login_required(role='admin')
@handle_server_exception
def update_film_by_id(filmId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('duration', help='duration cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.Done)
    parser.add_argument('created_at', help='creation date cannot be blank', required=True)

    data = parser.parse_args()
    name = data['name']
    state = State(data['state'])
    duration = data['duration']
    created_at = data['created_at']

    film = Film.get_by_id(filmId)

    if not film:
        return handle_error_format('Film with such id does not exist.',
                                   'Field \'filmId\' in path parameters.'), 404

    if Film.get_by_name(name) and not (name == film.name):
        return handle_error_format('Film with such name already exists.',
                                   'Field \'name\' in the request body.'), 400

    film.name = name
    film.state = state
    film.duration = duration
    film.created_at = created_at
    film.save_to_db()

    return Film.to_json(film)
