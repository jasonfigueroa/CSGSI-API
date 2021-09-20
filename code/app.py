from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from blacklist import BLACKLIST
from resources.user import (
	TokenRefresh,
	UserLogin,
	UserLogout,
	UserRegister,
	UserSteamId,
	UsernameExists,
	SteamIdExists
)
from resources.match import Match, MatchList
from resources.match_stats import MatchStats

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'test' # omit this line if publishing this source code to a 
						# public location
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:5025", "http://localhost:50312"]}})
# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:50312"}})
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5000"]}})
api = Api(app)

app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens

jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

# JWT configuration ends

@app.before_first_request
def create_tables():
	db.create_all()

api.add_resource(UserRegister, '/register')
api.add_resource(UserSteamId, '/user/steamid')
api.add_resource(UsernameExists, '/usernameexists/<username>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(SteamIdExists, '/steamidexists/<steam_id>')
api.add_resource(Match, '/match', '/match/<_id>')
api.add_resource(MatchList, '/match/list')
api.add_resource(MatchStats, '/matchstats', '/matchstats/<_id>')

if __name__ == '__main__':
	from db import db # Should I move this to the top of this file?
	db.init_app(app)
	app.run(host="localhost", port=3000, debug=True)