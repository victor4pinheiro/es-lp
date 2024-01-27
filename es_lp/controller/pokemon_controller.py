from logging import error
from flask import Blueprint, Response, request
from elasticsearch_dsl import Search, Q
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
        response = format_messages(
            messages={"type": "Validation errors", "errors": errors}, status=400
        )
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

@pokemon_bp.get("/search")
def search_pokemons():
    dynamic_queries = request.args.to_dict()
    size = request.args.get("size", 10000, type=int)

    if "size" in dynamic_queries:
        del dynamic_queries["size"]

    try:
        query = build_dynamic_query(dynamic_queries)
        s = (
            Search(using=elastic_search, index="pokemon")
            .query(query)
            .source(["_id", "name"])
            .extra(size=size)
        )
        response = s.execute()
    except Exception as e:
        return format_messages(f"Error: {str(e)}", 400)

    results = []
    for hit in response:
        results.append(
            {
                "_id": hit.meta.id,
                "name": hit.name,
            }
        )

    return format_messages({"pokemons": results}, 200)


def build_dynamic_query(query_params):
    query = Q()
    tmp_match = None

    try:
        for field, value in query_params.items():
            if field == "match":
                if field == "all" or field == "match":
                    tmp_match = None
                else:
                    tmp_match = value
            else:
                if tmp_match:
                    query &= Q(f"match_{tmp_match}", **{field: value})
                else:
                    query &= Q("match", **{field: value})
    except Exception as e:
        return format_messages(f"Error: {str(e)}", 404)

    return query
