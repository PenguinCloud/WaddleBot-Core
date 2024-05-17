import requests
from pydal import DAL, Field

class RolesManager:
    def __init__(self, db):
        self.db = db

    # Function to create the roles table
    def create_roles_table(self):
        self.db.define_table('roles',
                            Field('name', 'string'),
                            Field('description', 'string'),
                            Field('privilages', 'list:string'),
                            Field('requirements', 'list:string'),)
        
        self.db.commit()

    # Function to add a new role entry, if the role already exists, it will return an error
    def create_role(self, name, description, privilages, requirements): 
        # Before a new role is created, we need to check if the role already exists
        role = self.get_role_by_name(name)
        if role:
            return "Role already exists."
        else:
            self.db.roles.insert(name=name, description=description, privilages=privilages, requirements=requirements)

            self.db.commit()

            return "Role created successfully"
        
    # Function to get a role by name
    def get_role_by_name(self, name):
        role = self.db(self.db.roles.name == name).select().first()

        return role
    
    # Function to remove a role
    def remove_role(self, name):
        # Check if the role exists
        role = self.get_role_by_name(name)
        if not role:
            return "Role does not exist."

        # Remove the role
        self.db(self.db.roles.name == name).delete()

        self.db.commit()

        return "Role removed successfully"
    
    # Function to get a list of all roles
    def get_roles(self):
        roles = self.db(self.db.roles).select()

        return roles
    
    # Function to update a role
    def update_role(self, name, description, privilages, requirements):
        # Check if the role exists
        role = self.get_role_by_name(name)
        if not role:
            return "Role does not exist."

        # Update the role
        self.db(self.db.roles.name == name).update(description=description, privilages=privilages, requirements=requirements)

        self.db.commit()

        return "Role updated successfully"
