from src.app import db, auth
from passlib.hash import pbkdf2_sha256 as sha256
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('user', lazy='dynamic'))

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
                'email': user.email,
                'password': user.password,
                'playlists': user.playlists
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

@auth.verify_password
def verify_hash(username, password):
    user = User.get_by_username(username)
    if user and User.verify_hash(password, user.password):
        return username


@auth.get_user_roles
def get_user_roles(user):
    user_entity = User.get_by_username(user)
    return [role.name for role in user_entity.roles]


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class UsersRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

