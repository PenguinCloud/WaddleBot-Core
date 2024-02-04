#!/bin/bash
ansible-playbook entrypoint.yml  -c local 
matterbridge -c /etc/matterbridge.toml