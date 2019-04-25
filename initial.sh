#!/bin/sh
if apt-get update; then
    apt-get install python3 -y
    pip install -r requirements.txt
    apt-get install npm -y
else
    yum install python3
    pip install -r requirements.txt
fi

curl -sL https://deb.nodesource.com/setup_10.x | -E bash -
apt-get install -y nodejs
apt-get install npm -y
npm install jquery
npm install popper.js
npm install bootstrap