from flask import Flask, request, jsonify, \
    Blueprint, g, session
from flask_restx import Resource, Api, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/')
api = Api(
    app,
    title='Social Network',
    description='The basic model of social network',
    version='1.0',
    prefix='/api/',
    ordered=True
)

app.register_blueprint(blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:jmh990@localhost:5432/NetUsers"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config.update(dict(
    DATABASE="postgresql+psycopg2://postgres:jmh990@localhost:5432/NetUsers",
    DEBUG=False,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
))

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

parser_users = reqparse.RequestParser()
parser_users.add_argument('username', type=str, help='username')
parser_users.add_argument('password', type=str, help='password')

login_fields = api.model("Users", {
    "username": fields.String,
    "password": fields.String,
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_fields)
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = Users.query.filter_by(username=username).first()
        if user is None:
            return jsonify({"error": "Username is wrong"})
        elif not user.verify_password(password):
            return jsonify({"error": "Wrong password"})
        g.user = user
        session["logged_in"] = True
        return jsonify({"success": f"User {username} - {user.user_id} was successfully logged in!"})

@api.route('/logout')
class Logout(Resource):
    def post(self):
        if session["logged_in"] == False:
            pass
        else:
            current_user = g.user.username
            session["logged_in"] = False
            return jsonify({"success": f"User - {current_user} were successfully logged out"})

@api.route('/sign-up')
class Sign_up(Resource):
    @api.expect(login_fields)
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            return jsonify({"error": "This name is already taken"})
        else:
            try:
                new_user = Users(username=username)
                new_user.hash_password(password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({"success": f"User - {new_user.username} was successfully signed up"})

            except:
                return jsonify({"error": "Something goes wrong, this user was not signed up"})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
