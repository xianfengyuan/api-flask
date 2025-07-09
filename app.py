from flask import Flask, request

app = Flask(__name__)

stores = [
  {
    "name": "My store",
    "items": [
      {
        "name": "Chair",
        "price": 15.99
      }
    ]
  }
]

@app.get("/store")
def get_all_store():
  return {"stores": stores}

@app.post("/store")
def create_store():
  req = request.get_json()
  new_store = {"name": req["name"], "items": []}
  stores.append(new_store)
  return new_store, 201

@app.post("/store/<string:name>/item")
def create_item(name):
  req = request.get_json()
  for store in stores:
    if store["name"] == name:
      new_item = {"name": req["name"], "price": req["price"]}
      store["items"].append(new_item)
      return new_item, 201
  return {"message": "store not found"}, 404

@app.get("/store/<string:name>")
def get_store(name):
  for store in stores:
    if store["name"] == name:
      return store
  return {"message": "store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_in_store(name):
  for store in stores:
    if store["name"] == name:
      return {"items": store["items"]}
  return {"message": "store not found"}, 404
