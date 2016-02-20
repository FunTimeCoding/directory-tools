#!/bin/sh -e

sudo service slapd stop
sudo apt-get purge slapd
sudo rm -rf /etc/ldap
sudo rm -rf /var/lib/ldap
