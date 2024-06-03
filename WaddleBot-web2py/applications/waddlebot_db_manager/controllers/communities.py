# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new community from a given payload. Throws an error if no payload is given, or the community already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'community_description' not in payload:
        return dict(msg="Payload missing required fields.")
    if db(db.communities.community_name == payload['community_name']).count() > 0:
        return dict(msg="Community already exists.")
    db.communities.insert(community_name=payload['community_name'], community_description=payload['community_description'])
    return dict(msg="Community created.")

# Get all communities.
def get_all():
    communities = db(db.communities).select()
    return dict(data=communities)

# Get a community by its name. If the community does not exist, return an error.
def get_by_name():
    community_name = request.args(0)
    community_name = decode_name(community_name)
    if not community_name:
        return dict(msg="No community name given.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    return dict(data=community)

# Update a community by its name. If the community does not exist, return an error.
def update_by_name():
    community_name = request.args(0)
    community_name = decode_name(community_name)
    if not community_name:
        return dict(msg="No community name given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'community_description' not in payload:
        return dict(msg="Payload missing required fields.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community.update_record(community_name=payload['community_name'], community_description=payload['community_description'])
    return dict(msg="Community updated.")

# Delete a community by its name. If the community does not exist, return an error.
def delete_by_name():
    community_name = request.args(0)
    community_name = decode_name(community_name)
    if not community_name:
        return dict(msg="No community name given.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community.delete_record()
    return dict(msg="Community deleted.")

    
