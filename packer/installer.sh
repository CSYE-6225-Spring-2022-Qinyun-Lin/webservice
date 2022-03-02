#!/bin/bash

sudo yum -y update

sudo yum -y install wget

sudo wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm

sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022

sudo rpm -Uvh mysql80-community-release-el7-3.noarch.rpm

sudo yum install mysql-server -y

sleep 10s

sudo systemctl start mysqld
sudo systemctl start mysqld.service
sudo service mysqld.service start

sudo mysql --version

cd /var/log
temp=`sudo grep 'password' ./mysqld.log | gawk -F 'localhost: ' '{print $2}'`

echo $temp

# mysql -u root -p$temp --connect-expired-password -c "Alter user 'root'@'localhost' IDENTIFIED with mysql_native_password BY 'admin';"

mysql -u root -p$temp <<-EOF
UPDATE mysql.user SET Password=PASSWORD('admin') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
CREATE DATABASE csye6225;
EOF

sudo yum -y install python3

sudo yum -y install python3-pip

sudo pip3 install flask mysql-connector

echo all done!
