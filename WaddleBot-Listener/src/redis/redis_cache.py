import redis

# TODO: Remove these test commands when the cache is officially deployed
testCommands = {
    # Community related commands
    "!community_manage_add": "http://127.0.0.1:8000/waddlebot_db_manager/communities/",
    "!community_manage_desc": "http://127.0.0.1:8000/waddlebot_db_manager/communities/",
    "!community_manage_rem": "http://127.0.0.1:8000/waddlebot_db_manager/communities/",
    "!community_manage_ls": "http://127.0.0.1:8000/waddlebot_db_manager/communities/",
    # Community Member related commands
    "!community_join": "http://127.0.0.1:8000/waddlebot_db_manager/community_members/",
    "!community_leave": "http://127.0.0.1:8000/waddlebot_db_manager/community_members/",
    "!community_members_ls": "http://127.0.0.1:8000/waddlebot_db_manager/community_members/",
    "!community_update_role": "http://127.0.0.1:8000/waddlebot_db_manager/community_members/",
    # Context related commands
    "!namespace_switch":"http://127.0.0.1:8000/waddlebot_db_manager/context/",
    # Marketplace Related Commands
    "!marketplace_ls": "http://127.0.0.1:8000/marketplace_manager/marketplace/",
    "!marketplace_install": "http://127.0.0.1:8000/waddlebot_db_manager/community_modules/",
    "!marketplace_uninstall": "http://127.0.0.1:8000/waddlebot_db_manager/community_modules/",
    # Gateway route related commands
    "!gateway_add": "http://127.0.0.1:5000/gateway-creator/",
    "!gateway_rem": "http://127.0.0.1:5000/gateway-creator/",
    # Routing related commands
    "!route_add": "http://127.0.0.1:8000/waddlebot_db_manager/routing/",
    "!route_rem": "http://127.0.0.1:8000/waddlebot_db_manager/routing/",
    # Test script related commands
    "#test_script": "http://127.0.0.1:8000/waddlebot_db_manager/test_script/"
    
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
        

    