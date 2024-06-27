# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from routing_gateways.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new routing gateway from a given payload. Throws an error if no payload is given, or the routing gateway already exists.
def create_gateway():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    if 'gateway_type_name' not in payload or 'account_name' not in payload or 'channel_id' not in payload:
        return dict(msg="Payload missing required fields.", status=400)
    # Check if the account exists in the gateway_accounts table
    account = db(db.gateway_accounts.account_name == payload['account_name']).select().first()
    if not account:
        return dict(msg="Account does not exist.", status=404)
    # Check if the gateway type exists in the gateway_types table
    gateway_type = db(db.gateway_types.type_name == payload['gateway_type_name']).select().first()
    if not gateway_type:
        return dict(msg="Gateway type does not exist.", status=404)
    # Check if a record exists that matches the given payload exactly
    if db((db.routing_gateways.account == account.id) & (db.routing_gateways.channel_id == payload['channel_id'])).count() > 0:
        return dict(msg="Routing gateway already exists.", status=409)
    

    db.routing_gateways.insert(gateway_type=gateway_type.id, account=account.id, channel_id=payload['channel_id'])

    # Get the gateway type name
    route_type = db(db.gateway_types.id == gateway_type.id).select().first()

    return dict(msg="Routing gateway created.", status=201, route_type=route_type.type_name)

# Get all routing gateways in the database and displaye the actual names of the gateway type and account, instead of their IDs.
def get_all():
    routing_gateways = db(db.routing_gateways).select()
    data = []
    for routing_gateway in routing_gateways:
        gateway_type = db(db.gateway_types.id == routing_gateway.gateway_type).select().first()
        account = db(db.gateway_accounts.id == routing_gateway.account).select().first()
        data.append(dict(
            gateway_type=decode_name(gateway_type.type_name),
            account=decode_name(account.account_name),
            channel_id=routing_gateway.channel_id
        ))
    return dict(data=data)

# Get a routing gateway by its channel ID. If the routing gateway does not exist, return an error.
def get_by_channel_id():
    channel_id = request.args(0)
    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway not found.")
    return dict(data=routing_gateway)

# Update a routing gateway by its channel ID. If the routing gateway does not exist, return an error.
def update_by_channel_id():
    channel_id = request.args(0)
    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway not found.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'gateway_type_name' in payload:
        gateway_type = db(db.gateway_types.type_name == payload['gateway_type_name']).select().first()
        if not gateway_type:
            return dict(msg="Gateway type does not exist.")
        routing_gateway.gateway_type = gateway_type.id
    if 'account_name' in payload:
        account = db(db.gateway_accounts.account_name == payload['account_name']).select().first()
        if not account:
            return dict(msg="Account does not exist.")
        routing_gateway.account = account.id
    if 'channel_id' in payload:
        routing_gateway.channel_id = payload['channel_id']
    routing_gateway.update_record()
    return dict(msg="Routing gateway updated.")

# Delete a routing gateway by its channel ID. If the routing gateway does not exist, return an error.
def delete_by_channel_id():
    channel_id = request.args(0)
    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway not found.")
    routing_gateway.delete_record()
    return dict(msg="Routing gateway deleted.")
    
# Delete a routing gateway by its channel id and gateway type. The variables are passed as a payload. If the routing gateway does not exist, return an error.
def delete_by_channel_id_and_gateway_type():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    if 'channel_id' not in payload or 'gateway_type_name' not in payload:
        return dict(msg="Payload missing required fields.", status=400)
    gateway_type = db(db.gateway_types.type_name == payload['gateway_type_name']).select().first()
    if not gateway_type:
        return dict(msg="Gateway type does not exist.", status=404)
    routing_gateway = db((db.routing_gateways.channel_id == payload['channel_id']) & (db.routing_gateways.gateway_type == gateway_type.id)).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway not found.", status=404)
    routing_gateway.delete_record()
    return dict(msg="Routing gateway deleted.", status=200)
