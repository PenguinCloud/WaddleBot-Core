# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from currency.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Using a community name in the arguments and an identity name in the payload, get the currency of the identity in the community. 
# If the community or identity does not exist, return an error.
def get_currency():
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

    currency = db((db.currency.identity_id == identity.id) & (db.currency.community_id == community.id)).select().first()

    # If the currency does not exist, create it.
    if not currency:
        currency = db.currency.insert(identity_id=identity.id, community_id=community.id)

    return dict(msg=f"{payload['identity_name']} has {community_member.currency} currency in the community {community_name}.")

# Using a community name, identity name, and amount, add the amount to the member's currency in the community. If the community or 
# member does not exist, return an error.
def add_currency():
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

    currency = db((db.currency.identity_id == identity.id) & (db.currency.community_id == community.id)).select().first()

    # If the currency does not exist, create it.
    if not currency:
        currency = db.currency.insert(identity_id=identity.id, community_id=community.id)
    
    # Add the amount to the member's currency.
    currency.update_record(currency=currency.currency + amount)

    return dict(msg=f"{payload['identity_name']} has {currency.currency} currency in the community {community_name}.")

# Using a community name, identity name, and amount, subtract the amount from the member's currency in the community. If the community or
# member does not exist, return an error.
def subtract_currency():
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

    currency = db((db.currency.identity_id == identity.id) & (db.currency.community_id == community.id)).select().first()

    # If the currency does not exist, create it.
    if not currency:
        currency = db.currency.insert(identity_id=identity.id, community_id=community.id)
    
    # Subtract the amount from the member's currency.
    currency.update_record(currency=currency.currency - amount)

    return dict(msg=f"{payload['identity_name']} has {currency.currency} currency in the community {community_name}.")

# Using a community name, identity name, and amount, set the member's currency in the community to the amount. If the community or
# member does not exist, return an error.
def set_currency():
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

    currency = db((db.currency.identity_id == identity.id) & (db.currency.community_id == community.id)).select().first()

    # If the currency does not exist, create it.
    if not currency:
        currency = db.currency.insert(identity_id=identity.id, community_id=community.id)

    # Set the member's currency to the amount.
    currency.update_record(currency=amount)

    return dict(msg=f"{payload['identity_name']} has {currency.currency} currency in the community {community_name}.")

# Using a community name, a sender member name, a receiver member name, and an amount, transfer the amount from the sender to the receiver. 
# If the community, sender, or receiver does not exist, return an error. If the sender does not have enough currency, return an error.
def transfer_currency():
    community_name = request.args(0)
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given. Please provide a community_name, sender_name, receiver_name, and amount between [] characters.")
    payload = json.loads(payload)
    # Check if the sender name, receiver name, and amount are given in the payload.
    if "sender_name" not in payload or "receiver_name" not in payload or "amount" not in payload:
        return dict(msg="Please provide a sender_name, receiver_name, and amount between [] characters.")

    sender_name = payload.get("sender_name")
    receiver_name = payload.get("receiver_name")
    amount = payload.get("amount")
    
    community = db(db.community.name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    
    # Check if the sender exists.
    sender = db((db.identities.name == sender_name)).select().first()
    if not sender:
        return dict(msg="Sender does not exist.")
    
    # Check if the receiver exists.
    receiver = db((db.identities.name == receiver_name)).select().first()
    if not receiver:
        return dict(msg="Receiver does not exist.")
    
    # Check if the sender is a member of the community.
    sender_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == sender.id)).select().first()
    if not sender_member:
        return dict(msg="Sender is not a member of the community. Join the community first.")
    
    # Check if the receiver is a member of the community.
    receiver_member = db((db.community_members.community_id == community.id) & (db.community_members.identity_id == receiver.id)).select().first()
    if not receiver_member:
        return dict(msg="Receiver is not a member of the community. Join the community first.")

    sender_currency = db((db.currency.identity_id == sender.id) & (db.currency.community_id == community.id)).select().first()
    receiver_currency = db((db.currency.identity_id == receiver.id) & (db.currency.community_id == community.id)).select().first()

    # If the sender's currency does not exist, create it.
    if not sender_currency:
        sender_currency = db.currency.insert(identity_id=sender.id, community_id=community.id)
    
    # If the receiver's currency does not exist, create it.
    if not receiver_currency:
        receiver_currency = db.currency.insert(identity_id=receiver.id, community_id=community.id)

    # If the sender does not have enough currency, return an error.
    if sender_currency.currency < amount:
        return dict(msg="Sender does not have enough currency.")
    
    # Subtract the amount from the sender's currency.
    sender_currency.update_record(currency=sender_currency.currency - amount)

    # Add the amount to the receiver's currency.
    receiver_currency.update_record(currency=receiver_currency.currency + amount)

    return dict(msg=f"{sender_name} has {sender_currency.currency} currency and {receiver_name} has {receiver_currency.currency} currency in the community {community_name}.")
