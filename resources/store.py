from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema

from models import StoreModel
from db import db

blp = Blueprint("stores", __name__, description="store operations")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
  @blp.response(200, StoreSchema)
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store

  def delete(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return {"message": "store deleted"}

@blp.route("/store")
class StoreList(MethodView):
  @blp.response(200, StoreSchema(many=True))
  def get(self):
    return StoreModel.query.all()

  @blp.arguments(StoreSchema)
  @blp.response(201, StoreSchema)
  def post(self, store_data):
    store = StoreModel(**store_data)

    try:
      db.session.add(store)
      db.session.commit()
    except IntegrityError:
      abort(400, message="A store with such name already exists.")
    except SQLAlchemyError:
      abort(500, message="error insert")

    return store
