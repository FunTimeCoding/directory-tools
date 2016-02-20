#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
echo "Config indexes:"
${SEARCH} -b cn=config olcDatabase=mdb olcDbIndex | grep -v '^$'
echo
echo "Suffix ${SUFFIX} indexes:"
${SEARCH} -b "${SUFFIX}" olcDbIndex | grep -v '^$'
