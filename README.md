[![Publish Docker image](https://github.com/PenguinzPlays/MenialBotler/actions/workflows/docker-image.yml/badge.svg)](https://github.com/PenguinCloud/core/actions/workflows/docker-image.yml) [![version](https://img.shields.io/badge/version-0.0.0-yellow.svg)](https://semver.org) ![Docker Image Version (latest by date)](https://img.shields.io/docker/v//PenguinzPlays/MenialBotler?sort=date&style=plastic)


# Project Overview
MenialBot is a combination of a water service (MenailBotler) and serverless scripting (Lambda / OpenWhisk) which enables you to tag and direct traffic live to scripts any time anywhere! 
The bot is built on top of MatterBridge, and supports all channels which MatterBridge does!

# Why this bot vs others
## Scalable and Modular
The MenialBot is able to handle a large load as the watcher service (MenialBotler) is only a collect and forward docker service. Simply split channels between multiple docker deployments! 
The majority of the work and slowness is in the modules. These modules are simple action scripts which are triggered based on tagging first, specifics second.

## Flow
### Tags
Each chat message is evaluated against a tag, which are general types or classes or modules. The most basic three are Command, Event and Chat.
Commands look for an ! , events looks for key notifications from the platform (such as trains, subscription, etc. on Twitch), and finally the chat tag does string matches for specifics on chats... keep these at a minimal as they are the most resource intensive!
Behind the scenes, each tag is a python3.11 class! Some tags support parameters afterwards, while some dont. See documentation for Tags.

### Specifics
The specifics are the actual modules of the tag class. These are either pre-built into the tag class which are there from the start, or optional installed from either the store or locally. Common modules installed fall into core project extension modules, or community modules!
Specifics are essentially a function (though they may utilize sub-functions) and may take or require a parameter. See documentation for specifics.

## Examples
### Tag: Command
#### Specific: 
* !help - List how to use the command tag

### Tag: Event
#### Specifc: 
* TwitchSub - Actions to take when a subscriber to twitch happens

### Tag: Chat
#### Specifics: 
* Racist or Unwanted Word - matches on word and takes an action

## Some prebuilt-in always available modules
### Tag: Community <name>
#### Specifics: 
* Manage <action> - Manages communities which you have access to! Common Actions:
  * add <name> - Creates a community if you are a premium user (counts against your community credits!)
  * rem <name> - Removes a community if you are the communities' owner
  * ls <optional pattern> - Basic search / listing of available communities (supports asterisks for wildcard)
  * desc <description> - Sets a description
* Attribute <action> - These are used to categorize or label communities using available options. Common actions:
  * add <name> - adds an attribute to the channel, common attributes are: LGBTQ+, Religious, Military, Women, Sports, Gaming, Competition, Music, LifeSkills (this encompases fitness, cooking, etc.) , and more!
  * ls <optional pattern> - Basic search / listing of available attributes (supports asterisks for wildcard)
  * rem <name> - Removes attribute
  * search <attribute> <optional pattern> - Lists all communities which have the attribute and match the pattern 
* Channel <action> <name> - Only allows this community to be used on specific channels, if this specific is never hit, communities are global! Common Actions: 
  * add - Adds a channel by name or ID (depending on platform support)
  * rem - Remove channel by name or ID (depending on platform support)
  * ls <optional pattern> - List all available channels in the community by name or ID (depending on platform support) (supports asterisks for wildcard)
* Currency <action> <name> - Manages currency for a user (or any for all). Common actions: 
  * add <amount> <name> - Adds currency to the user specified (or any for all)
  * active <amount> <name> <timeout> <pattern> - Adds currency to the user specified (or any for all) if they type something which matches the pattern within timeout (timeout is in seconds)
  * rem <amount> <name> - Removes currency from the user specified (or any for all)
  * give <amount> <name> - Takes from user who initiated workflow and gives to specified user
  * ls <optional pattern> - Specifies where on the scoreboard a user (or any for all) lands position wise!
  * raffle <amount> <mode> <timeout> - Allows users to enter into a raffle for currency, common modes are: single, multi, roulette and timeout is in seconds!
* Name <name> - Sets the name to the new specified name
* Prize <action> - Creates a prize for a raffle / giveaway!
  * add <name> <description> <cost> <timeout> - Adds a Prize for which the community can enter for a chance to get! Timeout is in seconds! 
  * rem <name> - Removes the prize without a winner
  * winner <name> [announce] - Closes the prize and sets the winner to user id / name specified and if announce afterwards, will announce in the channels within the community
  * active <name> <timeout> <pattern> [announce] - Sets the prize to claiming status and sets the winner to user id / name specified and if announce afterwards, will announce in the channels within the community, winner must claim the prize within timeout (timeout in seconds) by matching the pattern
  * ls <status> <optional pattern> - List available prizes within community (supports asterisks for wildcard). Statuses: Open, Claiming, Closed . If the status is Claiming, will state winner and amount of time remaining to claim
* Role <action> - The global community has the following roles for example: Premium (For premium SaaS users, Creator (a la streamer). Common Actions: 
  * ls <optional pattern> - gives a list of all community roles 
  * add <name> - creates a new role with specified name
  * rem  <name> - removes a role
* User <action> - Manages users within the community. Common actions:
  * ls <optional pattern> - gives a list of roles the user is assigned to
  * add <name> <role> - Adds the user to the role
  * rem <name> <role> - Removes the user from the role
* More to come!

### Tag: Policy <tag name> <specific name> [parameter] (If parameter is availble, must be set, or use any for all of them)
#### Specifics:
* Role <action> - Manages the access list for roles. Common actions:
  * add <name> - Adds the role to the allow list
  * rem <name> - Removes the role from the allow list
  * ls - List the allow list of roles

### Tag: User <name>
#### Specifics:
 * RepCheck - Bans, Timeouts, Censor Hits, Channels Modding, etc. turn into a reputation score... everyone starts at 0
 * Ban - Bans user from channel
 * RemBan - Removes ban from user specified
 * TimeOut <time>  - Times out user for specified time in seconds (must match platform options) for user specified
 * RemTime - Removes time out for the user specified
 * RoleAdd 
 * IDValidation - Utilizes a third party service to validate your identity... which boosts your reputation
 * Puzzle - Asks the user a question (math, basic science, ascii word id, etc.) which they must pass or loose reputation (bot defense)
 
### Tag: DoorCheck
#### Specifics:
* ChatReq <role name> <req name> - Sets requirements for the role of users before they can chat. Only applies first matched role, global community is always last. Common requirement names:
  * time <time>- Amount of time the user in this role has to be in the channel before they can talk
  * follow <bool> - Is the user in this role a follower (twitch) or subscriber (youtube) etc. of the channel
  * backer <bool> - Is the user in this role providing monetary support to this channel
  * IDValidation <bool> - Has the user in this role went through the ID Validation
  * Reputation <score> - Has the user in this role met or surpassed the reputation score set?
  * Puzzle <puzzle name> - Give the user in this role a puzzle which they must pass before they can chat
* RoleReq <community name> <role name> - Sets what roles in what communities are allowed, for example a common global role is Creator (a la streamer)... you can allow or disallow. This can be used to just allow your community members to join the chat. Any users which do not match any of these (when set) will automatically be timed out continously at the max timeout for the platform.
* AutoShout <community name> <role name> <optional text> - Sends a shoutout message to the channel when a user belonging to a community and role starts chatting on the channel, some platforms will add additional details (such as last game played) as well, if available.

### Tag: Alias
Specifics:
* Link <name> <action> - a linker object. Common actions:
  * tag <name> <param> - Sets the tag and it's params for this linker (required before link object goes active)
  * specific <name> <param> - Sets the specific and it's params for this linker
  * desc <description> - Sets the description for this alias
  * ls <optional pattern> - List available aliases
Because of the simplicity of the core code, it runs lightweight!

## Secured... even if the software isn't
All images under go a 8 stage security check to ensure not only is the my portion of the code secure, but to also identify and help remediate the underlying libraries and software security. 

## Updated weekly
All of our images are checked weekly for updates from upstream sources.

## Active contribution and maintenance
PenguinzPlays has enlisted the help of his friends to ensure these images don't flop. He also uses this bot, so he doesn't want it to flop either!

## Scalable
ALl PTG images are designs to be micro-containers, ensuring easy verical and horizontal scaling is possible.

## Penguinz drinks his own koolaid
Penguinz uses his own images for everything sohe can identify bugs which our automation misses.

## Beta testing
Penguinz relies on volunteer customers and community members to beta test images, ensuring our stable / production images are well baked and as bug free as possible solutions.

## 
# Contributors
## PenguinzPlays
Maintainer: Penguin@PenguinTech.io
General: menialbot@penguintech.io

## community

* Join in and become a contributor!


# Resources
Documentation: ./docs/
Premium Support: https://support.penguintech.io
Community Bugs / Issues: -/issues
