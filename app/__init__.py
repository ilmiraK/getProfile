from flask import Flask
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

MONGO_URL = getenv('MONGO_URL')

client = MongoClient(MONGO_URL)

users = list(client.WeFriiendsUsers.users.find())

api = Api(app)
user_ns = api.namespace('/users')

usersModel = api.model('Users', {
    'userId': fields.String,
})


@user_ns.route('')
class UsersView(Resource):
    @api.marshal_with(usersModel, envelope='resource')
    def get(self):
        return users, 200


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        return users[bid], 200


if __name__ == '__main__':
    app.run(debug=True)
