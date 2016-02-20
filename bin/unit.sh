#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|delete NAME"
    echo "Example: ${0} \"users\""
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
VERB="${1}"
NAME="${2}"

if [ "${NAME}" = "" ]; then
    usage

    exit 1
fi

INTERCHANGE_FILE="/tmp/unit.ldif"

if [ "${VERB}" = "add" ]; then
    echo "dn: ou=${NAME},${SUFFIX}
objectClass: top
objectClass: organizationalUnit
ou: ${NAME}" > "${INTERCHANGE_FILE}"
    ${ADD} -f "${INTERCHANGE_FILE}"
    rm "${INTERCHANGE_FILE}"
elif [ "${VERB}" = "delete" ]; then
    echo "dn: ou=${NAME},${SUFFIX}
changeType: delete" > "${INTERCHANGE_FILE}"
    ${MODIFY} -f "${INTERCHANGE_FILE}"
    rm "${INTERCHANGE_FILE}"
else
    usage

    exit 1
fi
