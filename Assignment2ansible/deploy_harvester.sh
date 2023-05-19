#!/bin/bash

. ./unimelb-comp90024-2023-grp-25-openrc.sh; ansible-playbook -vv deploy_harvester.yaml -i instance_hosts.ini #| tee output.txt