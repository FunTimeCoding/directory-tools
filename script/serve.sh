#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/project.sh"

if [ "${SYSTEM}" = Darwin ]; then
    SED='gsed'
else
    SED='sed'
fi

UNDERSCORE=$(echo "${PROJECT_NAME}" | ${SED} --regexp-extended 's/-/_/g')
# shellcheck source=/dev/null
. "${HOME}/venv/bin/activate"
PORT=$(shyaml get-value port < "${HOME}/.${PROJECT_NAME}.yaml")
waitress-serve --port "${PORT}" --call "${UNDERSCORE}.application:create_app"
