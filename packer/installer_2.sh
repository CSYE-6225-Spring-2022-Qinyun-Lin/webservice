#!/bin/bash

sleep 10
export http_proxy= $Write proxy
export https_proxy= $write proxy

sudo -E yum -y update

sudo -E yum -y install wget
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm

sudo  rpm -ivh mysql-community-release-el7-5.noarch.rpm
sudo -E yum -y update
sudo -E yum -y install mysql-server
sudo systemctl start mysqld
sleep 1s

mysql -u root <<-EOF
UPDATE mysql.user SET Password=PASSWORD('adminadmin!') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
CREATE DATABASE webapp;
EOF

sudo yum -y install python3

sudo yum -y install python3-pip

sudo pip3 install flask mysql-connector