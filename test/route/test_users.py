from src.model import User, Role
from unittest import TestCase, mock
from undecorated import undecorated
from src.route import create_user, get_user_by_id, get_user_by_username, update_user_by_id, delete_user_by_id

class TestUsers(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            email='email',
            password='password'
        )

        self.user_json_create = {
            'username': 'pepega2',
            'email': 'pepega2k@gmail.com',
            'password': 'password'
        }

        self.get_user_json = {
            'email': 'email',
            'id': None,
            'password': 'password',
            'roles': [],
            'username': 'username'
        }

        self.update_user_json = {
            'username': 'username_new',
            'email': 'email'
        }

    @mock.patch('src.model.user.User.save_to_db')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.user.User.get_by_username')
    @mock.patch('src.model.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user(self, mock_request_parser, mock_generate_hash, mock_get_by_username, mock_get_by_name, mock_save_to_db):
        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'
        mock_get_by_username.return_value = False
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_save_to_db.return_value = True

        result = create_user()

        self.assertEqual(({'message': 'User was successfully created'}, 200), result)

    @mock.patch('src.model.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_email_fail(self, mock_request_parser, mock_generate_hash):
        self.user_json_create['email'] = 'invalid'

        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'Please, enter valid email address.',
                                       'source': "Field 'email' in the request body."}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.model.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_password_fail(self, mock_request_parser, mock_generate_hash):
        self.user_json_create['password'] = 'bad'

        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'Password should consist of at least 8 symbols.',
                                       'source': "Field 'password' in the request body."}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.model.user.User.get_by_username')
    @mock.patch('src.model.user.User.generate_hash')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_user_with_username_fail(self, mock_request_parser, mock_generate_hash, mock_get_by_username):
        mock_request_parser.return_value = self.user_json_create
        mock_generate_hash.return_value = 'password'
        mock_get_by_username.return_value = True

        result = create_user()

        self.assertEqual(({'errors': [{'message': 'User with such username already exists.',
                                       'source': "Field 'username' in the request body."}],
                           'traceId': result[0].get('traceId')}, 400), result)

    @mock.patch('src.model.user.User.get_by_id')
    def test_get_user_by_id(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = self.user

        undecorated_get_user_by_id = undecorated(get_user_by_id)
        result = undecorated_get_user_by_id(1)

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.model.user.User.get_by_id')
    def test_get_user_by_id_fail(self, mock_get_user_by_id):
        mock_get_user_by_id.return_value = None

        undecorated_get_user_by_id = undecorated(get_user_by_id)
        result = undecorated_get_user_by_id(1)

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
                                       'source': "Field 'userId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.model.user.User.get_by_username')
    def test_get_user_by_username(self, mock_get_by_username):
        mock_get_by_username.return_value = self.user

        undecorated_get_user_by_username = undecorated(get_user_by_username)
        result = undecorated_get_user_by_username(1)

        self.assertEqual(self.get_user_json, result)

    @mock.patch('src.model.user.User.get_by_username')
    def test_get_user_by_username_fail(self, mock_get_by_username):
        mock_get_by_username.return_value = None

        undecorated_get_user_by_username = undecorated(get_user_by_username)
        result = undecorated_get_user_by_username('None')

        self.assertEqual(({'errors': [{'message': 'User with such username does not exist.',
                                   'source': "Field \'username\' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.model.user.User.save_to_db')
    @mock.patch('src.model.user.User.get_by_id')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.user.User.get_by_username')
    @mock.patch('src.model.user.User.get_by_email')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_user_by_id(self, mock_request_parser, mock_current_user, mock_get_by_username,
                               mock_get_by_email, mock_get_by_name, mock_get_by_id, mock_save_to_db):
        mock_current_user.return_value = 'username'
        mock_request_parser.return_value = self.update_user_json
        admin = Role(id=1, name='admin')
        self.user.roles.append(admin)
        mock_get_by_name.return_value = admin
        mock_get_by_username.side_effect = [self.user, None]
        mock_get_by_email.side_effect = [self.user, None]
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_update_user_by_id = undecorated(update_user_by_id)
        result = undecorated_update_user_by_id(1)          #here

        self.get_user_json['username'] = 'username_new'

        self.assertEqual({'email': 'email',
                             'id': None,
                             'password': 'password',
                             'roles': ['admin'],
                             'username': 'username_new'}, result)

    @mock.patch('src.model.user.User.save_to_db')
    @mock.patch('src.model.user.User.get_by_id')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.user.User.get_by_username')
    @mock.patch('src.model.user.User.get_by_email')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_user_by_id_username_fail(self, mock_request_parser, mock_current_user, mock_get_by_username,
                               mock_get_by_email, mock_get_by_name, mock_get_by_id, mock_save_to_db):
        mock_current_user.return_value = 'username'
        mock_request_parser.return_value = self.update_user_json
        admin = Role(id=35151454, name='admin')
        self.user.roles.append(admin)
        mock_get_by_name.return_value = admin
        mock_get_by_username.return_value = self.user
        mock_get_by_email.return_value = self.user
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_update_user_by_id = undecorated(update_user_by_id)
        result = undecorated_update_user_by_id(1)          #here

        self.get_user_json['username'] = 'username_new'

        self.assertEqual(({'errors': [{'message': 'User with such username already exists.',
                                   'source': "Field \'username\' in the request body."}],
                           'traceId': result[0].get('traceId')}, 404), result)