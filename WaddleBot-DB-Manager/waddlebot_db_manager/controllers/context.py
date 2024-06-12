# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from context.py")

# Function to decode names with special characters in them.
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    # name = name.replace("_", " ")

    return name   

# Create the initial context of a identity_name, by adding the given identity_name to the "Global" community and then setting the context to the "Global" community. 
# If the identity_name already exists in the community, as well as the context, return an error. If the identity_name does not exist, return an error.
# If the community does not exist, return an error. If the identity_name is already in the community, return an error.  
def initialize_user():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'identity_name' not in payload:
        return dict(msg="Payload missing required fields.")
    identity_name = decode_name(payload['identity_name'])
    identity = db(db.identities.name == identity_name).select().first()

    # Create a new identity if the identity does not exist.
    if not identity:
        db.identities.insert(name=identity_name, country="Global", ip_address="", browser_fingerprints=[])
    

    # Set the new identity.
    identity = db(db.identities.name == identity_name).select().first()

    community = db(db.communities.community_name == "Global").select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community_member = db((db.community_members.identity_id == identity.id) & (db.community_members.community_id == community.id)).select().first()
    if community_member:
        return dict(msg="Identity is already in the community.")
    
    # Get the role id for the 'member' role.
    role = db(db.roles.name == "Member").select().first()

    db.community_members.insert(identity_id=identity.id, community_id=community.id, role_id=role.id, currency=0, reputation=600)
    context = db(db.context.identity_id == identity.id).select().first()
    # If the context already exists, update it.
    if context:
        db(db.context.identity_id == identity.id).update(community_id=community.id)
        return dict(msg="Your context has been set to the Global community.")
    db.context.insert(identity_id=identity.id, community_id=community.id)
    return dict(msg="Your context has been set to the Global community.")

    

# Create a new context from a given payload. Only one context can exist per identity. 
# Throws an error if no payload is given, or the context already exists. The payload 
# must contain the identity name and community name to get their respective ID's
def set_context():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'identity_name' not in payload or 'community_name' not in payload:
        return dict(msg="Payload missing required fields.")
    identity_name = decode_name(payload['identity_name'])
    community_name = decode_name(payload['community_name'])
    identity = db(db.identities.name == identity_name).select().first()
    community = db(db.communities.community_name == community_name).select().first()
    if not identity or not community:
        return dict(msg="Identity or community does not exist.")
    context = db(db.context.identity_id == identity.id).select().first()

    # If the identity is not in the community, return an error.
    community_member = db((db.community_members.identity_id == identity.id) & (db.community_members.community_id == community.id)).select().first()
    if not community_member:
        return dict(msg="You are not a member of the community. Please join the community first.")

    # If the context already exists, update it.
    if context:
        db(db.context.identity_id == identity.id).update(community_id=community.id)
        return dict(msg=f"Your context has been set to the community {community_name}.")
    db.context.insert(identity_id=identity.id, community_id=community.id)
    return dict(msg=f"Your context has been set to the community {community_name}.")

# Get all contexts.
def get_all():
    contexts = db(db.context).select()
    return dict(data=contexts)

# Get a context by its identity ID. If the context does not exist, return an error.
def get_by_identity_id():
    identity_id = request.args(0)
    if not identity_id:
        return dict(msg="No identity ID given.")
    context = db(db.context.identity_id == identity_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    return dict(data=context)

# Get a context by an identity name. If the context does not exist, return an error.
def get_by_identity_name():
    identity_name = request.args(0)
    if not identity_name:
        return dict(msg="No identity name given.")
    identity_name = decode_name(identity_name)
    identity = db(db.identities.name == identity_name).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")
    context = db(db.context.identity_id == identity.id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    # Get the community name from the community ID.
    community = db(db.communities.id == context.community_id).select().first()
    return dict(data={"identity_name": identity_name, "community_name": community.community_name})

# Update a context by its identity ID. If the context does not exist, return an error.
def update_by_identity_id():
    identity_id = request.args(0)
    if not identity_id:
        return dict(msg="No identity ID given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'identity_id' not in payload or 'community_id' not in payload:
        return dict(msg="Payload missing required fields.")
    context = db(db.context.identity_id == identity_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    db(db.context.identity_id == identity_id).update(**payload)
    return dict(msg="Context updated.")

# Delete a context by its identity ID. If the context does not exist, return an error.
def delete_by_identity_id():
    identity_id = request.args(0)
    if not identity_id:
        return dict(msg="No identity ID given.")
    context = db(db.context.identity_id == identity_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    db(db.context.identity_id == identity_id).delete()
    return dict(msg="Context deleted.")

# Get a context by its community ID. If the context does not exist, return an error.
def get_by_community_id():
    community_id = request.args(0)
    if not community_id:
        return dict(msg="No community ID given.")
    context = db(db.context.community_id == community_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    return dict(data=context)

# Update a context by its community ID. If the context does not exist, return an error.
def update_by_community_id():
    community_id = request.args(0)
    if not community_id:
        return dict(msg="No community ID given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'identity_id' not in payload or 'community_id' not in payload:
        return dict(msg="Payload missing required fields.")
    context = db(db.context.community_id == community_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    db(db.context.community_id == community_id).update(**payload)
    return dict(msg="Context updated.")

# Delete a context by its community ID. If the context does not exist, return an error.
def delete_by_community_id():
    community_id = request.args(0)
    if not community_id:
        return dict(msg="No community ID given.")
    context = db(db.context.community_id == community_id).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    db(db.context.community_id == community_id).delete()
    return dict(msg="Context deleted.")

# Get a context by its identity ID and community ID. If the context does not exist, return an error.
def get_by_identity_and_community_id():
    identity_id = request.args(0)
    community_id = request.args(1)
    if not identity_id or not community_id:
        return dict(msg="No identity ID or community ID given.")
    context = db((db.context.identity_id == identity_id) & (db.context.community_id == community_id)).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    return dict(data=context)

# Update a context by its identity ID and community ID. If the context does not exist, return an error.
def update_by_identity_and_community_id():
    identity_id = request.args(0)
    community_id = request.args(1)
    if not identity_id or not community_id:
        return dict(msg="No identity ID or community ID given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'identity_id' not in payload or 'community_id' not in payload:
        return dict(msg="Payload missing required fields.")
    context = db((db.context.identity_id == identity_id) & (db.context.community_id == community_id)).select().first()
    if not context:
        return dict(msg="Context does not exist.")
    db((db.context.identity_id == identity_id) & (db.context.community_id == community_id)).update(**payload)
    return dict(msg="Context updated.")

