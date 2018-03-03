from db import db

class UserModel(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	steam_id = db.Column(db.String(80))
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	def __init__(self, username, steam_id, password):
		self.steam_id = steam_id
		self.username = username
		self.password = password

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	@classmethod
	def find_by_steam_id(cls, steam_id):
		return cls.query.filter_by(steam_id=steam_id).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()