# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from gateway_server_types.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new gateway server type from a given payload. Throws an error if no payload is given, or the gateway server type already exists.
def create_gateway_server_type():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    if 'type_name' not in payload or 'description' not in payload:
        return dict(msg="Payload missing required fields.", status=400)
    # Check if a record exists that matches the given payload exactly
    if db(db.gateway_server_types.type_name == payload['type_name']).count() > 0:
        return dict(msg="Gateway server type already exists.", status=409)
    

    db.gateway_server_types.insert(type_name=payload['type_name'], description=payload['description'])

    return dict(msg="Gateway server type created.", status=201)

# Get all gateway server types in the database.
def get_all():
    gateway_server_types = db(db.gateway_server_types).select()
    data = []
    for gateway_server_type in gateway_server_types:
        data.append(dict(
            type_name=gateway_server_type.type_name,
            description=gateway_server_type.description
        ))
    return dict(data=data)

# Get a gateway server type by its name. If the gateway server type does not exist, return an error.
def get_by_name():
    type_name = request.vars.type_name
    if not type_name:
        return dict(msg="No gateway server type name given.", status=400)
    gateway_server_type = db(db.gateway_server_types.type_name == type_name).select().first()
    if not gateway_server_type:
        return dict(msg="Gateway server type does not exist.", status=404)
    return dict(type_name=gateway_server_type.type_name, description=gateway_server_type.description)

# Update a gateway server type by its name. If the gateway server type does not exist, return an error.
def update_by_name():
    type_name = request.vars.type_name
    if not type_name:
        return dict(msg="No gateway server type name given.", status=400)
    gateway_server_type = db(db.gateway_server_types.type_name == type_name).select().first()
    if not gateway_server_type:
        return dict(msg="Gateway server type does not exist.", status=404)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    if 'description' not in payload:
        return dict(msg="Payload missing required fields.", status=400)

    gateway_server_type.update_record(description=payload['description'])

    return dict(msg="Gateway server type updated.", status=200)

# Delete a gateway server type by its name. If the gateway server type does not exist, return an error.
def delete_by_name():
    type_name = request.vars.type_name
    if not type_name:
        return dict(msg="No gateway server type name given.", status=400)
    gateway_server_type = db(db.gateway_server_types.type_name == type_name).select().first()
    if not gateway_server_type:
        return dict(msg="Gateway server type does not exist.", status=404)

    gateway_server_type.delete_record()

    return dict(msg="Gateway server type deleted.", status=200)