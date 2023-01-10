from .database import db


class Bookmark(db.Model):
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    anime = db.Column(db.Integer, nullable=False, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, user, anime, score):
        self.user = user
        self.anime = anime
        self.score = score

    @property
    def serialize(self):
        return {
            'user': self.user,
            'anime': self.anime,
            'score': self.score
        }

    @staticmethod
    def serialize_list(list):
        return [m.serialize for m in list]