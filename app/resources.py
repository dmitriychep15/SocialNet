from flask import request, jsonify, g, session
from flask_restx import Resource

from flask_restx import Api
from .models import *
from .parsers import LoginParser, PostParser
# from . import db
from main_init import api, db


# api = Api(
#     app,
#     title='Social Network',
#     description='The basic model of social network',
#     version='1.0',
#     prefix='/api/',
#     ordered=True
# )


@api.route('/login')
class Login(Resource):
    @api.expect(LoginParser)
    def post(self):
        if session["logged_in"] is True:
            return jsonify({"error": "U need to log out before"})
        else:
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
        if session["logged_in"] is False:
            pass
        else:
            current_user = g.user.username
            session["logged_in"] = False
            return jsonify({"success": f"User - {current_user} were successfully logged out"})

@api.route('/sign_up')
class SignUp(Resource):
    @api.expect(LoginParser)
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

@api.route('/posts')
class Posts(Resource):
    @api.expect(PostParser)
    def post(self):
        if session["logged_in"] is False:
            return jsonify({"error": "U are not logged in"})
        else:
            title = request.json["title"]
            text = request.json["text"]
            new_post = Posts(title=title, text=text, author_id=g.user.users.user_id)
            db.session.add(new_post)
            db.session.commit()
            return jsonify({"success": f"New post - {title} was successfully created"})

    def get(self):
        if session["logged_in"] is False:
            return jsonify({"error": "U are not logged in"})
        else:
            posts = Posts.query.filter_by(author_id=g.user.user_id).order_by(Posts.date.desc()).all()
            return jsonify({
                "posts": {
                    article: {
                        "id": article.post_id, "text": article.text, "date": article.date.date()} for article in posts
                }
            })

    @api.expect(PostParser)
    def delete(self):
        if session["logged_in"] is False:
            return jsonify({"error": "U are not logged in"})
        else:
            id = request.json["id"]
            post = Posts.query.filter_by(post_id=id).first()
            db.session.delete(post)
            db.session.commit()
            return jsonify({"success": f"Post {id} was successfully deleted"})