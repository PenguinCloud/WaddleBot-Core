import requests
from pydal import DAL, Field

class RolesManager:
    def __init__(self, db):
        self.db = db

        self.create_roles_table()

    # Function to create the roles table
    def create_roles_table(self):
        print("Creating roles table")
        self.db.define_table('roles',
                            Field('name', 'string'),
                            Field('description', 'string'),
                            Field('privilages', 'list:string'),
                            Field('requirements', 'list:string'),)
        
        self.db.commit()

    # Function to add a new role entry, if the role already exists, it will return an error if the role exists
    def create_role(self, data):
        # Before a new role is created, we need to check if the role already exists
        role = self.db(self.db.roles.name == data['name']).select().first()
        if role:
            return "Role already exists."
        else:
            self.db.roles.insert(name=data['name'])

            role = self.db(self.db.roles.name == data['name']).select().first()

            if 'description' in data:
                role.update_record(description=data['description'])
            if 'privilages' in data:
                role.update_record(privilages=data['privilages'])
            if 'requirements' in data:
                role.update_record(requirements=data['requirements'])

            self.db.commit()

            return "Role created successfully"

        
    # Function to get a role by name
    def get_role_by_name(self, name):
        role = self.db(self.db.roles.name == name).select().first()

        if not role:
            return { 'error': 'Role does not exist.'}
        return role.as_dict()
    
    # Function to remove a role
    def remove_role(self, name):
        # Check if the role exists
        role = self.db(self.db.roles.name == name).select().first()
        if not role:
            return "Role does not exist."

        # Remove the role
        self.db(self.db.roles.name == name).delete()

        self.db.commit()

        return "Role removed successfully"
    
    # Function to get a list of all roles
    def get_roles(self):
        roles = self.db(self.db.roles).select()

        return roles.as_list()
    
    # Function to update a role
    def update_role(self, name, data):
        # Check if the role exists
        role = self.db(self.db.roles.name == name).select().first()
        if not role:
            return "Role does not exist."

        # Update the role
        if 'name' in data:
            role.update_record(name=data['name'])
        if 'description' in data:
            role.update_record(description=data['description'])
        if 'privilages' in data:
            role.update_record(privilages=data['privilages'])
        if 'requirements' in data:
            role.update_record(requirements=data['requirements'])

        self.db.commit()

        return "Role updated successfully"
