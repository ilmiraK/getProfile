import pymongo
from flask import Flask
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
from bson import ObjectId

app = Flask(__name__)

load_dotenv()

MONGO_URL = getenv('MONGO_URL')

client = MongoClient(MONGO_URL)

api = Api(app)
profile_ns = api.namespace('/profiles')

location_fields = api.model('Location', {
    'country': fields.String,
    'city': fields.String,
})

profiles_model = api.model('Profiles', {
    '_id': fields.String,
})

profile_model = api.model('Profiles', {
    '_id': fields.String,
    'userId': fields.String,
    'gender': fields.String,
    'reason': fields.List(fields.String),
    'photos': fields.List(fields.String),
    'createdAt': fields.DateTime,
    'updatedAt': fields.DateTime,
    'dob': fields.DateTime,
    'zodiacSign': fields.String,
    'location': fields.Nested(location_fields),

})


@profile_ns.route('/<string:country>&<string:city>')
class ProfilesView(Resource):
    @api.marshal_with(profiles_model, envelope='resource')
    def get(self, country, city):
        profiles = list(client.WeFriiendsUsers.profiles.find({'location.country': country.title(),
                                                              'location.city': city.title()}).sort('createdAt',
                                                                                                   pymongo.ASCENDING))
        return profiles, 200


@profile_ns.route('/<string:uid>')
class ProfileView(Resource):
    @api.marshal_with(profile_model, envelope='resource')
    def get(self, uid):
        profile = list(client.WeFriiendsUsers.profiles.find({"_id": ObjectId(uid)}))
        return profile, 200


if __name__ == '__main__':
    app.run(debug=True)
