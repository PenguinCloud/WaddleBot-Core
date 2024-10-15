# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from gateway_servers.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new gateway server from a given payload. Throws an error if no payload is given, or the gateway server already exists.
def create_gateway_server():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    if 'name' not in payload or 'server_type_name' not in payload or 'server_nick' not in payload or "server_id" not in payload:
        return dict(msg="Payload missing required fields. Please provide the name, server_type_name, server_nick and server_id.", status=400)
    # Check if the server type exists in the gateway_server_types table
    server_type = db(db.gateway_server_types.type_name == payload['server_type_name']).select().first()
    if not server_type:
        return dict(msg="Server type does not exist.", status=404)
    # Check if a record exists that matches the given payload exactly
    if db((db.gateway_servers.name == payload['name']) & (db.gateway_servers.server_type == server_type.id)).count() > 0:
        return dict(msg="Gateway server already exists.", status=409)
    

    db.gateway_servers.insert(name=payload['name'], server_type=server_type.id, server_nick=payload['server_nick'], server_id=payload['server_id'])

    return dict(msg="Gateway server created.", status=201)

# Get all gateway servers in the database and displaye the actual names of the server type, instead of their IDs.
def get_all():
    gateway_servers = db(db.gateway_servers).select()
    data = []
    for gateway_server in gateway_servers:
        server_type = db(db.gateway_server_types.id == gateway_server.server_type).select().first()
        data.append(dict(
            name=gateway_server.name,
            server_type=decode_name(server_type.type_name),
            server_nick=gateway_server.server_nick,
            server_id=gateway_server.server_id
        ))
    return dict(data=data)

# Get a gateway server by its name. If the gateway server does not exist, return an error.
def get_by_name():
    name = request.args(0)
    if not name:
        return dict(msg="No gateway server name given.", status=400)
    gateway_server = db(db.gateway_servers.name == name).select().first()
    if not gateway_server:
        return dict(msg="Gateway server does not exist.", status=404)
    server_type = db(db.gateway_server_types.id == gateway_server.server_type).select().first()
    return dict(name=gateway_server.name, server_type=decode_name(server_type.type_name), server_nick=gateway_server.server_nick)

# Update a gateway server by its name. If the gateway server does not exist, return an error.
def update_by_name():
    name = request.args(0)
    
    if not name:
        return dict(msg="No gateway server name given.", status=400)
    gateway_server = db(db.gateway_servers.name == name).select().first()
    if not gateway_server:
        return dict(msg="Gateway server does not exist.", status=404)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.", status=400)
    payload = json.loads(payload)
    # if 'server_type_name' not in payload or 'server_nick' not in payload or 'server_id' not in payload:
    #     return dict(msg="Payload missing required fields.", status=400)
    # Check if the server type exists in the gateway_server_types table

    if 'server_type_name' in payload:
        server_type = db(db.gateway_server_types.type_name == payload['server_type_name']).select().first()
        if not server_type:
            return dict(msg="Server type does not exist.", status=404)
        gateway_server.server_type = server_type.id

    if 'server_nick' in payload:
        gateway_server.server_nick = payload['server_nick']
    
    if 'server_id' in payload:
        gateway_server.server_id = payload['server_id']
    
    if 'protocol' in payload:
        gateway_server.protocol = payload['protocol']
    
    gateway_server.update_record()

    return dict(msg="Gateway server updated.", status=200)

# Delete a gateway server by its name. If the gateway server does not exist, return an error.
def delete_by_name():
    name = request.args(0)
    if not name:
        return dict(msg="No gateway server name given.", status=400)
    gateway_server = db(db.gateway_servers.name == name).select().first()
    if not gateway_server:
        return dict(msg="Gateway server does not exist.", status=404)
    gateway_server.delete_record()

    return dict(msg="Gateway server deleted.", status=200)