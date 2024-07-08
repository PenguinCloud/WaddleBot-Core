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
    if 'gateway_type_name' not in payload or 'gateway_server_name' not in payload or 'channel_id' not in payload:
        return dict(msg="Payload missing required fields.", status=400)
    # Check if the gateway_server exists in the gateway_servers table
    gateway_server = db(db.gateway_servers.name == payload['gateway_server_name']).select().first()
    if not gateway_server:
        return dict(msg="Gateway Server does not exist.", status=404)
    # Check if the gateway type exists in the gateway_types table
    gateway_type = db(db.gateway_types.type_name == payload['gateway_type_name']).select().first()
    if not gateway_type:
        return dict(msg="Gateway type does not exist.", status=404)
    # Check if a record exists that matches the given payload exactly
    if db((db.routing_gateways.gateway_server == gateway_server.id) & (db.routing_gateways.channel_id == payload['channel_id'])).count() > 0:
        return dict(msg="Routing gateway already exists.", status=409)
    

    db.routing_gateways.insert(gateway_type=gateway_type.id, gateway_server=gateway_server.id, channel_id=payload['channel_id'])

    # Get the gateway type name
    route_type = db(db.gateway_types.id == gateway_type.id).select().first()

    return dict(msg="Routing gateway created.", status=201, route_type=route_type.type_name)

# Get all routing gateways in the database and displaye the actual names of the gateway type and gateway_server, instead of their IDs.
def get_all():
    routing_gateways = db(db.routing_gateways).select()
    data = []
    for routing_gateway in routing_gateways:
        gateway_type = db(db.gateway_types.id == routing_gateway.gateway_type).select().first()
        gateway_server = db(db.gateway_servers.id == routing_gateway.gateway_server).select().first()
        if gateway_server:
            data.append(dict(
                gateway_type=decode_name(gateway_type.type_name),
                gateway_server=decode_name(gateway_server.name),
                channel_id=routing_gateway.channel_id
            ))
        else:
            data.append(dict(
                gateway_type=decode_name(gateway_type.type_name),
                gateway_server="Gateway Server not found",
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
    payload = request.body.read()
    
    if not payload:
        return dict(msg="No payload given.", status=400)
    
    payload = json.loads(payload)

    if 'channel_id' not in payload:
        return dict(msg="Payload missing required fields. Please provide the channel_id.", status=400)
    channel_id = payload['channel_id']

    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway not found.")
    
    if 'gateway_type_name' not in payload or 'gateway_server_name' not in payload:
        return dict(msg="Payload missing required fields.", status=400)
    # Check if the gateway_server exists in the gateway_servers table
    gateway_server = db(db.gateway_servers.name == payload['gateway_server_name']).select().first()
    if not gateway_server:
        return dict(msg="Gateway Server does not exist.", status=404)
    # Check if the gateway type exists in the gateway_types table
    gateway_type = db(db.gateway_types.type_name == payload['gateway_type_name']).select().first()
    if not gateway_type:
        return dict(msg="Gateway type does not exist.", status=404)
    routing_gateway.update_record(gateway_type=gateway_type.id, gateway_server=gateway_server.id)
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
