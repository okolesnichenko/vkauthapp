from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    token = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))