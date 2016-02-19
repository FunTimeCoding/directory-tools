#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
INTERCHANGE_FILE="/tmp/create_root_suffix.ldif"
echo "dn: ${SUFFIX}
objectClass: top
objectClass: dcObject
objectclass: organization
o: ${ORGANIZATION}
dc: ${DOMAIN}
description: ${ORGANIZATION} Organization" > "${INTERCHANGE_FILE}"
${ADD} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
