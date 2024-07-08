# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from gateway_types.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new gateway type from a given payload. Throws an error if no payload is given, or the gateway type already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'type_name' not in payload or 'description' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.gateway_types.type_name == payload['type_name']).count() > 0:
        return dict(msg="Gateway type already exists.")
    db.gateway_types.insert(type_name=payload['type_name'], description=payload['description'])
    return dict(msg="Gateway type created.")

# Get all gateway types.
def get_all():
    gateway_types = db(db.gateway_types).select()
    return dict(data=gateway_types)

# Get a gateway type by its name. If the gateway type does not exist, return an error.
def get_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    gateway_type = db(db.gateway_types.type_name == type_name).select().first()
    if not gateway_type:
        return dict(msg="Gateway type not found.")
    return dict(data=gateway_type)

# Update a gateway type by its name. If the gateway type does not exist, return an error.
def update_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    gateway_type = db(db.gateway_types.type_name == type_name).select().first()
    if not gateway_type:
        return dict(msg="Gateway type not found.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'type_name' in payload:
        gateway_type.type_name = payload['type_name']
    if 'description' in payload:
        gateway_type.description = payload['description']
    gateway_type.update_record()
    return dict(msg="Gateway type updated.")

# Delete a gateway type by its name. If the gateway type does not exist, return an error.
def delete_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    gateway_type = db(db.gateway_types.type_name == type_name).select().first()
    if not gateway_type:
        return dict(msg="Gateway type not found.")
    gateway_type.delete_record()
    return dict(msg="Gateway type deleted.")
