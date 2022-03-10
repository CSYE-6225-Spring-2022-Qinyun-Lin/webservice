#!/bin/bash

sleep 10
export http_proxy= $Write proxy
export https_proxy= $write proxy

# update yum and install unzip
sudo -E yum -y update
sudo -E yum -y install unzip

# move the application to right place and unzip it
cd ~
mkdir webservice
cp /tmp/webservice.zip /home/ec2-user/webservice/webservice.zip
cd webservice
unzip webservice.zip
ls -al
pwd

sleep 1s

# installing python3 and required libs
sudo yum -y install python3
sudo yum -y install python3-pip
sudo pip3 install flask mysql-connector boto3
