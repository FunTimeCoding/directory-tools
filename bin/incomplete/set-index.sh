#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
echo "dn: olcDatabase={2}mdb,cn=config
changeType: modify
add: olcDbIndex
olcDbIndex: uid eq" | ${MODIFY_SOCKET}
