import json
import os

import redis

_client = None


def _conn() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis(
            host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            db=0,
            decode_responses=True,
        )
        _seed_if_empty()
    return _client


def _seed_if_empty():
    if _client.exists("items:counter"):
        return
    _client.set("item:1", json.dumps(
        {"id": 1, "title": "Item di esempio", "note": "Inserito automaticamente al primo avvio"}
    ))
    _client.set("items:counter", 1)


def _item_ids():
    ids = []
    for key in _conn().scan_iter("item:*"):
        item_id = int(key.split(":")[1])
        ids.append(item_id)
    return sorted(ids)


def get_all():
    c = _conn()
    return [json.loads(c.get(f"item:{item_id}")) for item_id in _item_ids()]


def get(item_id):
    c = _conn()
    value = c.get(f"item:{item_id}")
    return json.loads(value) if value else None


def create(title, note):
    c = _conn()
    item_id = c.incr("items:counter")
    item = {"id": item_id, "title": title, "note": note}
    c.set(f"item:{item_id}", json.dumps(item))
    return item


def update(item_id, title, note):
    c = _conn()
    if not c.exists(f"item:{item_id}"):
        return None
    item = {"id": item_id, "title": title, "note": note}
    c.set(f"item:{item_id}", json.dumps(item))
    return item


def delete_item(item_id):
    c = _conn()
    return c.delete(f"item:{item_id}") > 0