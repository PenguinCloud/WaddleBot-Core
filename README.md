[![Publish Docker image](https://github.com/PenguinzPlays/MenialBotler/actions/workflows/docker-image.yml/badge.svg)](https://github.com/PenguinCloud/core/actions/workflows/docker-image.yml) [![version](https://img.shields.io/badge/version-0.0.0-yellow.svg)](https://semver.org) ![Docker Image Version (latest by date)](https://img.shields.io/docker/v//PenguinzPlays/MenialBotler?sort=date&style=plastic)


# Project Overview
MenialBot is a combination of a water service (MenailBotler) and serverless scripting (Lambda / OpenWhisk) which enables you to tag and direct traffic live to scripts any time anywhere! 
The bot is built on top of MatterBridge, and supports all channels which MatterBridge does!

# Why this bot vs others
## Scalable and Modular
The MenialBot is able to handle a large load as the watcher service (MenialBotler) is only a collect and forward docker service. Simply split channels between multiple docker deployments! 
The majority of the work and slowness is in the modules. These modules are simple action scripts which are triggered based on tagging first, specifics second.

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
