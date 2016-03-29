#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|add_user|list|delete NAME [GROUP_NUMBER]"
    echo "Example: ${0} add example"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
VERB="${1}"
NAME="${2}"

if [ "${VERB}" = "" ]; then
    usage

    exit 1
fi

if [ "${VERB}" = "add" ]; then
    if [ "${NAME}" = "" ]; then
        usage

        exit 1
    fi

    GROUP_DN="cn=${NAME},ou=groups,${SUFFIX}"
    GROUP_NUMBER="${3}"
    LAST_GROUP_NUMBER_FILE="last_group_number.txt"

    if [ "${GROUP_NUMBER}" = "" ]; then
        if [ -f "${LAST_GROUP_NUMBER_FILE}" ]; then
            GROUP_NUMBER="2000"
        else
            GROUP_NUMBER=$(cat "${LAST_GROUP_NUMBER_FILE}")
            GROUP_NUMBER=$(echo "${GROUP_NUMBER} + 1" | bc)
        fi
    fi

    echo "GROUP_NUMBER: ${GROUP_NUMBER}"
    echo "dn: ${GROUP_DN}
objectClass: posixGroup
cn: ${NAME}
gidNumber: ${GROUP_NUMBER}" | ${ADD_MANAGER_PASSWORD}
    echo "${GROUP_NUMBER}" > "${LAST_GROUP_NUMBER_FILE}"
elif [ "${VERB}" = "add_user" ]; then
    if [ "${NAME}" = "" ]; then
        usage

        exit 1
    fi

    GROUP_DN="cn=${NAME},ou=groups,${SUFFIX}"
    echo "Enter user to add:"
    read -r USER_NAME
    echo "dn: ${GROUP_DN}
changeType: modify
add: memberUid
memberUid: ${USER_NAME}" | ${MODIFY_MANAGER_PASSWORD} "${GROUP_DN}"
elif [ "${VERB}" = "delete" ]; then
    if [ "${NAME}" = "" ]; then
        usage

        exit 1
    fi

    GROUP_DN="cn=${NAME},ou=groups,${SUFFIX}"
    ${DELETE_MANAGER_PASSWORD} "${GROUP_DN}"
elif [ "${VERB}" = "list" ]; then
    ${SEARCH_MANAGER_PASSWORD} -b "ou=groups,${SUFFIX}" "(objectClass=posixGroup)"
fi
