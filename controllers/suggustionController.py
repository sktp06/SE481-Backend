import pickle

from flask_sqlalchemy import SQLAlchemy

from models import Bookmark

db = SQLAlchemy()


class SuggestionController:
    parsed_data = pickle.load(open('../assets/parsed_data.pkl', 'rb'))
    rating = Bookmark.query.all()
    rating = Bookmark.serialize_list(rating)
    anime_features = ['mal_id', 'title', 'score', 'genres', 'popularity',
                      'members', 'favorites', 'rating', 'status', 'rank']

    anime = parsed_data[anime_features]
    merged_df = anime.merge(rating, left_on='mal_id', right_on='anime', how='inner')

    # genre_names = [
    #     'Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi',
    #     'Game', 'Space', 'Music', 'Mystery', 'School', 'Fantasy',
    #     'Horror', 'Kids', 'Sports', 'Magic', 'Romance',
    # ]
