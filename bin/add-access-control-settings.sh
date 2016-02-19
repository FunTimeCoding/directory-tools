#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
INTERCHANGE_FILE="/tmp/add_access_control_settings.ldif"
echo "dn: olcDatabase={2}mdb,cn=config
changeType: modify
add: olcAccess
olcAccess: to attrs=userPassword,shadowLastChange by self write by anonymous auth by * none
add: olcAccess
olcAccess: to dn.base=\"\" by * read
add: olcAccess
olcAccess: to * by * read" > "${INTERCHANGE_FILE}"
${MODIFY} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
