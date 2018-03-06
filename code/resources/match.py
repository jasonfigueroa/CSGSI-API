from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.match import MatchModel

class Match(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('datetime_start',
        type=int,
        required=True,
        help="A start datetime is required"
    )

    parser.add_argument('minutes_played',
        type=int,
        required=True,
        help="Total minutes played for the match is required"
    )

    parser.add_argument('map_name',
        type=str,
        required=True,
        help="A map name is required"
    )

    parser.add_argument('team',
        type=str,
        required=True,
        help="The player's team is required"
    )

    parser.add_argument('round_win_team',
        type=str,
        required=True,
        help="The team that won the match is required"
    )

    @jwt_required()
    def get(self, _id):
        match = MatchModel.find_by_id(_id, current_identity.id)
        if match and current_identity.id != match.user_id:
            return {"message": "Not authorized to view this content"}, 401
        if match:
            return match.json()
        return {"message": "Match not found"}, 404

    @jwt_required()
    def post(self):
        data = Match.parser.parse_args()

        datetime_start = data['datetime_start']
        minutes_played = data['minutes_played']
        map_name = data['map_name']
        team = data['team']
        round_win_team = data['round_win_team']

        user_id = current_identity.id        

        match = MatchModel(
            user_id,
            datetime_start,
            minutes_played,
            map_name,
            team,
            round_win_team
        )

        try:
            match.save_to_db()
        except:
            return {"message": "An error occurred while storing the match stats"}, 500

        return match.json(), 201

class MatchList(Resource):
    @jwt_required()
    def get(self):
        matches = [match.json() for match in MatchModel.query.all() if match.user_id == current_identity.id]

        return {"matches": matches}
