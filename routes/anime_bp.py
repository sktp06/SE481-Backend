from flask import Blueprint
from controllers.animeController import AnimeController


class AnimeBlueprint:
    anime_bp = Blueprint('anime_bp', __name__, url_prefix='/anime')
    anime_bp.route('/title', methods=['POST'])(AnimeController.query_title)
    anime_bp.route('/description', methods=['POST'])(AnimeController.query_description)
