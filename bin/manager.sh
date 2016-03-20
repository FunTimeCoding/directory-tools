#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} test|new_password"
    echo "Example: ${0} examplePassword"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
VERB="${1}"

if [ "${VERB}" = "test" ]; then
    echo "Who am I?"
    ${WHO_MANAGER}
    echo
    echo "Self search"
    ${SEARCH_MANAGER} -b "${MANAGER_DN}" | grep -v '^$'
    echo
    echo "Password hash"
    #${SEARCH_SOCKET} -b 'cn=config' 'olcDatabase=mdb' 'olcRootPW' | grep -v '^$'
    ${SEARCH_SOCKET} -b 'cn=config' 'olcDatabase=mdb'
elif [ "${VERB}" = "new_password" ]; then
    echo "Enter new password:"
    read -r NEW_PASSWORD
    ENCRYPTED_PASSWORD=$(slappasswd -s "${NEW_PASSWORD}")
    echo "dn: olcDatabase={1}mdb,cn=config
replace: olcRootPW
olcRootPW: ${ENCRYPTED_PASSWORD}" | ${MODIFY_SOCKET}
    echo "dn: cn=admin,${SUFFIX}
changeType: modify
replace: userPassword
userPassword: ${ENCRYPTED_PASSWORD}" | ${MODIFY_SOCKET}
else
    usage

    exit 1
fi
