#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} NAME"
    echo "Example: ${0} \"users\""
}

. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
NAME="${1}"

if [ "${NAME}" = "" ]; then
    usage

    exit 1
fi

INTERCHANGE_FILE="/tmp/add_unit.ldif"
echo "dn: ou=${NAME},${SUFFIX}
objectClass: top
objectClass: organizationalUnit
ou: ${NAME}" > "${INTERCHANGE_FILE}"
${ADD} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
