#!/bin/bash

# sudo systemctl stop webapp.service

sleep 30

cd /home/ec2-user/webservice/src

sudo rm -rf ./service.py
sudo rm -rf ./db_operation.py
sudo rm -rf ./s3_operation.py
sudo rm -rf /opt/cloudwatch-config.json
