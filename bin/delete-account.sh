#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} USER_NAME"
    echo "Example: ${0} jdoe"
}

. "${SCRIPT_DIR}/../lib/directory_tools.sh"
USER_NAME="${1}"

if [ "${USER_NAME}" = "" ]; then
    usage

    exit 1
fi

${DELETE} "uid=${USER_NAME},ou=users,${SUFFIX}"
