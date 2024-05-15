import requests
from pydal import DAL, Field

class UserManager:
    def __init__(self, db):
        # self.connectionString = connectionString
        # self.db = DAL(connectionString,pool_size=0)
        self.db = db
        
    # Function to create the user table
    def create_user_table(self):
        self.db.define_table('users', 
                            Field('username'))
        self.db.commit()

    # Function to create a new user, if the user already exists, it will return an error
    def create_user(self, username):

        # Before a new user is created, we need to check if the user already exists
        user = self.get_user_by_name(username)
        if user:
            return "User already exists."
        else:
            self.db.users.insert(username=username)

            self.db.commit()

            return "User created successfully"
    
    # Function to retrieve a specific user by username
    def get_user_by_name(self, username):
        user = self.db(self.db.users.username == username).select().first()

        return user

# def create_user_table(connectionString):
#     db = DAL(connectionString)

#     db.define_table('users', Field('name'))

#     db.commit()
