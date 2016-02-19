#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"

sudo sh -c "echo \"slapd/root_password password string ${PLAIN_PASSWORD}\" | debconf-set-selections"
sudo sh -c "echo \"slapd/root_password_again password string ${PLAIN_PASSWORD}\" | debconf-set-selections"
sudo sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install slapd'
sudo apt-get install -qq ldap-utils nmap
