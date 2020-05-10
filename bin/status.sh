#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"

echo "# Service status"
sudo systemctl status --no-pager slapd
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

if [ "${1}" = "--ssl" ]; then
    echo "# GnuTLS security check"
    echo
    OUTPUT=$(gnutls-cli-debug -p 636 "ldap.${DOMAIN}.${TOP_LEVEL}" 2>/dev/null)
    OUTPUT=$(echo "${OUTPUT}" | grep -v 'unknown protocol ldaps')
    echo "${OUTPUT}"
    echo

    echo "# NMAP security check"
    nmap -Pn -p T:636 --script ssl-enum-ciphers localhost
fi
