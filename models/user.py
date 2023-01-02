from .database import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    anime_id = db.Column(db.Integer, nullable=True)

    def __init__(self, username, password, anime_id):
        self.username = username
        self.password = password
        self.anime_id = anime_id

    # แปลงค่า ส่งต่อ จัดเก็บ ให้อ่านได้คร๊าบบ
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'anime_id': self.anime_id
        }

