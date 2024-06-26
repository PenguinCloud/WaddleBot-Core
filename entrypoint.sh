#!/bin/bash
ansible-playbook entrypoint.yml -c local --tags "configure"
matterbridge -conf /etc/matterbridge/matterbridge.toml