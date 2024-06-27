# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from gateway_accounts.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new gateway account from a given payload. Throws an error if no payload is given, or the gateway account already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'account_name' not in payload or 'account_type_name' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.gateway_accounts.account_name == payload['account_name']).count() > 0:
        return dict(msg="Gateway account already exists.")
    account_type = db(db.account_types.type_name == payload['account_type_name']).select().first()
    if not account_type:
        return dict(msg="Gateway type does not exist.")
    db.gateway_accounts.insert(account_name=payload['account_name'], account_type=account_type.id)
    return dict(msg="Gateway account created.")

# Get all gateway accounts.
def get_all():
    gateway_accounts = db(db.gateway_accounts).select()
    return dict(data=gateway_accounts)

# Get a gateway account by its name. If the gateway account does not exist, return an error.
def get_by_name():
    account_name = request.args(0)
    account_name = decode_name(account_name)
    account = db(db.gateway_accounts.account_name == account_name).select().first()
    if not account:
        return dict(msg="Gateway account not found.")
    return dict(data=account)

# Get the first default gateway account of a specific type name. The account name is within a payload.
def get_default_by_type():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'account_type_name' not in payload:
        return dict(msg="Payload missing required fields: account_type_name.")

    account_type_name = payload['account_type_name']    
    account_type = db(db.gateway_types.type_name == account_type_name).select().first()
    if not account_type:
        return dict(msg="Gateway type not found.")
    account = db((db.gateway_accounts.account_type == account_type.id) & (db.gateway_accounts.is_default == True)).select().first()
    return dict(data=[account])

# Update a gateway account by its name. If the gateway account does not exist, return an error.
def update_by_name():
    account_name = request.args(0)
    account_name = decode_name(account_name)
    account = db(db.gateway_accounts.account_name == account_name).select().first()
    if not account:
        return dict(msg="Gateway account not found.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'account_type_name' in payload:
        account_type = db(db.gateway_types.type_name == payload['account_type_name']).select().first()
        if not account_type:
            return dict(msg="Gateway type does not exist.")
        account.update_record(account_type=account_type.id)
    if 'is_default' in payload:
        account.update_record(is_default=payload['is_default'])
    return dict(msg="Gateway account updated.")

# Delete a gateway account by its name. If the gateway account does not exist, return an error.
def delete_by_name():
    account_name = request.args(0)
    account_name = decode_name(account_name)
    account = db(db.gateway_accounts.account_name == account_name).select().first()
    if not account:
        return dict(msg="Gateway account not found.")
    account.delete_record()
    return dict(msg="Gateway account deleted.")

# Get all gateway accounts of a specific type.
def get_by_type():
    account_type_name = request.args(0)
    account_type_name = decode_name(account_type_name)
    account_type = db(db.gateway_types.type_name == account_type_name).select().first()
    if not account_type:
        return dict(msg="Gateway type not found.")
    accounts = db(db.gateway_accounts.account_type == account_type.id).select()
    return dict(data=accounts)