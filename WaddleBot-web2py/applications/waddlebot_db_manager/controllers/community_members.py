# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities.py")

# Create a new community member from a given payload. Throws an error if no payload is given, or the community member id already exists in a given community id
def create_member():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'identity_name' not in payload:
        return dict(msg="Missing the required fields. Need community_name and identity_name.")
    
    # Set the role_id to 1 by default, if it does not exist in the payload.
    role_id = 1
    if "role_id" in payload:
        role_id = payload.get('role_id', None)

    # Get the community_id from the communities table, using the community_name, if it exists.
    community = db(db.communities.community_name == payload['community_name']).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Get the identity_id from the identities table, using the identity_name, if it exists.
    identity = db(db.identities.name == payload['identity_name']).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")

    # Check if the community member already exists in the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if community_member:
        return dict(msg="Community member already exists.")

    # Create the community member.
    db.community_members.insert(community_id=community.id, identity_id=identity.id, role_id=role_id, currency=0)

    return dict(msg=f"{payload['identity_name']} has joined the community {payload['community_name']}.")

# Get all community members accross all communities.
def get_all():
    community_members = db(db.community_members).select()
    return dict(data=community_members)

# Get all community members in a given community id.
def get_by_community_id():
    community_id = request.args(0)
    if not community_id:
        return dict(msg="No community id given.")
    community_members = db(db.community_members.community_id == community_id).select()
    return dict(data=community_members)

# Update a community member by its community id and member id. If the community member does not exist, return an error.
def update_by_community_id_and_identity_id():
    community_id = request.args(0)
    identity_id = request.args(1)
    if not community_id or not identity_id:
        return dict(msg="No community id or member id given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_id' not in payload or 'identity_id' not in payload or 'role_id' not in payload or 'currency' not in payload:
        return dict(msg="Payload missing required fields.")
    community_member = db((db.community_members.community_id == community_id) & (db.community_members.identity_id == identity_id)).select().first()
    if not community_member:
        return dict(msg="Community member does not exist.")
    community_member.update_record(**payload)
    return dict(msg="Community member updated.")

# Delete a community member by its community id and member id. If the community member does not exist, return an error.
def delete_by_community_id_and_identity_id():
    community_id = request.args(0)
    identity_id = request.args(1)
    if not community_id or not identity_id:
        return dict(msg="No community id or member id given.")
    community_member = db((db.community_members.community_id == community_id) & (db.community_members.identity_id == identity_id)).select().first()
    if not community_member:
        return dict(msg="Community member does not exist.")
    community_member.delete_record()
    return dict(msg="Community member deleted.")

# Using the community name and identity name, remove a member from a community.
def remove_member():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name between [] characters.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'identity_name' not in payload:
        return dict(msg="Missing the required fields. Need community_name between [] characters.")
    
    # Get the community_id from the communities table, using the community_name, if it exists.
    community = db(db.communities.community_name == payload['community_name']).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Get the identity_id from the identities table, using the identity_name, if it exists.
    identity = db(db.identities.name == payload['identity_name']).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")

    # Check if the community member already exists in the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if not community_member:
        return dict(msg="Community member does not exist.")

    # Remove the community member.
    community_member.delete_record()

    return dict(msg=f"{payload['identity_name']} has left the community {payload['community_name']}.")

