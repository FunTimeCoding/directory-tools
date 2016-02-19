#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
INTERCHANGE_FILE="/tmp/add_index.ldif"
echo "dn: olcDatabase={2}mdb,cn=config
changeType: modify
add: olcDbIndex
olcDbIndex: uid eq" > "${INTERCHANGE_FILE}"
${MODIFY} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"