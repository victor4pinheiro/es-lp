from flask import Blueprint
from es_lp.controller.pokemon_controller import pokemon_bp
from es_lp.sync import pokeapi_bp

routes = Blueprint('route', __name__, url_prefix='/api')
routes.register_blueprint(pokemon_bp)
routes.register_blueprint(pokeapi_bp)
