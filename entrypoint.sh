#!/bin/bash
ansible-playbook entrypoint.yml -c local 
matterbridge -conf /etc/matterbridge.toml