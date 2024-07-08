[![Publish Docker image](https://github.com/PenguinzPlays/MenialBotler/actions/workflows/docker-image.yml/badge.svg)](https://github.com/PenguinCloud/core/actions/workflows/docker-image.yml) [![version](https://img.shields.io/badge/version-0.0.0-yellow.svg)](https://semver.org) ![Docker Image Version (latest by date)](https://img.shields.io/docker/v//PenguinzPlays/MenialBotler?sort=date&style=plastic)


# Project Overview
WaddleBot is a combination of a watcher service, core modules and serverless scripting (Lambda / OpenWhisk) which enables you to tag and direct traffic live to scripts any time anywhere! 
The bot is built on top of MatterBridge for core chat monitoring, giving access to dozens of platforms for our core modules. We also add other libraries and API queries to supplement. 

<img height=400 alt="MenialBot Diagram" src="https://lh3.googleusercontent.com/u/0/drive-viewer/AFGJ81qdQcOY3JbDynETv3ANcdhD9rUNZvxNj3Vj5KVT-GYdDtoZee4w0NP0RTQmsQ-QPeXFS1DR0eW3ldXcu1FFqay8JfIxLA=w3799-h939"></a>

# Why this bot vs others
## Scalable and Modular
The MenialBot is able to handle a large load as the watcher service (WaddleBot Router) is only a collect and forward docker service. Simply split channels between multiple docker deployments! 
The majority of the work and slowness is in the modules. These modules are simple action scripts which are triggered based on tagging first, specifics second.

## Secured... even if the software isn't
All images under go a 8 stage security check to ensure not only is the my portion of the code secure, but to also identify and help remediate the underlying libraries and software security. 

## Updated weekly
All of our images are checked weekly for updates from upstream sources, and we have an on-staff seasoned security engineer who periodically checks our code.

## Active contribution and maintenance
PenguinzPlays has enlisted the help of his friends to ensure these images don't flop. He also uses this bot, so he doesn't want it to flop either!

## Scalable
This bot was designed to handle 1000's of channels/interfaces per cluster and keep on pressing.

## Penguinz drinks his own koolaid
Penguinz and team uses this bot first before we deploy to everyone else to identify bugs which our unit tests and automation misses.

## Beta testing
Penguinz relies on volunteer customers and community members to beta test images, ensuring our stable / production images are well baked and as bug free as possible before it goes to release candidate.

## Project Setup
To compile the project for testing/deployment, do the following:


# Contributors
## Core Maintainers: 
* Penguin@PenguinTech.io
* MJ Shepherd
*JFish

## community

* Join in and become a contributor!


# Resources
Documentation: ./docs/
Premium Support: https://support.penguintech.io
Community Bugs / Issues: -/issues
