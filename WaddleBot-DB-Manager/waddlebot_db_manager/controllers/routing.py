# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from routing.py")

# Function to decode names with special characters in them.
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new routing from a given payload. Throws an error if no payload is given, or the routing already exists.
def create_routing():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'name' not in payload or 'description' not in payload or 'privilages' not in payload or 'requirements' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.routings.name == payload['name']).count() > 0:
        return dict(msg="Routing already exists.")
    db.routings.insert(**payload)
    return dict(msg="Routing created.")

# Get all routings.
def get_all():
    routings = db(db.routings).select()
    return dict(data=routings)

# Get a routing by its name. If the routing does not exist, return an error.
def get_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    routing = db(db.routings.name == name).select().first()
    if not routing:
        return dict(msg="Routing does not exist.")
    return dict(data=routing)

# Update a routing by its name. If the routing does not exist, return an error.
def update_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'name' not in payload or 'description' not in payload or 'privilages' not in payload or 'requirements' not in payload:
        return dict(msg="Payload missing required fields.")
    routing = db(db.routings.name == name).select().first()
    if not routing:
        return dict(msg="Routing does not exist.")
    
    routing.update_record(**payload)
    return dict(msg="Routing updated.")

# Delete a routing by its name. If the routing does not exist, return an error.
def delete_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    routing = db(db.routings.name == name).select().first()
    if not routing:
        return dict(msg="Routing does not exist.")
    routing.delete_record()
    return dict(msg="Routing deleted.")

# Get all routings for a specific community name.
def get_by_community_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    community = db(db.communities.community_name == name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    routings = db(db.routings.community_id == community.id).select()
    return dict(data=routings)


    