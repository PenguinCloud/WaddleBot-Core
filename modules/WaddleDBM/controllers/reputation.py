# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from reputation.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Using a community name in the arguments and an identity name in the payload, get the reputation of the identity in the community. 
# If the community or identity does not exist, return an error.
def get_reputation():
    community_name = request.args(0)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name and identity_name between [] characters.")
    payload = json.loads(payload)
    identity_name = payload.get("identity_name")
    if not identity_name:
        return dict(msg="No identity_name given. Please provide an identity_name between [] characters.")
    
    community = db(db.community.name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Check if the identity exists.
    identity = db((db.identities.name == identity_name)).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")
    
    # Check if the member is a member of the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if not community_member:
        return dict(msg="Identity is not a member of the community. Join the community first.")

    reputation = db((db.reputation.identity_id == identity.id) & (db.reputation.community_id == community.id)).select().first()

    # If the reputation does not exist, create it.
    if not reputation:
        reputation = db.reputation.insert(identity_id=identity.id, community_id=community.id)

    return dict(msg=f"{payload['identity_name']} has {community_member.reputation} reputation in the community {community_name}.")

# Using a community name, identity name, and amount, add the amount to the member's reputation in the community. If the community or 
# member does not exist, return an error.
def add_reputation():
    community_name = request.args(0)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name, identity_name, and amount between [] characters.")
    payload = json.loads(payload)
    # Check if the identity name and amount are given in the payload.
    if "identity_name" not in payload or "amount" not in payload:
        return dict(msg="Please provide an identity_name and amount between [] characters.")

    identity_name = payload.get("identity_name")
    amount = payload.get("amount")
    
    community = db(db.community.name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Check if the identity exists.
    identity = db((db.identities.name == identity_name)).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")
    
    # Check if the member is a member of the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if not community_member:
        return dict(msg="Identity is not a member of the community. Join the community first.")

    reputation = db((db.reputation.identity_id == identity.id) & (db.reputation.community_id == community.id)).select().first()

    # If the reputation does not exist, create it.
    if not reputation:
        reputation = db.reputation.insert(identity_id=identity.id, community_id=community.id)
    
    # Add the amount to the member's reputation.
    reputation.update_record(reputation=reputation.reputation + amount)

    return dict(msg=f"{payload['identity_name']} has {reputation.reputation} reputation in the community {community_name}.")

# Using a community name, identity name, and amount, subtract the amount from the member's reputation in the community. If the community or
# member does not exist, return an error.
def subtract_reputation():
    community_name = request.args(0)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name, identity_name, and amount between [] characters.")
    payload = json.loads(payload)
    # Check if the identity name and amount are given in the payload.
    if "identity_name" not in payload or "amount" not in payload:
        return dict(msg="Please provide an identity_name and amount between [] characters.")

    identity_name = payload.get("identity_name")
    amount = payload.get("amount")
    
    community = db(db.community.name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Check if the identity exists.
    identity = db((db.identities.name == identity_name)).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")
    
    # Check if the member is a member of the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if not community_member:
        return dict(msg="Identity is not a member of the community. Join the community first.")

    reputation = db((db.reputation.identity_id == identity.id) & (db.reputation.community_id == community.id)).select().first()

    # If the reputation does not exist, create it.
    if not reputation:
        reputation = db.reputation.insert(identity_id=identity.id, community_id=community.id)
    
    # Subtract the amount from the member's reputation.
    reputation.update_record(reputation=reputation.reputation - amount)

    return dict(msg=f"{payload['identity_name']} has {reputation.reputation} reputation in the community {community_name}.")

# Using a community name, identity name, and amount, set the member's reputation in the community to the amount. If the community or
# member does not exist, return an error.
def set_reputation():
    community_name = request.args(0)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name, identity_name, and amount between [] characters.")
    payload = json.loads(payload)
    # Check if the identity name and amount are given in the payload.
    if "identity_name" not in payload or "amount" not in payload:
        return dict(msg="Please provide an identity_name and amount between [] characters.")

    identity_name = payload.get("identity_name")
    amount = payload.get("amount")
    
    community = db(db.community.name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Check if the identity exists.
    identity = db((db.identities.name == identity_name)).select().first()
    if not identity:
        return dict(msg="Identity does not exist.")
    
    # Check if the member is a member of the community.
    community_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == identity.id)).select().first()
    if not community_member:
        return dict(msg="Identity is not a member of the community. Join the community first.")

    reputation = db((db.reputation.identity_id == identity.id) & (db.reputation.community_id == community.id)).select().first()

    # If the reputation does not exist, create it.
    if not reputation:
        reputation = db.reputation.insert(identity_id=identity.id, community_id=community.id)

    # Set the member's reputation to the amount.
    reputation.update_record(reputation=amount)

    return dict(msg=f"{payload['identity_name']} has {reputation.reputation} reputation in the community {community_name}.")

