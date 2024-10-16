from unittest import TestCase, mock
from src.model import Film



class TestFilm(TestCase):

    def setUp(self) -> None:
        self.film = Film(
            name='name',
            duration='100',
            state='state',
            created_at='created_at'
        )

    def test_to_json(self):
        film = self.film
        expected_json = {'created_at': 'created_at',
                         'duration': '100',
                         'name': 'name',
                         'id': None,
                         'state': 'state'}

        result = film.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        film = self.film

        mock_add.return_value = None
        mock_commit.return_value = None

        Film.save_to_db(film)

        mock_add.assert_called_once_with(film)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        film = self.film
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = film

        result = Film.get_by_id(1)

        self.assertEqual(film, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        film = self.film
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = film

        result = Film.get_by_name('name')

        self.assertEqual(film, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.film.Film.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        film = self.film
        mock_get_by_id.return_value = film
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Film.delete_by_id(1)

        self.assertEqual(film.to_json(), result)
        mock_get_by_id.assert_called_once_with(1)
        mock_query_property_getter.return_value.filter_by.assert_called_once_with(id=1)
        mock_query_property_getter.return_value.filter_by.return_value.delete.assert_called_once_with()
        mock_commit.assert_called_once_with()

    @mock.patch('src.model.film.Film.get_by_id')
    def test_delete_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Film.delete_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Film with such id does not exist.',
                                        'source': "Field 'FilmId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)
        mock_get_by_id.assert_called_once_with(1)