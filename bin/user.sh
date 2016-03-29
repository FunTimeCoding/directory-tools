#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} add|delete|change_password|set_password|test USERNAME FULL_NAME [USER_NUMBER]"
    echo "Example: ${0} jd \"John Doe\""
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
VERB="${1}"
USERNAME="${2}"
FULL_NAME="${3}"

if [ "${VERB}" = "" ] || [ "${USERNAME}" = "" ] || [ "${FULL_NAME}" = "" ]; then
    usage

    exit 1
fi

FIRST_NAME="${FULL_NAME% *}"
LAST_NAME="${FULL_NAME#* }"
FIRST_LETTER=$(echo "${FIRST_NAME}" | head -c 1)
USERNAME=$(echo "${FIRST_LETTER}${LAST_NAME}" | sed 's/.*/\L&/')
USER_PASSWORD=$(slappasswd -s "${USERNAME}")
USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"

if [ "${VERB}" = "add" ]; then
    USER_NUMBER="${4}"

    if [ "${USER_NUMBER}" = "" ]; then
        USER_NUMBER_FILE="user_number.txt"

        if [ ! -f "${USER_NUMBER_FILE}" ]; then
            echo "2000" > "${USER_NUMBER_FILE}"
        fi

        USER_NUMBER=$(cat "${USER_NUMBER_FILE}")
    fi

    echo "USER_NUMBER: ${USER_NUMBER}"
    echo "Enter group number:"
    read -r GROUP_NUMBER
    echo "dn: ${USER_DN}
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
cn: ${FULL_NAME}
sn: ${LAST_NAME}
uid: ${USERNAME}
uidNumber: ${USER_NUMBER}
gidNumber: ${GROUP_NUMBER}
homeDirectory: /home/${USERNAME}
loginShell: /bin/bash
gecos: ${FULL_NAME}
userPassword: ${USER_PASSWORD}
displayName: ${USERNAME}
mail: ${USERNAME}@${DOMAIN}.${TOP_LEVEL}
shadowLastChange: 0
shadowMax: 0
shadowWarning: 0" | ${ADD_MANAGER}
    NEXT_USER_NUMBER=$(echo "${USER_NUMBER} + 1" | bc)
    echo "${NEXT_USER_NUMBER}" > "${USER_NUMBER_FILE}"
elif [ "${VERB}" = "test" ]; then
    echo "Who am I?"
    ${WHO} -D "${USER_DN}"
    echo "Self search"
    ${SEARCH} -D "uid=${USERNAME},ou=users,${SUFFIX}" -b "uid=${USERNAME},ou=users,${SUFFIX}"
elif [ "${VERB}" = "set_password" ]; then
    echo "Enter new password:"
    read -r NEW_PASSWORD
    ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
    echo "Enter manager password:"
    echo "dn: ${USER_DN}
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" | ${MODIFY_MANAGER}
elif [ "${VERB}" = "change_password" ]; then
    echo "Enter new password:"
    read -r NEW_PASSWORD
    ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
    echo "Enter current password:"
    echo "dn: ${USER_DN}
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" | ${MODIFY} -D "uid=${USERNAME},ou=users,${SUFFIX}"
elif [ "${VERB}" = "delete" ]; then
    ${DELETE_MANAGER} "${USER_DN}"
fi
