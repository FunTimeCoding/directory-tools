#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
echo "dn: ${SUFFIX}
objectClass: dcObject
objectclass: organization
o: ${ORGANIZATION}
dc: ${DOMAIN}
description: ${ORGANIZATION} Organization" | ${ADD_MANAGER}
