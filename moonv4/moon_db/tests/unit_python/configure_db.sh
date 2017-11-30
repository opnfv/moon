#!/usr/bin/env bash

apt-get install mysql-server python-mysqldb python-pymysql

mysql -uroot -ppassword <<EOF
CREATE DATABASE moon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON moon.* TO 'moonuser'@'%' IDENTIFIED BY 'password';
GRANT ALL ON moon.* TO 'moonuser'@'localhost' IDENTIFIED BY 'password';
EOF
