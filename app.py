import os
from flask import Flask, jsonify
from flask_smorest import Api  # or use 'from flask_restful import Api' if you use Flask-RESTful
from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint

from flask_jwt_extended import JWTManager

from db import db

def create_app(db_url=None):
  app = Flask(__name__)

  app.config["PROPAGATE_EXCEPTIONS"] = True
  app.config["API_TITLE"] = "Stores REST API"
  app.config["API_VERSION"] = "v1"
  app.config["OPENAPI_VERSION"] = "3.0.3"
  app.config["OPENAPI_URL_PREFIX"] = "/"
  app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger_ui"
  app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
  app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
  app.config["SQLALCHEAMY_TRACK_MODIFICATIONS"] = False
  db.init_app(app)

  api = Api(app)
  app.config['JWT_SECRET_KEY'] = "jose"
  jwt = JWTManager(app)

  @jwt.invalid_token_loader
  def invalid_token_callback(error):
    return (
      jsonify({"message": "signature verification failed", "error": str(error)}),
      401
    )

  @app.before_request
  def create_tables():
    db.create_all()

  api.register_blueprint(ItemBluePrint)
  api.register_blueprint(StoreBluePrint)
  api.register_blueprint(TagBluePrint)
  api.register_blueprint(UserBluePrint)

  return app
