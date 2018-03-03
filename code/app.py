from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister
from resources.match_stats import MatchStats, MatchStatsList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test' # omit this line if publishing this source code to a 
						# public location
app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:5025", "http://localhost:50312"]}})
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:50312"}})
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')
api.add_resource(MatchStats, '/matchstats', '/matchstats/<_id>')
api.add_resource(MatchStatsList, '/matchstats/list')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True)