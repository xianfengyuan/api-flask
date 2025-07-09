from flask import Flask
from flask_smorest import Api  # or use 'from flask_restful import Api' if you use Flask-RESTful
from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBluePrint)
api.register_blueprint(StoreBluePrint)
