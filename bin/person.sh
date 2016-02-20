#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|delete FULL_NAME"
    echo "Example: ${0} add \"John Doe\""
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
VERB="${1}"
FULL_NAME="${2}"

if [ "${FULL_NAME}" = "" ]; then
    usage

    exit 1
fi

FIRST_NAME="${FULL_NAME% *}"
LAST_NAME="${FULL_NAME#* }"
FIRST_LETTER=$(echo "${FIRST_NAME}" | head -c 1)
USER_NAME=$(echo "${FIRST_LETTER}${LAST_NAME}" | sed 's/.*/\L&/')

if [ "${VERB}" = "add" ]; then
    echo "dn: uid=${USER_NAME},ou=people,${SUFFIX}
objectClass: inetOrgPerson
cn: ${FULL_NAME}
sn: ${LAST_NAME}
uid: ${USER_NAME}" | ${ADD_MANAGER}
elif [ "${VERB}" = "delete" ]; then
    ${DELETE_MANAGER} "uid=${USER_NAME},ou=people,${SUFFIX}"
else
    usage

    exit 1
fi
