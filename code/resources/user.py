from werkzeug.security import generate_password_hash
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

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
		user = UserModel.find_by_id(current_identity.id)
		if user and user.id != current_identity.id:
			return {"Not authorized to view this contnet"}, 401
		if user:
			return {"steam_id": user.steam_id}
		return {"message": "Steam id not found"}, 404

