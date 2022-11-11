from src.app import app
from src.model.user import User
from flask_restful import reqparse
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


@app.route('/user/create', methods=['POST'])
@handle_server_exception
def create_user():
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank', required=True)
    parser.add_argument('email', help='email cannot be blank', required=True)
    parser.add_argument('password', help='password cannot be blank', required=True)

    data = parser.parse_args()
    username = data['username']
    email = data['email']

    if '@' not in email:
        return handle_error_format('Please, enter valid email address.', 'Field \'email\' in the request body.'), 400

    if User.get_by_username(username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    user = User(
        username=username,
        email=email,
        password=User.generate_hash(data['password'])
    )

    try:
        user.save_to_db()

        return {'message': 'User was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/user/<userId>', methods=['GET'])
@handle_server_exception
def get_user_by_id(userId: int):
    user = User.get_by_id(userId)
    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404
    return User.to_json(user)


@app.route('/user/name/<username>', methods=['GET'])
@handle_server_exception
def get_user_by_username(username: str):
    user = User.get_by_username(username)
    if not user:
        return handle_error_format('User with such username does not exist.',
                                   'Field \'username\' in path parameters.'), 404
    return User.to_json(user)


@app.route('/user/<userId>', methods=['PUT'])
@handle_server_exception
def update_user_by_id(userId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('username', help='username cannot be blank', required=True)
    parser.add_argument('email', help='email cannot be blank', required=True)

    data = parser.parse_args()
    username = data['username']
    email = data['email']

    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 404

    if User.get_by_username(username) and not (username == user.username):
        return handle_error_format('User with such username already exists.',
                                   'Field \'username\' in the request body.'), 400

    if User.get_by_email(email) and not (email == user.email):
        return handle_error_format('User with such email already exists.',
                                   'Field \'email\' in the request body.'), 400

    user.username = username
    user.email = email
    user.save_to_db()

    return User.to_json(user)


@app.route('/user/<userId>', methods=['DELETE'])
@handle_server_exception
def delete_user_by_id(userId: int):
    return User.delete_by_id(userId)
