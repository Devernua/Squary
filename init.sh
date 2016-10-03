#!/usr/bin/bash

sudo nginx -s stop
sudo rm /etc/nginx/sites-avalible/default
sudo rm /etc/nginx/sites-enabled/default
sudo ln -sf $PWD/etc/nginx.conf /etc/nginx/conf.d/squary.conf

sudo nginx
