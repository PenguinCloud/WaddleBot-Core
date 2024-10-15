# -*- coding: utf-8 -*-
import json


# try something like
def index(): return dict(message="hello from communities_modules.py")

# Create a new community module from a given payload. Throws an error if no payload is given, or the community module already exists.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'module_id' not in payload or 'community_id' not in payload:
        return dict(msg="Payload missing required fields.")
    if db((db.community_modules.community_id == payload['community_id']) & (db.community_modules.module_id == payload['module_id'])).count() > 0:
        return dict(msg="Community Module already exists.")
    # Check if enabled is in the payload, if not, add it with a default value of True
    if 'enabled' not in payload:
        payload['enabled'] = True

    # Check if privilages is in the payload, if not, add it with an empty list
    if 'privilages' not in payload:
        payload['privilages'] = []

    db.community_modules.insert(**payload)
    return dict(msg="Community Module created.")

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

# Get a community module by its community id and module id. If the community module does not exist, return an error.
def get_by_community_id_and_module_id():
    community_id = request.args(0)
    module_id = request.args(1)
    if not community_id or not module_id:
        return dict(msg="No community id or module id given.")
    community_module = db((db.community_modules.community_id == community_id) & (db.community_modules.module_id == module_id)).select().first()
    if not community_module:
        return dict(msg="Community module is not installed in this community.")
    return dict(community_module=community_module)

# Get a community module by its community name and module id. If the community module does not exist, return an error.
def get_by_community_name_and_module_id():
    community_name = request.args(0)
    module_id = request.args(1)
    if not community_name or not module_id:
        return dict(msg="No community name or module id given.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community_module = db((db.community_modules.community_id == community.id) & (db.community_modules.module_id == module_id)).select().first()
    if not community_module:
        return dict(msg="Community module is not installed in this community.")
    return community_module.as_dict()

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

# Install a community module, using its module_id in a payload, into a given community_name as an argument. If the community module already exists in the given community, return an error.
def install_by_community_name():
    community_name = request.args(0)
    payload = request.body.read()
    if not community_name:
        return dict(msg="No community name given.")
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'module_id' not in payload:
        return dict(msg="Payload missing required fields.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community_module = db((db.community_modules.community_id == community.id) & (db.community_modules.module_id == payload['module_id'])).select().first()
    if community_module:
        return dict(msg="Community module already exists.")
    
    # If the community is "Global", return an error, as community modules cannot be installed in the global community.
    if community.community_name == "Global":
        return dict(msg="Cannot install community module in Global community.")

    payload['community_id'] = community.id

    # Check if enabled is in the payload, if not, add it with a default value of True
    if 'enabled' not in payload:
        payload['enabled'] = True

    # Check if privilages is in the payload, if not, add it with an empty list
    if 'privilages' not in payload:
        payload['privilages'] = []

    db.community_modules.insert(**payload)
    return dict(msg="Community module installed.")

# Uninstall a community module, using its module_id in a payload, from a given community_name as an argument. If the community module does not exist in the given community, return an error.
def uninstall_by_community_name():
    community_name = request.args(0)
    payload = request.body.read()
    if not community_name:
        return dict(msg="No community name given.")
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'module_id' not in payload:
        return dict(msg="Payload missing required fields.")
    community = db(db.communities.community_name == community_name).select().first()
    if not community:
        return dict(msg="Community does not exist.")
    community_module = db((db.community_modules.community_id == community.id) & (db.community_modules.module_id == payload['module_id'])).select().first()
    if not community_module:
        return dict(msg="Community module does not exist.")
    
    # If the community is "Global", return an error, as community modules cannot be uninstalled from the global community.
    if community.community_name == "Global":
        return dict(msg="Cannot uninstall module from Global community.")

    community_module.delete_record()
    return dict(msg="Community module uninstalled.")