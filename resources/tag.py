from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from schemas import TagSchema, TagAndItemSchema
from db import db
from models import TagModel, ItemModel, StoreModel

blp = Blueprint("tags", __name__, description="tag operations")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
  @jwt_required()
  @blp.response(200, TagSchema(many=True))
  def get(self, store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store.tags.all()

  @jwt_required()
  @blp.arguments(TagSchema)
  @blp.response(201, TagSchema)
  def post(self, tag_data, store_id):
    tag = TagModel(**tag_data, store_id=store_id)

    try:
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagToItem(MethodView):
  @jwt_required()
  @blp.response(201, TagSchema)
  def post(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)
    item.tags.append(tag)
    tag.items.append(item)

    try:
      db.session.add(item)
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return tag

  @jwt_required()
  @blp.response(200, TagAndItemSchema)
  def delete(self, item_id, tag_id):
    item = ItemModel.query.get_or_404(item_id)
    tag = TagModel.query.get_or_404(tag_id)
    item.tags.remove(tag)
    tag.items.remove(item)

    try:
      db.session.add(item)
      db.session.add(tag)
      db.session.commit()
    except SQLAlchemyError as e:
      abort(500, message=str(e))

    return {"message": "removed", "item": item, "tag": tag}

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
  @jwt_required()
  @blp.response(200, TagSchema)
  def get(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)
    return tag

  @jwt_required()
  @blp.response(
    202,
    description="delete tag with no item",
    example={"message": "tag deleted"}
  )
  @blp.response(
    400,
    description="NOOP if tag is assigned with items."
  )
  def delete(self, tag_id):
    tag = TagModel.query.get_or_404(tag_id)

    if not tag.items:
      db.session.delete(tag)
      db.session.commit()
      return {"message": "tag deleted"}
    abort(
      400,
      message="couldnot delete tag, items associated with it"
    )
