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

if [ "${VERB}" = "add" ]; then
    echo "dn: ou=${NAME},${SUFFIX}
objectClass: organizationalUnit
ou: ${NAME}" | ${ADD_MANAGER}
elif [ "${VERB}" = "delete" ]; then
    ${DELETE_MANAGER} "dn: ou=${NAME},${SUFFIX}"
else
    usage

    exit 1
fi
