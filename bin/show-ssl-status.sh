#!/bin/sh -e
# Not needed anymore since SSL support is deprecated.

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"

echo "# GnuTLS security check"
echo
OUTPUT=$(gnutls-cli-debug -p 636 "ldap.${DOMAIN}.${TOP_LEVEL}" 2>/dev/null)
OUTPUT=$(echo "${OUTPUT}" | grep -v 'unknown protocol ldaps')
echo "${OUTPUT}"
echo

echo "# NMAP security check"
nmap -Pn -p T:636 --script ssl-enum-ciphers localhost
