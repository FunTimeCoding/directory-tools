#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)

usage() {
    echo "Usage: ${0} DISTINGUISHED_NAME
Example: ${0} uid=john,ou=users,dc=example,dc=org"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
DISTINGUISHED_NAME="${1}"

if [ "${DISTINGUISHED_NAME}" = '' ]; then
    usage

    exit 1
fi

echo "dn: ${DISTINGUISHED_NAME}
delete: pwdAccountLockedTime" >tmp/unlock.diff
ldapmodify -W -D "${MANAGER_DN}" -f tmp/unlock.ldif
