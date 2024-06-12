# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from discord.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Create a new discord channel from a given payload. Throws an error if no payload is given, or the discord channel already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'channel' not in payload or 'community_id' not in payload or 'servers' not in payload or 'aliases' not in payload:
        return dict(msg="Payload missing required fields.")
    if db((db.discord.channel == payload['channel']) & (db.discord.community_id == payload['community_id'])).count() > 0:
        return dict(msg="Discord channel already exists.")
    db.discord.insert(**payload)
    return dict(msg="Discord channel created.")

# Get all discord channels.
def get_all():
    discord_channels = db(db.discord).select()
    return dict(data=discord_channels)

# Get a discord channel by its channel name. If the discord channel does not exist, return an error.
def get_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    discord_channel = db(db.discord.channel == channel).select().first()
    if not discord_channel:
        return dict(msg="Discord channel does not exist.")
    return dict(data=discord_channel)

# Update a discord channel by its channel name. If the discord channel does not exist, return an error.
def update_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'channel' not in payload or 'community_id' not in payload or 'servers' not in payload or 'aliases' not in payload:
        return dict(msg="Payload missing required fields.")
    discord_channel = db(db.discord.channel == channel).select().first()
    if not discord_channel:
        return dict(msg="Discord channel does not exist.")
    discord_channel.update_record(**payload)
    return dict(msg="Discord channel updated.")

# Delete a discord channel by its channel name. If the discord channel does not exist, return an error.
def delete_by_channel():
    channel = request.args(0)
    channel = decode_name(channel)
    if not channel:
        return dict(msg="No channel name given.")
    discord_channel = db(db.discord.channel == channel).select().first()
    if not discord_channel:
        return dict(msg="Discord channel does not exist.")
    discord_channel.delete_record()
    return dict(msg="Discord channel deleted.")