from main_init import app
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


db = app.config["db"]


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Posts(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Messages(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sender_name = db.Column(db.String(), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    recipient_name = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Friends(db.Model):
    __tablename__ = 'friends'

    pair_id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(), nullable=False)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user2 = db.Column(db.String(), nullable=False)
    user2_id = db.Column(db.Integer,  db.ForeignKey('users.user_id'), nullable=False)
