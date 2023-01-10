from flask import request, jsonify
from spellchecker import SpellChecker
import pickle
import pandas as pd

spell = SpellChecker(language='en')
bm25_title = pickle.load(open('utils/bm25_title.pkl', 'rb'))
bm25_synopsis = pickle.load(open('utils/bm25_synopsis.pkl', 'rb'))
parsed_data = pickle.load(open('assets/parsed_data.pkl', 'rb'))


class AnimeController:
    @staticmethod
    def query_title():
        query = request.args['query']
        spell_corr = [spell.correction(w) for w in query.split()]
        score = bm25_title.transform(query)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=10)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'content': df_bm.to_dict('records')}), 200

    @staticmethod
    def query_description():
        query = request.json['query']
        spell_corr = [spell.correction(w) for w in query.split()]
        score = bm25_synopsis.transform(query)
        df_bm = pd.DataFrame(data=parsed_data)
        df_bm['bm25'] = list(score)
        df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
        df_bm = df_bm.nlargest(columns='bm25', n=10)
        df_bm = df_bm.drop(columns='bm25', axis=1)
        return jsonify({'query': query, 'spell_corr': spell_corr, 'content': df_bm.to_dict('records')}), 200
