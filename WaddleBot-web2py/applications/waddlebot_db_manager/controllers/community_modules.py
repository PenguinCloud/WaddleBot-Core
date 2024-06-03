# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities_modules.py")

# Create a community module from a given payload. Throws an error if no payload is given, or the module already exists in a given community id
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'module_id' not in payload or 'community_id' not in payload:
        return dict(msg="Payload missing required fields.")
    if db((db.community_modules.module_id == payload['module_id']) & (db.community_modules.community_id == payload['community_id'])).count() > 0:
        return dict(msg="Community module already exists in this community.")
    db.community_modules.insert(**payload)
    return dict(msg="Community module created.")

# Get all community modules accross all communities.
def get_all():
    community_modules = db(db.community_modules).select()
    return dict(data=community_modules)

# Get all community modules in a given community id.
def get_by_community_id():
    community_id = request.args(0)
    if not community_id:
        return dict(msg="No community id given.")
    community_modules = db(db.community_modules.community_id == community_id).select()
    return dict(data=community_modules)

# Update a community module by its community id and module id. If the community module does not exist, return an error.
def update_by_community_id_and_module_id():
    community_id = request.args(0)
    module_id = request.args(1)
    if not community_id or not module_id:
        return dict(msg="No community id or module id given.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'module_id' not in payload or 'community_id' not in payload or 'enabled' not in payload or 'privilages' not in payload:
        return dict(msg="Payload missing required fields.")
    community_module = db((db.community_modules.community_id == community_id) & (db.community_modules.module_id == module_id)).select().first()
    if not community_module:
        return dict(msg="Community module does not exist.")
    community_module.update_record(**payload)
    return dict(msg="Community module updated.")

# Delete a community module by its community id and module id. If the community module does not exist, return an error.
def delete_by_community_id_and_module_id():
    community_id = request.args(0)
    module_id = request.args(1)
    if not community_id or not module_id:
        return dict(msg="No community id or module id given.")
    community_module = db((db.community_modules.community_id == community_id) & (db.community_modules.module_id == module_id)).select().first()
    if not community_module:
        return dict(msg="Community module does not exist.")
    community_module.delete_record()
    return dict(msg="Community module deleted.")