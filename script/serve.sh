#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../configuration/project.sh"

if [ "${SYSTEM}" = Darwin ]; then
    SED='gsed'
else
    SED='sed'
fi

# shellcheck source=/dev/null
. "${HOME}/venv/bin/activate"
PORT=$(shyaml get-value port <"${HOME}/.${PROJECT_NAME_DASH}.yaml")
waitress-serve --port "${PORT}" --call "${PROJECT_NAME_UNDERSCORE}.application:create_app"
