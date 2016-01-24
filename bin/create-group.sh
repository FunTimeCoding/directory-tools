#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)
. "${SCRIPT_DIR}/../lib/directory_tools.sh"
INTERCHANGE_FILE="/tmp/create_group.ldif"
echo "dn: ou=People,dc=${DOMAIN},dc=${TOP_LEVEL}
objectClass: organizationalUnit
ou: People" > "${INTERCHANGE_FILE}"
${ADD} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
