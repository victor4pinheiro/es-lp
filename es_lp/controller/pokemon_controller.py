from flask import Blueprint, request, jsonify
from es_lp.database.connection import client
from es_lp.models.pokemon import PokemonSchema

pokemon_bp = Blueprint("pokemon", __name__, url_prefix="/pokemons")


@pokemon_bp.post("/")
def create_pokemon():
    pokemon_schema = PokemonSchema()

    try:
        data = request.get_json()

        errors = pokemon_schema.validate(data)
        if errors:
            return jsonify({"message": "Validation errors", "errors": errors}), 400

        elastic_search = client
        pokemon = {"name": data["name"]}

        elastic_search.index(index="pokemon", document=pokemon)
        return jsonify({"message": "Pokemon created successfully"}), 201

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@pokemon_bp.get("/")
def list_all_pokemons():
    pokemons_schema = PokemonSchema(many=True)
    max_pokemons = int(request.args.get("limit") or 10000)
    try:
        elastic_search = client

        response = elastic_search.search(index="pokemon", size=max_pokemons)
        pokemons = response["hits"]["hits"]

        output = pokemons_schema.dump([{'_id': pokemon['_id'], 'name': pokemon['_source']['name']} for pokemon in pokemons])

        return jsonify({"pokemons": output}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
