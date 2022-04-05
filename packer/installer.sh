#!/bin/bash

sleep 10
export http_proxy= $Write proxy
export https_proxy= $write proxy

# update yum and install packages
sudo -E yum -y update
sudo -E yum -y install unzip
sudo yum install ruby -y
sudo yum install wget -y

sleep 1s

# move the application to right place and unzip it
cd ~
mkdir webservice
cp /tmp/webservice.zip /home/ec2-user/webservice/webservice.zip
cd webservice
unzip webservice.zip
ls -al
pwd

sleep 1s

# install CodeDeploy
CODEDEPLOY_BIN="/opt/codedeploy-agent/bin/codedeploy-agent"
$CODEDEPLOY_BIN stop
sudo yum erase codedeploy-agent -y

cd /home/ec2-user
sudo wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
sudo chmod +x ./install

sudo ./install auto
sudo service codedeploy-agent status

# install and config CloudWatch Agent
sudo yum install amazon-cloudwatch-agent -y

# install python3 and required libs
sudo yum -y install python3
sudo yum -y install python3-pip
sudo pip3 install flask mysql-connector boto3 statsd
