from flask import Flask, jsonify, render_template, request

from db import create, delete_item, get, get_all, update

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/items")
def list_items():
    return jsonify(get_all())


@app.post("/api/items")
def create_item():
    data = request.get_json(force=True)
    item = create(data.get("title", ""), data.get("note", ""))
    return jsonify(item), 201


@app.get("/api/items/<int:item_id>")
def get_item(item_id):
    item = get(item_id)
    if item is None:
        return jsonify({"error": "non trovato"}), 404
    return jsonify(item)


@app.put("/api/items/<int:item_id>")
def update_item(item_id):
    data = request.get_json(force=True)
    item = update(item_id, data.get("title", ""), data.get("note", ""))
    if item is None:
        return jsonify({"error": "non trovato"}), 404
    return jsonify(item)


@app.delete("/api/items/<int:item_id>")
def delete_item_route(item_id):
    if delete_item(item_id):
        return jsonify({"ok": True})
    return jsonify({"error": "non trovato"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)