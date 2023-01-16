from flask import Blueprint
from controllers.suggustionController import SuggestionController

class SuggestionBlueprint:
    suggestion_bp = Blueprint('suggestion_bp', __name__, url_prefix='/suggestion')
    suggestion_bp.route('/', methods=['POST'])(SuggestionController.getSuggestionByUserId)