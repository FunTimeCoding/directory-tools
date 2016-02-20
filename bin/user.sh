#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|delete|test FULL_NAME"
    echo "Example: ${0} \"John Doe\""
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
USER_PASSWORD=$(slappasswd -s "${USER_NAME}")

if [ "${VERB}" = "add" ]; then
    INTERCHANGE_FILE="/tmp/user.ldif"
    echo "dn: uid=${USER_NAME},ou=users,${SUFFIX}
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: ${FULL_NAME}
sn: ${LAST_NAME}
uid: ${USER_NAME}
uidNumber: 2000
gidNumber: 2000
homeDirectory: /home/${USER_NAME}
loginShell: /bin/bash
gecos: ${USER_NAME}
userPassword: ${USER_PASSWORD}
displayName: ${USER_NAME}
mail: ${USER_NAME}@${DOMAIN}.${TOP_LEVEL}
shadowLastChange: 0
shadowMax: 0
shadowWarning: 0" > "${INTERCHANGE_FILE}"
    ${ADD_MANAGER} -f "${INTERCHANGE_FILE}"
    rm "${INTERCHANGE_FILE}"
elif [ "${VERB}" = "test" ]; then
    echo "Who am I?"
    ${WHO} -D "uid=${USER_NAME},ou=users,${SUFFIX}"
    echo "Self search"
    ${SEARCH} -D "uid=${USER_NAME},ou=users,${SUFFIX}" -b "uid=${USER_NAME},ou=users,${SUFFIX}"
elif [ "${VERB}" = "delete" ]; then
    ${DELETE_MANAGER} "uid=${USER_NAME},ou=users,${SUFFIX}"
else
    usage

    exit 1
fi
