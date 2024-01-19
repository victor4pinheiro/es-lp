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
    with requests.get(url) as response:
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
    except Exception as e:
        error(f"The {pokemon['name']} already exists! Error: {e}")


def sync():
    try:
        if elasticsearch.count(index="pokemon") != 0:
            raise Exception("Data already exists")

        limit = get_size_pokemons()
        pokemons = fetch_pokemon_data(limit)

        for index, pokemon in enumerate(pokemons):
            index_pokemon(index, pokemon)
    except Exception as e:
        error(f"Error during synchronization: {e}")
