from logging import error
from database import connection
import requests

elasticsearch = connection.client

def get_size_pokemons():
    url = "https://pokeapi.co/api/v2/pokemon"
    results = get_data_json(url, only_pokemon=False)
    total = results["count"]
    return total


def get_data_json(url, only_pokemon=True) -> dict:
    response = requests.get(url)
    data = response.json()
    if only_pokemon is True:
        return data.get("results", [])
    return data


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
    except Exception:
        error(f"The {pokemon["name"]} already exists!")


def sync():
    limit = get_size_pokemons()
    pokemons = fetch_pokemon_data(limit)

    for index, pokemon in enumerate(pokemons):
        index_pokemon(index, pokemon)
