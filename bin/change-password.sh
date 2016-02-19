#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} USER_NAME NEW_PASSWORD"
    echo "Example: ${0} jdoe examplePassword"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
USER_NAME="${1}"
NEW_PASSWORD="${1}"

if [ "${USER_NAME}" = "" ]; then
    usage

    exit 1
fi

if [ "${NEW_PASSWORD}" = "" ]; then
    usage

    exit 1
fi

ENCRYPTED_PASSWORD=$(slappasswd -s "${PLAIN_PASSWORD}")
INTERCHANGE_FILE="/tmp/change_password.ldif"
echo "dn: uid=${USER_NAME},${SUFFIX}
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" > "${INTERCHANGE_FILE}"
${MODIFY} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
