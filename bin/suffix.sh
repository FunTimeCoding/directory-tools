#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"

if [ "${1}" = "--all" ]; then
    ${SEARCH_SOCKET} -b cn=config 'olcSuffix=*' olcSuffix | grep -v '^$'
else
    echo "Enter manager password:"
    #${SEARCH_MANAGER} -b "${SUFFIX}" | grep -v '^$'
    ${SEARCH_MANAGER} -b "${SUFFIX}"
fi
