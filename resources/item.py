from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchema, ItemUpdateSchema

from db import db
from models import ItemModel

blp = Blueprint("items", __name__, description="item operations")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
  @jwt_required()
  @blp.response(200, ItemSchema)
  def get(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item

  @jwt_required()
  def delete(self, item_id):
    item = ItemModel.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return {"message": "item deleted"}

  @jwt_required()
  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema)
  def put(self, item_data, item_id):
    item = ItemModel.query.get(item_id)
    if item:
      item.price = item_data["price"]
      item.name = item_data["name"]
    else:
      item = ItemModel(id=item_id, **item_data)

    db.session.add(item)
    db.session.commit()

    return item

@blp.route("/item")
class ItemList(MethodView):
  @jwt_required()
  @blp.response(200, ItemSchema(many=True))
  def get(self):
    return ItemModel.query.all()

  @jwt_required()
  @blp.arguments(ItemSchema)
  @blp.response(201, ItemSchema)
  def post(self, item_data):
    item = ItemModel(**item_data)

    try:
      db.session.add(item)
      db.session.commit()
    except SQLAlchemyError:
      abort(500, message="error insert")

    return item
