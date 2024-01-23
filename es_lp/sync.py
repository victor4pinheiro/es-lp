from logging import error

from flask import Blueprint, Response, jsonify
from es_lp.database import connection
import requests

from es_lp.middleware.messages import format_messages

elasticsearch = connection.environments
pokeapi_bp = Blueprint("pokeapi", __name__, url_prefix="/pokeapi")


def get_size_pokemons():
    url = "https://pokeapi.co/api/v2/pokemon"
    results = get_data_json(url, only_pokemon=False)
    total = results["count"]
    return total


def get_data_json(url, only_pokemon=True) -> dict:
    with requests.get(url) as results:
        data = results.json()
    
    response = data

    if only_pokemon is True:
        response =  data.get("results", [])

    return response


def fetch_pokemon_data(limit):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    results = get_data_json(url)
    return results


def index_pokemon(index, pokemon):
    doc = {
        "name": pokemon["name"],
    }
    try:
        elasticsearch.create(index="pokemon", id=index, document=doc)
    except Exception as e:
        error(f"The {pokemon['name']} already exists! Error: {e}")


@pokeapi_bp.get("/sync")
def sync() -> Response:
    response = format_messages("Pokemon created successfully", 201)

    try:
        if elasticsearch.count(index="pokemon") != 0:
            raise Exception("Data already exists")

        limit = get_size_pokemons()
        pokemons = fetch_pokemon_data(limit)

        for index, pokemon in enumerate(pokemons):
            index_pokemon(index, pokemon)

    except Exception as e:
        error(f"Error during synchronization: {e}")
        response = format_messages("Error during synchronization", 500)
    return response
