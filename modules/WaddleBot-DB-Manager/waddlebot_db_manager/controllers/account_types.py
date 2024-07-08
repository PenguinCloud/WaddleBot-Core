# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from account_types.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new account type from a given payload. Throws an error if no payload is given, or the account type already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'type_name' not in payload or 'description' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.account_types.type_name == payload['type_name']).count() > 0:
        return dict(msg="Account type already exists.")
    db.account_types.insert(type_name=payload['type_name'], description=payload['description'])
    return dict(msg="Account type created.")

# Get all account types.
def get_all():
    account_types = db(db.account_types).select()
    return dict(data=account_types)

# Get an account type by its name. If the account type does not exist, return an error.
def get_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    account_type = db(db.account_types.type_name == type_name).select().first()
    if not account_type:
        return dict(msg="Account type not found.")
    return dict(data=account_type)

# Update an account type by its name. If the account type does not exist, return an error.
def update_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    account_type = db(db.account_types.type_name == type_name).select().first()
    if not account_type:
        return dict(msg="Account type not found.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'type_name' in payload:
        account_type.type_name = payload['type_name']
    if 'description' in payload:
        account_type.description = payload['description']
    account_type.update_record()
    return dict(msg="Account type updated.")

# Delete an account type by its name. If the account type does not exist, return an error.
def delete_by_name():
    type_name = request.args(0)
    type_name = decode_name(type_name)
    account_type = db(db.account_types.type_name == type_name).select().first()
    if not account_type:
        return dict(msg="Account type not found.")
    account_type.delete_record()
    return dict(msg="Account type deleted.")


