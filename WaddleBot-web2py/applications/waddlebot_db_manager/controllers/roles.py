# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from roles.py")

# Function to decode names with special characters in them.
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new role from a given payload. Throws an error if no payload is given, or the role already exists.
def create_role():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'name' not in payload or 'description' not in payload or 'privilages' not in payload or 'requirements' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.roles.name == payload['name']).count() > 0:
        return dict(msg="Role already exists.")
    db.roles.insert(**payload)
    return dict(msg="Role created.")

# Get all roles.
def get_all():
    roles = db(db.roles).select()
    return dict(data=roles)

# Get a role by its name. If the role does not exist, return an error.
def get_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    role = db(db.roles.name == name).select().first()
    if not role:
        return dict(msg="Role does not exist.")
    return dict(data=role)

# Update a role by its name. If the role does not exist, return an error.
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
    role = db(db.roles.name == name).select().first()
    if not role:
        return dict(msg="Role does not exist.")
    role.update_record(**payload)
    return dict(msg="Role updated.")

# Delete a role by its name. If the role does not exist, return an error.
def delete_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    role = db(db.roles.name == name).select().first()
    if not role:
        return dict(msg="Role does not exist.")
    role.delete_record()
    return dict(msg="Role deleted.") 