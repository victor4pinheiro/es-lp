from marshmallow import Schema, fields


class PokemonSchema(Schema):
    _id = fields.Str(required=False)
    name = fields.Str(required=True)

    class Meta:
        strict = True
