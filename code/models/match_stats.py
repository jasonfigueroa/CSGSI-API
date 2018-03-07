from db import db

class MatchStatsModel(db.Model):
    __tablename__ = 'match_stats'

    id = db.Column(db.Integer, primary_key=True)
    kills = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    mvps = db.Column(db.Integer)
    score = db.Column(db.Integer)

    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    match = db.relationship('MatchModel', back_populates='match_stats')
    

    def __init__(self, match_id, kills, assists, deaths, mvps, score):
        self.match_id = match_id
        self.kills = kills
        self.assists = assists
        self.deaths = deaths
        self.mvps = mvps
        self.score = score

    def json(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'kills': self.kills,
            'assists': self.assists, 
            'deaths': self.deaths, 
            'mvps': self.mvps, 
            'score': self.score, 
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
