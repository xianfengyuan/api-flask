import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="item operations")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
  @blp.response(200, ItemSchema)
  def get(self, item_id):
    try:
      return items[item_id]
    except KeyError:
      abort(404, message="item not found")

  def delete(self, item_id):
    try:
      del items[item_id]
      return {"message": "item deleted"}
    except KeyError:
      abort(404, message="item not found")

  @blp.arguments(ItemUpdateSchema)
  @blp.response(200, ItemSchema)
  def put(self, item_data, item_id):
    try:
      item = items[item_id]
      item |= item_data
      return {"message": "item updated"}
    except KeyError:
      abort(404, message="item not found")

@blp.route("/item")
class ItemList(MethodView):
  @blp.response(200, ItemSchema(many=True))
  def get(self):
    return items.values()

  @blp.arguments(ItemSchema)
  @blp.response(201, ItemSchema)
  def post(self, item_data):
    for item in items.values():
      if (
        item_data["name"] == item["name"]
        and item_data["store_id"] == item["store_id"]
      ):
        abort(404, message="item already exists")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item
