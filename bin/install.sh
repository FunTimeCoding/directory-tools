#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
echo "slapd slapd/password1 password ${MANAGER_PASSWORD}" | sudo debconf-set-selections
echo "slapd slapd/password2 password ${MANAGER_PASSWORD}" | sudo debconf-set-selections
sudo apt-get install -qq slapd ldap-utils nmap
