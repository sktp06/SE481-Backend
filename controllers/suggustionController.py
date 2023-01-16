import pickle

import numpy as np
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import seaborn as sns



from models import Bookmark

db = SQLAlchemy()


class SuggestionController:
    @staticmethod
    def getSuggestionByUserId():
        parsed_data = pickle.load(open('assets/parsed_data.pkl', 'rb'))
        rating = Bookmark.query.all()
        rating = Bookmark.serialize_list(rating)
        rating = pd.DataFrame(rating)
        anime_features = ['mal_id', 'title', 'score', 'genres', 'popularity',
                          'members', 'favorites', 'rating', 'status', 'rank']

        anime = parsed_data[anime_features]
        merged_df = anime.merge(rating, left_on='mal_id', right_on='anime', how='inner')
        print(merged_df)

        genre_names = [
            'Action', 'Adventure', 'Comedy', 'Drama', 'Sci-Fi',
            'Game', 'Space', 'Music', 'Mystery', 'School', 'Fantasy',
            'Horror', 'Kids', 'Sports', 'Magic', 'Romance',
        ]

        def genre_to_category(df):
            '''Add genre category column
            '''
            d = {name: [] for name in genre_names}

            def f(row):
                genres = row.genres.split(',')
                for genre in genre_names:
                    if genre in genres:
                        d[genre].append(1)
                    else:
                        d[genre].append(0)

            # create genre category dict
            df.apply(f, axis=1)
            # add genre category
            genre_df = pd.DataFrame(d, columns=genre_names)
            df = pd.concat([df, genre_df], axis=1)
            return df

        def make_anime_feature(df):
            # add genre category columns
            df = genre_to_category(df)

            return df

        def preprocess(merged_df):
            merged_df = make_anime_feature(merged_df)
            # merged_df = make_user_feature(merged_df)
            return merged_df

        merged_df = preprocess(merged_df)
        merged_df = merged_df.drop(['mal_id', 'genres'], axis=1)
        fit, blindtest = train_test_split(merged_df, test_size=0.2, random_state=0)
        fit_train, fit_test = train_test_split(fit, test_size=0.3, random_state=0)
        features = ['popularity', 'members', 'favorites', 'rank']

        features += genre_names
        user_col = 'user'
        item_col = 'anime'
        target_col = 'score_y'

        fit_train = fit_train.sort_values('user').reset_index(drop=True)
        fit_test = fit_test.sort_values('user').reset_index(drop=True)
        blindtest = blindtest.sort_values('user').reset_index(drop=True)

        # model query data
        fit_train_query = fit_train[user_col].value_counts().sort_index()
        fit_test_query = fit_test[user_col].value_counts().sort_index()
        blindtest_query = blindtest[user_col].value_counts().sort_index()
        model = lgb.LGBMRanker()
        print(fit_train[target_col])
        print(fit_test[target_col])
        model.fit(
            fit_train[features],
            fit_train[target_col],
            group=fit_train_query,
            eval_set=[(fit_test[features], fit_test[target_col])],
            eval_group=[list(fit_test_query)],
            eval_at=[1, 3, 5, 10],  # calc validation ndcg@1,3,5,10
            early_stopping_rounds=100,
            verbose=10
        )

        pickle.dump(model, open('assets/model.pkl', 'wb'))
        model.predict(blindtest.iloc[:10][features])

        def predict(user_df, top_k, anime, rating):
            user_anime_df = anime.merge(user_df, left_on='mal_id', right_on='anime')
            user_anime_df = make_anime_feature(user_anime_df)

            excludes_genres = list(np.array(genre_names)[np.nonzero([user_anime_df[genre_names].sum(axis=0) <= 1])[1]])

            pred_df = make_anime_feature(anime.copy())
            pred_df = pred_df.loc[pred_df[excludes_genres].sum(axis=1) == 0]

            for col in user_df.columns:
                if col in features:
                    pred_df[col] = user_df[col].values[0]

            preds = model.predict(pred_df[features])

            topk_idx = np.argsort(preds)[::-1][:top_k]

            recommend_df = pred_df.iloc[topk_idx].reset_index(drop=True)

            # check recommend
            print('---------- Recommend ----------')
            for i, row in recommend_df.iterrows():
                print(f'{i + 1}: {row["title"]}')

            print('---------- Rated ----------')
            user_df = user_df.merge(anime, left_on='anime', right_on='mal_id', how='inner')
            for i, row in user_df.sort_values('score_x', ascending=False).iterrows():
                print(f'score:{row["score_x"]}: {row["title"]}')
            return recommend_df

        user_id = 1
        user_df = rating.copy().loc[rating['user'] == user_id]
        # user_df = make_user_feature(user_df)
        predict(user_df, 5, anime, rating)


