#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|add_user|delete NAME [GROUP_NUMBER]"
    echo "Example: ${0} add example"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
VERB="${1}"
NAME="${2}"

if [ "${NAME}" = "" ]; then
    usage

    exit 1
fi

GROUP_DN="cn=${NAME},ou=groups,${SUFFIX}"

if [ "${VERB}" = "add" ]; then
	GROUP_NUMBER="${3}"

	if [ "${GROUP_NUMBER}" = "" ]; then
		GROUP_NUMBER_FILE="group_number.txt"

		if [ ! -f "${GROUP_NUMBER_FILE}" ]; then
			echo "2000" > "${GROUP_NUMBER_FILE}"
    	fi

    	GROUP_NUMBER=$(cat "${GROUP_NUMBER_FILE}")
	fi

	echo "GROUP_NUMBER: ${GROUP_NUMBER}"
    echo "dn: ${GROUP_DN}
objectClass: posixGroup
cn: ${NAME}
gidNumber: ${GROUP_NUMBER}" | ${ADD_MANAGER}
    NEXT_GROUP_NUMBER=$(echo "${GROUP_NUMBER} + 1" | bc)
    echo "${NEXT_GROUP_NUMBER}" > "${GROUP_NUMBER_FILE}"
elif [ "${VERB}" = "add_user" ]; then
	echo "Enter user to add:"
	read -r USER_NAME
    echo "dn: ${GROUP_DN}
changeType: modify
add: memberUid
memberUid: ${USER_NAME}" | ${MODIFY_MANAGER}
elif [ "${VERB}" = "delete" ]; then
    ${DELETE_MANAGER} "${GROUP_DN}"
else
    usage

    exit 1
fi
