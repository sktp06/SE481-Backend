from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy_utils.functions import database_exists, create_database
from routes.auth_bp import AuthBlueprint
from routes.bookmark_bp import BookmarkBlueprint

from models.database import db
from utils.bm25 import BM25
from spellchecker import SpellChecker
import pickle
import pandas as pd

spell = SpellChecker(language='en')
parsed_data = pickle.load(open('assets/parsed_data.pkl', 'rb'))
bm25_title = pickle.load(open('utils/bm25_title.pkl', 'rb'))
bm25_synopsis = pickle.load(open('utils/bm25_synopsis.pkl', 'rb'))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config.from_object('config')

if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    print('Creating a database')
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(AuthBlueprint.auth_bp)
app.register_blueprint(BookmarkBlueprint.bookmark_bp)


@app.route('/anime/title', methods=['POST'])
def query_title():
    query = request.args['query']
    spell_corr = [spell.correction(w) for w in query.split()]
    score = bm25_title.transform(query)
    df_bm = pd.DataFrame(data=parsed_data)
    df_bm['bm25'] = list(score)
    df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
    df_bm = df_bm.nlargest(columns='bm25', n=10)
    df_bm = df_bm.drop(columns='bm25', axis=1)
    return df_bm.to_json(orient='records')


@app.route('/anime/description', methods=['POST'])
def query_description():
    query = request.args['query']
    spell_corr = [spell.correction(w) for w in query.split()]
    score = bm25_synopsis.transform(query)
    df_bm = pd.DataFrame(data=parsed_data)
    df_bm['bm25'] = list(score)
    df_bm['rank'] = df_bm['bm25'].rank(ascending=False)
    df_bm = df_bm.nlargest(columns='bm25', n=10)
    df_bm = df_bm.drop(columns='bm25', axis=1)
    return df_bm.to_json(orient='records')


@app.route('/correction', methods=['GET'])
def correction():
    query = request.args['query']
    spell_corr = [spell.correction(w) for w in query.split()]
    if spell_corr[0] == None:
        return 'No correction'
    return jsonify(' '.join(spell_corr))


@app.route('/suggestion', method=['GET'])
def predict_anime():
    return


if __name__ == '__main__':
    app.run(debug=False)
