# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities.py")

# Create a new community member from a given payload. Throws an error if no payload is given, or the community member id already exists in a given community id
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_id' not in payload or 'identity_id' not in payload or 'role_id' not in payload:
        return dict(msg="Payload missing required fields.")
    if db((db.community_members.community_id == payload['community_id']) & (db.community_members.identity_id == payload['identity_id'])).count() > 0:
        return dict(msg="Community member already exists in this community.")
    db.community_members.insert(community_id=payload['community_id'], identity_id=payload['identity_id'], role_id=payload['role_id'])
    return dict(msg="Community member created.")

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

