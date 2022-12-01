from unittest import TestCase, mock
from src.model import User, Role
from src.model import Film, State
from undecorated import undecorated

from src.route import create_film, update_film_by_id, get_film_by_id

class TestFilms(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            email='email',
            password='password'
        )

        self.film = Film(
            name='name',
            duration='100',
            created_at='created_at',
            state='Done'
        )

        self.film_new = Film(
            name='name2',
            duration='110',
            created_at='created_at2',
            state='Done2'
        )

        self.user_role = Role(
            id=1,
            name='user'
        )

        self.admin_role = Role(
            id=2,
            name='admin'
        )

        self.user.roles.append(self.user_role)

    @mock.patch('src.model.Film.save_to_db')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.User.get_by_id')
    @mock.patch('src.model.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_create_film(self, mock_request_parser, mock_current_user, mock_get_by_name,
                         mock_get_by_username, mock_get_by_id, mock_save_to_db):
        #mock_current_user.return_value = 'username'
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_request_parser.return_value = self.film
        mock_get_by_id.return_value = self.user
        mock_get_by_username.return_value = self.user
        mock_save_to_db.return_value = True

        undecorated_create_film = undecorated(create_film)
        result = undecorated_create_film(1)

        self.assertEqual(({'message': 'Film was successfully created'}, 200), result)

    @mock.patch('src.model.Film.save_to_db')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.Film.get_by_id')
    @mock.patch('src.model.Film.get_by_name')
    @mock.patch('src.model.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_update_film_by_id(self, mock_request_parser, mock_get_by_name,
                         mock_get_by_film_name, mock_get_by_username, mock_get_by_film_id, mock_save_to_db):
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_request_parser.return_value = Film.to_json(self.film)
        mock_get_by_film_id.return_value = self.film
        mock_get_by_film_name.return_value = None
        mock_get_by_username.return_value = self.film_new
        mock_save_to_db.return_value = True

        undecorated_update_film_by_id = undecorated(update_film_by_id)
        result = undecorated_update_film_by_id(1)

        self.assertEqual(self.film_new.to_json(), result)

    @mock.patch('src.model.Film.save_to_db')
    @mock.patch('src.model.user.Role.get_by_name')
    @mock.patch('src.model.Film.get_by_id')
    @mock.patch('src.model.Film.get_by_name')
    @mock.patch('src.model.User.get_by_username')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_get_film_by_id(self, mock_request_parser, mock_get_by_name,
                         mock_get_by_film_name, mock_get_by_username, mock_get_by_film_id, mock_save_to_db):
        mock_get_by_name.return_value = Role(id=1, name='user')
        mock_request_parser.return_value = Film.to_json(self.film)
        mock_get_by_film_id.return_value = self.film
        mock_get_by_film_name.return_value = None
        mock_get_by_username.return_value = self.film_new
        mock_save_to_db.return_value = True

        undecorated_update_film_by_id = undecorated(get_film_by_id)
        result = undecorated_update_film_by_id(1)

        self.assertEqual(self.film_new.to_json(), result)

