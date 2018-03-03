from db import db

class MatchStatsModel(db.Model):
    __tablename__ = 'match_stats'

    id = db.Column(db.Integer, primary_key=True)
    map_played = db.Column(db.String(80))
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mvps = db.Column(db.Integer)
    score = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')

    def __init__(self, user_id, map_played, kills, assists, deaths, mvps, score, minutes_played):
        self.user_id = user_id
        self.map_played = map_played
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.mvps = mvps
        self.score = score
        self.minutes_played = minutes_played

    def json(self):
        return {
            'id': self.id, 
            'map': self.map_played, 
            'kills': self.kills, 
            'assists': self.assists, 
            'deaths': self.deaths, 
            'mvps': self.mvps, 
            'score': self.score, 
            'minutes_played': self.minutes_played
        }

    @classmethod
    def find_by_id(cls, _id, user_id):
        subquery = cls.query.filter_by(id=_id)
        return subquery.filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()