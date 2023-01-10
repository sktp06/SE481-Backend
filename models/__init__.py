import bcrypt
from models.user import User
from models.bookmark import Bookmark
from sqlalchemy import event
from .database import db


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(User(username='kuromi06', password=bcrypt.hashpw('123456Eiei'.encode('utf-8'),bcrypt.gensalt(10)),anime_id=None))
    db.session.commit()

@event.listens_for(Bookmark.__table__, 'after_create')
def create_bookmark(*args, **kwargs):
    db.session.add(Bookmark(user=1, anime=1, score=1))
    db.session.add(Bookmark(user=1, anime=21, score=10))
    db.session.add(Bookmark(user=1, anime=20, score=100))
    db.session.commit()