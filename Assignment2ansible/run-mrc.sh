#!/bin/bash

ansible-galaxy collection install openstack.cloud:2.0.0
. /Users/sennhang/Documents/CCC/A2/pt-74505-openrc.sh; ansible-playbook -vv mrc.yaml | tee output.txt
