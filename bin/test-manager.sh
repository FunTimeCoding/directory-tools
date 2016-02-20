#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"

echo "Who am I?"
${WHO_MANAGER}
echo "Self search"
${SEARCH_MANAGER} -b "${MANAGER_DN}"
