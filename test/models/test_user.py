from unittest import TestCase, mock

from src.model import User, Role
from src.model.user import verify_hash, get_user_roles


class TestUser(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            email='email',
            password='password'
        )

    def test_to_json(self):
        user = self.user

        expected_json = {'email': 'email',
                         'id': None,
                         'username': 'username',
                         'password': 'password',
                         'roles': []
                         }

        result = user.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        user = self.user

        mock_add.return_value = None
        mock_commit.return_value = None

        User.save_to_db(user)

        mock_add.assert_called_once_with(user)
        mock_commit.assert_called_once_with()

    def test_generate_hash(self):
        user = self.user

        result = user.generate_hash('password')

        self.assertTrue(result)

    def test_verify_hash(self):
        user = self.user
        user.password = user.generate_hash('password')

        result = user.verify_hash('password', user.password)

        self.assertTrue(result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_username(self, mock_query_property_getter):
        user = self.user
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user

        result = User.get_by_username('username')

        self.assertEqual(user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_email(self, mock_query_property_getter):
        user = self.user
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user

        result = User.get_by_email('email')

        self.assertEqual(user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        user = self.user
        user.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user

        result = User.get_by_id(1)

        self.assertEqual(user, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.user.User.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        mock_get_by_id.return_value = self.user
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = User.delete_by_id('id')

        self.assertTrue(result)

    @mock.patch('src.model.user.User.get_by_id')
    def test_delete_by_identifier_with_invalid_user(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = User.delete_by_id('id')

        self.assertEqual(({'errors': [{'message': 'User with such id does not exist.',
              'source': "Field 'userId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)


class TestRole(TestCase):

    def test_to_json(self):
        role = Role(id=1, name='user')
        expected_json = {'id': 1, 'name': 'user'}

        result = role.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        role = Role(id=1, name='user')

        mock_add.return_value = None
        mock_commit.return_value = None

        Role.save_to_db(role)

        mock_add.assert_called_once_with(role)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        role = Role(id=1, name='user')
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = role

        result = Role.get_by_name('user')

        self.assertEqual(role, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        role = Role(id=1, name='user')
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = role

        result = Role.get_by_id('user')

        self.assertEqual(role, result)

    @mock.patch('src.model.user.User.verify_hash')
    @mock.patch('src.model.user.User.get_by_username')
    def test_verify_hash(self, mock_get_by_username, mock_verify_hash):
        user = User(
            username='username',
            email='email',
            password='password'
        )
        mock_get_by_username.return_value = user
        mock_verify_hash.return_value = True

        result = verify_hash('password', 'username')

        self.assertTrue(result)



    @mock.patch('src.model.user.User.get_by_username')
    def test_get_user_roles(self, mock_get_by_username):
        user = User(
            username='username',
            email='email',
            password='password'
        )
        role1 = Role(id=1, name='user')
        role2 = Role(id=2, name='admin')
        user.roles.append(role1)
        user.roles.append(role2)
        mock_get_by_username.return_value = user

        result = get_user_roles('username')

        self.assertEqual(result, ['user', 'admin'])

