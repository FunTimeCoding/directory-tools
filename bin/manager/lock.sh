#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)

usage() {
    echo "Usage: ${0} DISTINGUISHED_NAME LOCK_TIME
Example: ${0} uid=john,ou=users,dc=example,dc=org 20200101143000Z"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
DISTINGUISHED_NAME="${1}"
LOCK_TIME="${1}"

if [ "${DISTINGUISHED_NAME}" = '' ] || [ "${LOCK_TIME}" = '' ]; then
    usage

    exit 1
fi

echo "dn: ${DISTINGUISHED_NAME}
add: pwdAccountLockedTime
pwdAccountLockedTime: ${LOCK_TIME}" >tmp/lock.diff
ldapmodify -W -D "${MANAGER_DN}" -f tmp/lock.ldif
