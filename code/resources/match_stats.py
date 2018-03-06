from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.match_stats import MatchStatsModel

class MatchStats(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('match_id',
        type=int,
        required=True,
        help="A match id is required"
    )

    parser.add_argument('kills',
        type=int,
        required=True,
        help="Total kills are required"
    )

    parser.add_argument('round_kills',
        type=int,
        required=True,
        help="Round kills are required"
    )

    parser.add_argument('round_killhs',
        type=int,
        required=True,
        help="Round kill headshots are required"
    )

    parser.add_argument('assists',
        type=int,
        required=True,
        help="Total assists are required"
    )
    
    parser.add_argument('deaths', 
        type=int,
        required=True,
        help="Total deaths are required"
    )

    parser.add_argument('mvps',
        type=int,
        required=True,
        help="Total MVPs required"
    )

    parser.add_argument('score',
        type=int,
        required=True,
        help="The score is required"
    )

    @jwt_required()
    # def get(self, _id):
    #     match_stats = MatchStatsModel.find_by_id(_id, current_identity.id)
    #     if match_stats and current_identity.id != match_stats.user_id:
    #         return {"message": "Not authorized to view this content"}, 401
    #     if match_stats:
    #         return match_stats.json()
    #     return {"message": "Match stats not found."}, 404
    def get(self, _id):
        match_stats = MatchStatsModel.find_by_id(_id)
        if match_stats:
            return match_stats.json()
        return {"message": "Match stats not found."}, 404

    @jwt_required()
    def post(self):
        data = MatchStats.parser.parse_args()
        
        match_id = data['match_id']
        kills = data['kills']
        round_kills = data['round_kills']
        round_killhs = data['round_killhs']
        assists = data['assists']
        deaths = data['deaths']
        mvps = data['mvps']
        score = data['score']

        match_stats = MatchStatsModel(
            match_id,
            kills,
            round_kills,
            round_killhs,
            assists,
            deaths,
            mvps,
            score
        )
        
        try:
            match_stats.save_to_db()
        except:
            return {"message": "An error occurred while storing the match stats"}, 500

        return match_stats.json(), 201

# class MatchStatsList(Resource):
#     @jwt_required()
#     def get(self):
#         match_stats = [match_stats.json() for match_stats in MatchStatsModel.query.all() if match_stats.user_id == current_identity.id]

#         return {"match_stats": match_stats}
