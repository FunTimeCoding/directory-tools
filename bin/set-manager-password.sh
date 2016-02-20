#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} NEW_PASSWORD"
    echo "Example: ${0} examplePassword"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
NEW_PASSWORD="${1}"

if [ "${NEW_PASSWORD}" = "" ]; then
    usage

    exit 1
fi

ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
INTERCHANGE_FILE="/tmp/change_manager_password.ldif"
echo "dn: olcDatabase={1}mdb,cn=config
replace: olcRootPW
olcRootPW: ${ENCRYPTED_PASSWORD}" > "${INTERCHANGE_FILE}"
${MODIFY} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
