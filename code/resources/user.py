import sys
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity,
	create_access_token,
    create_refresh_token,
	get_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="A username is required to register."
	)

	parser.add_argument('steam_id',
		type=str,
		required=True,
		help="A steam id is required to register."
	)

	parser.add_argument('password',
		type=str,
		required=True,
		help="A password is required to register."
	)

	def post(self):
		data = UserRegister.parser.parse_args()
		
		username = data['username']
		steam_id = data['steam_id']
		password = data['password']

		if UserModel.find_by_username(username):
			return {"message": "User with that username already exists."}, 400

		if UserModel.find_by_steam_id(steam_id):
			return {"message": "User with that steam id already exists."}, 400
		
		user = UserModel(username, steam_id, generate_password_hash(password))
		user.save_to_db()
		return {"message": "User created successfully."}, 201

class UserSteamId(Resource):

	@jwt_required()
	def get(self):
		current_user_id = get_jwt_identity()
		user = UserModel.find_by_id(current_user_id)
		if user and user.id != current_user_id:
			return {"Not authorized to view this contnet"}, 401
		if user:
			return {"steam_id": user.steam_id}
		return {"message": "Steam id not found"}, 404

class UsernameExists(Resource):
	def get(self, username):
		if UserModel.find_by_username(username):
			return {"message": "User with that username already exists."}
		return {"message": "That username is currently available."}

class SteamIdExists(Resource):
	def get(self, steam_id):
		if UserModel.find_by_steam_id(steam_id):
			return {"message": "User with that steam id already exists."}
		return {"message": "That steam id is currently available."}

class UserLogin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="A username is required to register."
	)

	parser.add_argument('password',
		type=str,
		required=True,
		help="A password is required to register."
	)

	def post(self):
		data = UserLogin.parser.parse_args()

		user = UserModel.find_by_username(data['username'])

		if user and check_password_hash(user.password, data['password']):
			access_token = create_access_token(identity=user.id, fresh=True)
			refresh_token = create_refresh_token(user.id)
			return {
						'access_token': access_token,
						'refresh_token': refresh_token
					}, 200

		return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
