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

if [ "${VERB}" = "" ]; then
    usage

    exit 1
fi

if [ "${VERB}" = "add" ]; then
    if [ "${USERNAME}" = "" ]; then
        usage

        exit 1
    fi

    FULL_NAME="${3}"
    USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"

    # TODO: Either make username derived from real name optional or let usernames be nicknames and enforce them with a tight convention.
    #FIRST_LETTER=$(echo "${FIRST_NAME}" | head -c 1)
    #USERNAME=$(echo "${FIRST_LETTER}${LAST_NAME}" | sed 's/.*/\L&/')

    FIRST_NAME="${FULL_NAME% *}"
    LAST_NAME="${FULL_NAME#* }"
    USER_PASSWORD=$(slappasswd -s "${USERNAME}")

    if [ "${FULL_NAME}" = "" ]; then
        usage

        exit 1
    fi

    USER_NUMBER="${4}"
    LAST_USER_NUMBER_FILE="last_user_number.txt"

    if [ "${USER_NUMBER}" = "" ]; then
        if [ -f "${LAST_USER_NUMBER_FILE}" ]; then
            USER_NUMBER=$(cat "${LAST_USER_NUMBER_FILE}")
            USER_NUMBER=$(echo "${USER_NUMBER} + 1" | bc)
        else
            USER_NUMBER="2000"
        fi
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
shadowWarning: 0" | ${ADD_MANAGER_PASSWORD}
    echo "${USER_NUMBER}" > "${LAST_USER_NUMBER_FILE}"
elif [ "${VERB}" = "test" ]; then
    if [ "${USERNAME}" = "" ]; then
        usage

        exit 1
    fi

    FULL_NAME="${3}"
    USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"
    echo "Who am I?"
    ${WHO} -D "${USER_DN}"
    echo "Self search"
    ${SEARCH} -D "uid=${USERNAME},ou=users,${SUFFIX}" -b "uid=${USERNAME},ou=users,${SUFFIX}"
elif [ "${VERB}" = "set_password" ]; then
    if [ "${USERNAME}" = "" ]; then
        usage

        exit 1
    fi

    FULL_NAME="${3}"
    USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"
    echo "Enter new password:"
    read -r NEW_PASSWORD
    ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
    echo "dn: ${USER_DN}
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" | ${MODIFY_MANAGER_PASSWORD}
elif [ "${VERB}" = "change_password" ]; then
    if [ "${USERNAME}" = "" ]; then
        usage

        exit 1
    fi

    FULL_NAME="${3}"
    USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"
    echo "Enter new password:"
    read -r NEW_PASSWORD
    ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
    echo "Enter current password:"
    echo "dn: ${USER_DN}
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" | ${MODIFY} -D "uid=${USERNAME},ou=users,${SUFFIX}"
elif [ "${VERB}" = "delete" ]; then
    if [ "${USERNAME}" = "" ]; then
        usage

        exit 1
    fi

    FULL_NAME="${3}"
    USER_DN="uid=${USERNAME},ou=users,${SUFFIX}"
    ${DELETE_MANAGER_PASSWORD} "${USER_DN}"
    # TODO: Consider decreasing the user and group number if they are the most recent one.
elif [ "${VERB}" = "list" ]; then
    ${SEARCH_MANAGER_PASSWORD} -b "ou=users,${SUFFIX}" "(objectClass=inetOrgPerson)"
fi
