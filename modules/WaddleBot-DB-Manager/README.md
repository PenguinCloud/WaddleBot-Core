# Waddlebot web2py Modules

This section of waddlebot contains all the modules and libraries to run any related applications that have been built in web2py.

# Basic Setup

To start the web2py applications, do the following:

1. Insure that you have downloaded and extracted web2py from "http://www.web2py.com/init/default/download" to anywhere on your pc.

2. Navigate to the root folder of web2py where the binary "web2py.exe" is located.

3. Copy the "waddlebot_db_manager" folder, found in this folder, over to the above mentioned root folder's "applications" folder.

4. Run "web2py.exe".

5. You will now be prompted with the server start UI. 

6. Customize the settings to your liking and ensure that you have an admin password set. Note down the port as well.

7. Click "start server".

8. The server should be running now. If you navigate to "http://127.0.0.1:8000/" you should have access to the default webpage of the modules.

# Database table value examples

Below is a list of example values for each table in the waddlebot_db_manager:

## identities

`{
    "id": 1,
    "name": "Test User",
    "country": "string",
    "ip_address": "string",
    "browser_fingerprints": [
        "test"
    ]
}`

## communities

`{
    "id": 6,
    "community_name": "test",
    "community_description": ""
}`

## community_members

`{
    "id": 1,
    "community_id": 1,
    "identity_id": 1,
    "role_id": 4,
    "currency": 0,
    "reputation": 0
}`

## community_modules

`{
    "id": 1,
    "module_id": 1,
    "community_id": 2,
    "enabled": true,
    "privilages": [
        "Read", "Write"
    ]
}`

## roles

`{
    "id": 2,
    "name": "Owner",
    "description": "This role is the owner of a community.",
    "privilages": [
        "read",
        "write",
        "update",
        "install",
        "ban"
    ],
    "requirements": []
}`

## marketplace

`{
    "id": 2,
    "name": "Community",
    "description": "A test set of commands for the community",
    "gateway_url": "http://127.0.0.1:8000/waddlebot_db_manager/communities/",
    "module_type_id": 1,
    "metadata": {
        "!community": {
            "manage": {
                "add": {
                    "description": "Add a new community. Example: !community manage add [my_community]",
                    "method": "POST",
                    "action": "create_by_name.json",
                    "parameters": [],
                    "payload_keys": [
                        "identity_name",
                        "community_name"
                    ]
                },
                "desc": {
                    "description": "Add a description to a community. Example: !community manage desc [My community description] <my_community>",
                    "method": "PUT",
                    "action": "update_desc_by_name.json",
                    "parameters": [
                        {
                            "name": "name",
                            "description": "The name of the community",
                            "required": true
                        }
                    ],
                    "payload_keys": [
                        "community_description"
                    ]
                },
                "rem": {
                    "description": "Remove a community. Example: !community manage rem <my_community>",
                    "method": "DELETE",
                    "action": "delete_by_name.json",
                    "parameters": [
                        {
                            "name": "name",
                            "description": "The name of the community",
                            "required": true
                        }
                    ],
                    "payload_keys": []
                },
                "ls": {
                    "description": "List all the communities. Example: !community manage ls",
                    "method": "GET",
                    "action": "get_all.json",
                    "parameters": [],
                    "payload_keys": []
                }
            }
        }
    },
    "module_type_name": "Core"
}`

## modules_types

`{
    "id": 1,
    "name": "Core",
    "description": "This type of module must be installed into a community to work."
},
{
    "id": 2,
    "name": "Community",
    "description": "This type of module must be installed into a community to work."
},`