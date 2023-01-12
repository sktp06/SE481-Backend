from flask import jsonify, request
from models.bookmark import Bookmark
from flask_sqlalchemy import SQLAlchemy
import pickle
db = SQLAlchemy()
parsed_data = pickle.load(open('assets/parsed_data.pkl', 'rb'))


class BookmarkController:
    @staticmethod
    def getBookmarkByUserId():
        userId = request.get_json()['userId']
        try:
            bookmarks = db.session.query(Bookmark).filter_by(user=userId).all()
            bookmarks = Bookmark.serialize_list(bookmarks)
            if (not len(bookmarks)):
                raise
            animes = []
            for b in bookmarks:
                animes.append(parsed_data[parsed_data['mal_id'] == b['anime']].to_dict('records')[0])
            result = {'userId': userId, 'animes': animes}
            return jsonify(result)
        except:
            return jsonify({'message': 'The bookmark for userId {} is not existed'.format(userId)})

    @staticmethod
    def addBookmark():
        # NOTE: body contain userId and serialNo
        try:
            userId = request.get_json()['userId']
            animeId = request.get_json()['animeId']
            score = request.get_json()['score']
            bookmark = Bookmark(userId, animeId, score)
            try:
                db.session.add(bookmark)
                db.session.commit()
            except:
                return jsonify({'message': 'This bookmark information went wrong'}), 404
            return jsonify({'message': 'The bookmark is added successfully'})
        except:
            return jsonify({'message': 'The request body required userId, animeId and score'}), 400

    @staticmethod
    def removeBookmark():
        # NOTE: body contain userId and serialNo
        try:
            userId = request.get_json()['userId']
            animeId = request.get_json()['animeId']
            bookmark = db.session.query(Bookmark).filter_by(user=userId, anime=animeId).first()
            try:
                db.session.delete(bookmark)
                db.session.commit()
            except:
                return jsonify({'message': 'This bookmark is not existed'}), 404
            return jsonify({'message': 'The bookmark is deleted successfully'})
        except:
            return jsonify({'message': 'The request body required userId, and animeId'}), 400
