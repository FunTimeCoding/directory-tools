#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} FULL_NAME"
    echo "Example: ${0} \"John Doe\""
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
FULL_NAME="${1}"

if [ "${FULL_NAME}" = "" ]; then
    usage

    exit 1
fi

INTERCHANGE_FILE="/tmp/add_person.ldif"
FIRST_NAME="${FULL_NAME% *}"
LAST_NAME="${FULL_NAME#* }"
FIRST_LETTER=$(echo "${FIRST_NAME}" | head -c 1)
USER_NAME=$(echo "${FIRST_LETTER}${LAST_NAME}" | sed 's/.*/\L&/')
echo "dn: uid=${USER_NAME},ou=People,${SUFFIX}
objectClass: inetOrgPerson
description: ${FULL_NAME} Person
cn: ${FULL_NAME}
sn: ${LAST_NAME}
uid: areitzel" > "${INTERCHANGE_FILE}"
${ADD} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
