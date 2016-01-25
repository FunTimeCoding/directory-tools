#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)
. "${SCRIPT_DIR}/../lib/directory_tools.sh"
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
