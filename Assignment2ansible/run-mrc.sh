#!/bin/bash

ansible-galaxy collection install openstack.cloud:2.0.0
. /unimelb-comp90024-2023-grp-25-openrc.sh; ansible-playbook -vv mrc.yaml | tee output.txt
