#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)
. "${SCRIPT_DIR}/../lib/directory_tools.sh"

sudo sh -c "echo \"slapd/root_password password string ${PLAIN_PASSWORD}\" | debconf-set-selections"
sudo sh -c "echo \"slapd/root_password_again password string ${PLAIN_PASSWORD}\" | debconf-set-selections"
sudo sh -c 'DEBIAN_FRONTEND=noninteractive apt-get install slapd'
sudo apt-get install -qq ldap-utils nmap
