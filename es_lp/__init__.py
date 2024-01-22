from flask import Flask
from flask_marshmallow import Marshmallow
from es_lp.routes import routes


app = Flask(__name__)
app.register_blueprint(routes)
ma = Marshmallow(app)


if __name__ == "__main__":
    app.run(debug=True)
