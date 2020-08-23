#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)

usage() {
    echo "Usage: ${0} DISTINGUISHED_NAME EMAIL
Example: ${0} uid=john,ou=users,dc=example,dc=org john@example.org"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../../lib/directory-tools.sh"
DISTINGUISHED_NAME="${1}"
EMAIL="${1}"

if [ "${DISTINGUISHED_NAME}" = '' ] || [ "${EMAIL}" = '' ]; then
    usage

    exit 1
fi

echo "dn: ${DISTINGUISHED_NAME}
changetype: modify
replace: mail
mail: ${EMAIL}" >tmp/email.diff
ldapmodify -W -D "${MANAGER_DN}" -f tmp/email.ldif
