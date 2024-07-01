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

#Function to replace the first character of a string with a hash if it is an underscore.
def replace_first_char(name):
    if name[0] == "_":
        name = "#" + name[1:]
    return name

# Create a new routing from a given payload. Throws an error if no payload is given, or the routing already exists.
def create_routing():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'name' not in payload or 'description' not in payload or 'privilages' not in payload or 'requirements' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.routing.name == payload['name']).count() > 0:
        return dict(msg="Routing already exists.")
    db.routing.insert(**payload)
    return dict(msg="Routing created.")

# Get all routings.
def get_all():
    routings = db(db.routing).select()
    return dict(data=routings)

# Function to get all routes that also have a community name.
def get_all_community_routes():
    routings = db(db.routing).select()
    for routing in routings:
        community = db(db.communities.id == routing.community_id).select().first()
        routing.community_name = community.community_name
    return dict(data=routings)

# Get a routing by its name. If the routing does not exist, return an error.
def get_by_name():
    name = request.args(0)
    name = decode_name(name)
    if not name:
        return dict(msg="No name given.")
    routing = db(db.routing.name == name).select().first()
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
    routing = db(db.routing.name == name).select().first()
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
    routing = db(db.routing.name == name).select().first()
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
    routings = db(db.routing.community_id == community.id).select()
    return dict(data=routings)

# Add a routing gateway to a community's list of gateways, if it doesnt exist, by their community name. If the community or 
# routing does not exist, return an error. The  is passed as an argument. The community_name is passed as a payload.
def add_route_to_community():
    channel_id = replace_first_char(request.args(0))
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload:
        return dict(msg="Payload missing required fields.")
    community_name = decode_name(payload['community_name'])
    
    # Checkif the channel_id is given in the arguments.
    print(channel_id)
    if not channel_id:
        return dict(msg="No channel ID given in the arguments.")

    # Check if the community is given in the payload.
    if not community_name:
        return dict(msg="No community name given in the payload. Remember to add the community name at the end of the command between [] brackets.")

    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    # Get the routing gateway bu the channel_id from the routing_gateways table.
    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway does not exist. Please create it first via !gateway add [platform] [channel_name]")

    # Get the routing record from the routing table by the community_id. If it doesnt exist, create it.
    routing = db(db.routing.community_id == community.id).select().first()
    if not routing:
        routing = db.routing.insert(community_id=community.id)

    # Add the routing gateway to the routing record. By adding 
    gateways = routing.gateways
    if not gateways:
        gateways = []

    if channel_id in gateways:
        return dict(msg="Routing gateway already exists in community.")
    gateways.append(channel_id)
    routing.update_record(gateways=gateways)

    return dict(msg="Routing added to community.")

# Remove a routing gateway from a community's list of gateways, if it exists, by their community name. If the community or 
# routing does not exist, return an error. The channel ID is passed as an argument. The community_name is passed as a payload.
def remove_route_from_community():
    channel_id = replace_first_char(request.args(0))
    print(channel_id)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload:
        return dict(msg="Payload missing required fields.")
    community_name = decode_name(payload['community_name'])
    
    # Checkif the channel_id is given in the arguments.
    if not channel_id:
        return dict(msg="No channel ID given in the arguments.")

    # Check if the community is given in the payload.
    if not community_name:
        return dict(msg="No community name given in the payload. Remember to add the community name at the end of the command between [] brackets.")

    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    # Get the routing gateway bu the channel_id from the routing_gateways table.
    routing_gateway = db(db.routing_gateways.channel_id == channel_id).select().first()
    if not routing_gateway:
        return dict(msg="Routing gateway does not exist. Please create it first via !gateway add [platform] [channel_name]")

    # Get the routing record from the routing table by the community_id. If it doesnt exist, throw an error.
    routing = db(db.routing.community_id == community.id).select().first()
    if not routing:
        return dict(msg="Community does not exist in the routings table.")

    # Remove the routing gateway from the routing record, if it exists.
    gateways = routing.gateways
    if not gateways:
        return dict(msg="No routing gateways in community.")
    
    print("Gateways for the current community: ", gateways)
    if channel_id in gateways:
        gateways.remove(channel_id)
    else:
        return dict(msg="Routing gateway does not exist in community.")
    
    routing.update_record(gateways=gateways)

    return dict(msg="Routing removed from community.")
    