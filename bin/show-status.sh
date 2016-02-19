#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"

echo "# Service status"
sudo service slapd status
echo

echo "# Network status"
sudo netstat -apn | grep slapd
echo

echo "# slapcat"
sudo slapcat

echo "# /etc/default/slapd"
grep -ve "^#" -ve "^$" /etc/default/slapd
echo

echo "# Security config"
${CAT} -b cn=config -a 'olcTLSCertificateFile=*'

echo "# Suffix"
${SEARCH} -b "${SUFFIX}"

echo "# Security check 1"
OUTPUT=$(gnutls-cli-debug -p 636 "ldap.${DOMAIN}.${TOP_LEVEL}" 2>/dev/null)
OUTPUT=$(echo "${OUTPUT}" | grep -v 'unknown protocol ldaps')
echo "${OUTPUT}"
echo

echo "# Security check 2"
nmap -Pn -p T:636 --script ssl-enum-ciphers localhost