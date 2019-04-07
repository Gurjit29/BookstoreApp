#!/bin/sh
apt-get update
apt-get install python3 -y
apt-get install npm -y
pip install -r requirements.txt
npm install jquery
npm install popper.js
npm install bootstrap
