#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/project.sh"
id -u vagrant 2> /dev/null && VAGRANT_ENVIRONMENT='true' || VAGRANT_ENVIRONMENT='false'

if [ "${VAGRANT_ENVIRONMENT}" = true ]; then
    VIRTUAL_ENVIRONMENT_PATH='/home/vagrant/venv'
else
    VIRTUAL_ENVIRONMENT_PATH='.venv'
fi

if [ "${SYSTEM}" = Darwin ]; then
    SED='gsed'
else
    SED='sed'
fi

UNDERSCORE=$(echo "${PROJECT_NAME}" | ${SED} --regexp-extended 's/-/_/g')
# shellcheck source=/dev/null
. "${VIRTUAL_ENVIRONMENT_PATH}/bin/activate"
PORT=$(cat "${HOME}/.${PROJECT_NAME}.yaml" | shyaml get-value port)
waitress-serve --port "${PORT}" --call "${UNDERSCORE}.application:create_app"
