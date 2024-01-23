from logging import error
from flask import Blueprint, Response, request
from es_lp.database.connection import client as elastic_search
from es_lp.middleware.messages import format_messages
from es_lp.models.pokemon import PokemonSchema

pokemon_bp = Blueprint("pokemon", __name__, url_prefix="/pokemons")


@pokemon_bp.post("/")
def create_pokemon() -> Response:
    pokemon_schema = PokemonSchema()
    data = request.get_json()
    errors = pokemon_schema.validate(data)
    response = None

    if errors:
        response = format_messages(messages={"type": "Validation errors", "errors": errors}, status=400)
    else:
        try:
            pokemon = {"name": data["name"]}
            elastic_search.index(index="pokemon", document=pokemon)
            response = format_messages("Pokemon created successfully", 201)
        except Exception as e:
            error({"message": f"Error: {str(e)}"})
            response = format_messages("Pokemon created successfully", 500)

    return response


@pokemon_bp.get("/")
def list_all_pokemons() -> Response:
    pokemons_schema = PokemonSchema(many=True)
    max_pokemons = int(request.args.get("limit") or 10000)
    response = None

    try:
        search_response = elastic_search.search(index="pokemon", size=max_pokemons)
        pokemons = search_response["hits"]["hits"]
        output = pokemons_schema.dump(
            [
                {"_id": pokemon["_id"], "name": pokemon["_source"]["name"]}
                for pokemon in pokemons
            ]
        )
        response = format_messages({"pokemons": output}, 200)
    except Exception as e:
        response = format_messages(f"Error: {str(e)}", 500)

    return response
