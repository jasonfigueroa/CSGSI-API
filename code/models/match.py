from db import db

class MatchModel(db.Model):
    __tablename__ = 'match'

    id = db.Column(db.Integer, primary_key=True)
    datetime_start = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    map_name = db.Column(db.String(80))
    team = db.Column(db.String(80))
    round_win_team = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('UserModel')

    match_stats = db.relationship('MatchStatsModel', uselist=False, back_populates='match')
    
    def __init__(self, user_id, datetime_start, minutes_played, map_name, team, round_win_team):
        self.user_id = user_id
        self.datetime_start = datetime_start
        self.minutes_played = minutes_played
        self.map_name = map_name
        self.team = team
        self.round_win_team = round_win_team

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'datetime_start': self.datetime_start,
            'minutes_played': self.minutes_played,
            'map_name': self.map_name,
            'team': self.team,
            'round_win_team': self.round_win_team
        }

    @classmethod
    def find_by_id(cls, _id, user_id):
        subquery = cls.query.filter_by(id=_id)
        return subquery.filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
