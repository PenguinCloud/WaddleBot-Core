import redis

# TODO: Remove these test commands when the cache is officially deployed
testCommands = {
    "!community": "http://127.0.0.1:5000/community",
    "!marketplace": "http://127.0.0.1:6300/marketplace/",
}

class RedisCache:
    def __init__(self, host, port):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    # Function to add the given test commands to redis, if they do not already exist.
    def add_test_commands(self):
        for command in testCommands:
            if not self.redis.exists(command):
                self.redis.set(command, testCommands[command])

    # Function to get a command from redis, return None if it does not exist.
    def get_command(self, command):
        if self.redis.exists(command):
            return self.redis.get(command)
        return None
    
    # Function to get all commands from redis
    def get_all_commands(self):
        commands = []
        for key in self.redis.keys():
            commands.append(key + ": " + self.redis.get(key))
        return commands
    
    # Function to get all keys from redis
    def get_all_keys(self):
        return self.redis.keys()
        

    