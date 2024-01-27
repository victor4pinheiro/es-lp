GET http://www.localhost:5000/api/pokemons/search?size=10&name=demon
HTTP 200

GET http://www.localhost:5000/api/pokemons/search?size=100&match=phrase_prefix&name=cha
HTTP 200

GET http://www.localhost:5000/api/pokemons/search?size=100&match=all&name=charmander
HTTP 200

GET http://www.localhost:5000/api/pokemons/search?size=100&match=all&name=cha
HTTP 200
[Asserts]
jsonpath "$.message.pokemons" count == 0

GET http://www.localhost:5000/api/pokemons/search?size=100&match=match&name=charmander
