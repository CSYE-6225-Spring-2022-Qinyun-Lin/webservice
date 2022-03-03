#!/bin/bash

sleep 10
export http_proxy= $Write proxy
export https_proxy= $write proxy

sudo -E yum -y update

cd ~
mkdir webservice
cp /tmp/webservice.zip ~/webservice/webservice.zip

sudo -E yum -y install unzip

cd webservice
unzip webservice.zip
ls -al
pwd

sudo -E yum -y install wget
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm

sudo  rpm -ivh mysql-community-release-el7-5.noarch.rpm
sudo -E yum -y update
sudo -E yum -y install mysql-server
sudo systemctl start mysqld
sleep 1s

# cd /var/log
# temp=`sudo grep 'password' ./mysqld.log | gawk -F 'localhost: ' '{print $2}'`
# echo $temp
# mysql -u root -p$temp --connect-expired-password -c "Alter user 'root'@'localhost' IDENTIFIED with mysql_native_password BY 'admin';"

mysql -u root <<-EOF
UPDATE mysql.user SET Password=PASSWORD('adminadmin!') WHERE User='root';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.db WHERE Db='test' OR Db='test_%';
FLUSH PRIVILEGES;
CREATE DATABASE csye6225;
use csye6225;
create table health
(
    id varchar(50) not null,
    user_name varchar(50) not null,
    password varchar(100) not null,
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    account_created datetime not null,
    account_updated datetime not null,
    constraint heath_id_uindex
        unique (id),
    constraint heath_user_name_uindex
        unique (user_name)
);

alter table health
    add primary key (id);
EOF

sudo yum -y install python3
sudo yum -y install python3-pip
sudo pip3 install flask mysql-connector

sudo cp ~/webservice/systemd/webapp.service /etc/systemd/system/webapp.service
sudo chmod 644 /etc/systemd/system/webapp.service
sudo -E yum install systemd -y
sudo systemctl daemon-reload
sudo systemctl enable webapp.service
sudo systemctl start webapp.service
