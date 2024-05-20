import redis

testCommands = {
    "community_manage_add": {"command": "!community_manage_add", "url": "http://127.0.0.1:5000/community_new", "payload_keys": "community_name", "method": "POST", "description": "Create a new community. Example: !community_manage_add [community_name]"},
    "community_manage_rem": {"command": "!community_manage_rem", "url": "http://127.0.0.1:5000/community_delete", "payload_keys": "", "method": "DELETE", "description": "Delete a community. Example: !community_manage_rem <community_name>"},
    "community_manage_ls": {"command": "!community_manage_ls", "url": "http://127.0.0.1:5000/community_list", "payload_keys": "", "method": "GET", "description": "List all communities. Example: !community_manage_ls"},
    "community_manage_desc": {"command": "!community_manage_desc", "url": "http://127.0.0.1:5000/community_update", "payload_keys": "community_description", "method": "PUT", "description": "Add a description to a community. Example: !community_manage_desc <community_name> [description]"},
}

class RedisManager:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    # Function to add the given test commands to redis, if they do not already exist.
    def add_test_commands(self):
        for command in testCommands:
            if not self.redis.exists(command):
                self.redis.hset(command, mapping=testCommands[command])

    # Function to get a command from redis, return None if it does not exist.
    def get_command(self, command):
        if self.redis.exists(command):
            return self.redis.hgetall(command)
        return None
    
    # Function to get all commands from redis
    def get_all_commands(self):
        commands = []
        for key in self.redis.keys():
            commands.append(self.redis.hgetall(key))
        return commands
    
    # Function to get all keys from redis
    def get_all_keys(self):
        return self.redis.keys()
        

    