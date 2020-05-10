#!/bin/sh -e

if [ ! -d /etc/ldap/slapd.d ]; then
    echo "Configuration directory not found."

    exit 1
fi

if [ ! -d /var/lib/ldap ]; then
    echo "Data directory not found."

    exit 1
fi

sudo systemctl stop slapd
DATE=$(date '+%Y-%m-%d')

sudo mv /etc/ldap/slapd.d "/etc/ldap/slapd.d-${DATE}"
sudo mkdir /etc/ldap/slapd.d
sudo chown openldap:openldap /etc/ldap/slapd.d
sudo slapadd -n 0 -F /etc/ldap/slapd.d -l tmp/configuration.ldif

sudo mv /var/lib/ldap "/var/lib/ldap-${DATE}"
sudo mkdir /var/lib/ldap
sudo chown openldap:openldap /var/lib/ldap
sudo slapadd -n 0 -F /var/lib/ldap -l tmp/data.ldif

sudo systemctl start slapd
