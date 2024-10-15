#!/bin/bash
ansible-playbook entrypoint.yml  -c local 
python3 web2py.py -a 'root' -i 0.0.0.0 -p 8000