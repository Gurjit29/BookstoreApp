#!/bin/sh
if apt-get update; then
    apt-get install python3 -y
    apt-get install npm -y
else
    yum install python3
    yum install npm
fi
pip install -r requirements.txt
npm install jquery
npm install popper.js
npm install bootstrap
