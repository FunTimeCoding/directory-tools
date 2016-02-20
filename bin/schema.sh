#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"

if [ "${1}" = "--full" ]; then
    ${SEARCH_SOCKET} -b cn=schema,cn=config | grep -v '^$'
else
    ${SEARCH_SOCKET} -b cn=schema,cn=config '(objectClass=olcSchemaConfig)' dn | grep -v '^$'
fi
