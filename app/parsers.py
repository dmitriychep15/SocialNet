from flask_restx import fields

from main_init import api


LoginParser = api.model("Users", {
    "username": fields.String,
    "password": fields.String,
})


PostParser = api.model("Posts", {
    "title": fields.String,
    "text": fields.String,
    "id": fields.Integer,
})