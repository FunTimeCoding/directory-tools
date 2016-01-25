#!/bin/sh -e

if [ "$(command -v shyaml || true)" = "" ]; then
    echo "Command not found: shyaml"

    exit 1
fi

CONFIG=""
VERBOSE=false

function_exists()
{
    declare -f -F "${1}" > /dev/null

    return $?
}

while true; do
    case ${1} in
        -c|--config)
            CONFIG=${2-}
            shift 2
            ;;
        -h|--help)
            echo "Global usage: ${0} [-v|--verbose][-d|--debug][-h|--help][-c|--config CONFIG]"

            if function_exists usage; then
                usage
            fi

            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            echo "Verbose mode enabled."
            shift
            ;;
        -d|--debug)
            set -x
            shift
            ;;
        *)
            break
            ;;
    esac
done

OPTIND=1

if [ "${VERBOSE}" = true ]; then
    echo "find_config"
fi

if [ "${CONFIG}" = "" ]; then
    CONFIG="${HOME}/.directory-tools.yml"
fi

REALPATH_EXISTS=$(command -v realpath 2>&1)

if [ ! "${REALPATH_EXISTS}" = "" ]; then
    REALPATH_CMD="realpath"
else
    REALPATH_EXISTS=$(command -v grealpath 2>&1)

    if [ ! "${REALPATH_EXISTS}" = "" ]; then
        REALPATH_CMD="grealpath"
    else
        echo "Required tool (g)realpath not found."

        exit 1
    fi
fi

if [ -f "${CONFIG}" ]; then
    CONFIG=$(${REALPATH_CMD} "${CONFIG}")
else
    CONFIG=""
fi

if [ "${VERBOSE}" = true ]; then
    echo "load_config"
fi

if [ ! "${CONFIG}" = "" ]; then
    export PLAIN_PASSWORD=$(shyaml get-value "password" < "${CONFIG}" 2>/dev/null || true)
    export PASSWORD=$(slappasswd -s "${PLAIN_PASSWORD}")
    export DOMAIN=$(shyaml get-value "domain" < "${CONFIG}" 2>/dev/null || true)
    export TOP_LEVEL=$(shyaml get-value "top_level" < "${CONFIG}" 2>/dev/null || true)
fi

if [ "${VERBOSE}" = true ]; then
    echo "define_library_variables"
fi

export ADD="sudo ldapadd -Y EXTERNAL -H ldapi:///"
export DELETE="sudo ldapdelete -Y EXTERNAL -H ldapi:///"
export MODIFY="sudo ldapmodify -Y EXTERNAL -H ldapi:///"
export SUFFIX="dc=${DOMAIN},dc=${TOP_LEVEL}"
export DOMAIN_UPPER_CASE=$(echo ${DOMAIN} | sed 's/.*/\u&/')
export ORGANIZATION="${DOMAIN_UPPER_CASE} Organization"
