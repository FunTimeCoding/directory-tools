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
        --config)
            CONFIG=${2-}
            shift 2
            ;;
        --help)
            echo "Global usage: ${0} [--verbose][--debug][--help][--config CONFIG]"

            if function_exists usage; then
                usage
            fi

            exit 0
            ;;
        --verbose)
            VERBOSE=true
            echo "Verbose mode enabled."
            shift
            ;;
        --debug)
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
    REALPATH="realpath"
else
    REALPATH_EXISTS=$(command -v grealpath 2>&1)

    if [ ! "${REALPATH_EXISTS}" = "" ]; then
        REALPATH="grealpath"
    else
        echo "Required tool (g)realpath not found."

        exit 1
    fi
fi

if [ -f "${CONFIG}" ]; then
    CONFIG=$(${REALPATH} "${CONFIG}")
else
    CONFIG=""
fi

if [ "${VERBOSE}" = true ]; then
    echo "load_config"
fi

if [ ! "${CONFIG}" = "" ]; then
    MANAGER_PASSWORD=$(shyaml get-value "manager-password" < "${CONFIG}" 2>/dev/null || true)
    export MANAGER_PASSWORD
    ENCRYPTED_MANAGER_PASSWORD=$(slappasswd -s "${MANAGER_PASSWORD}")
    export ENCRYPTED_MANAGER_PASSWORD
    DOMAIN=$(shyaml get-value "domain" < "${CONFIG}" 2>/dev/null || true)
    export DOMAIN
    TOP_LEVEL=$(shyaml get-value "top_level" < "${CONFIG}" 2>/dev/null || true)
    export TOP_LEVEL
fi

if [ "${VERBOSE}" = true ]; then
    echo "define_library_variables"
fi

SEARCH="sudo ldapsearch -o ldif-wrap=no -Q -Y EXTERNAL -H ldapi:/// -LLL"
export SEARCH
CAT="sudo slapcat -o ldif-wrap=no -F /etc/ldap/slapd.d"
export CAT
ADD="sudo ldapadd -Y EXTERNAL -H ldapi:///"
export ADD
DELETE="sudo ldapdelete -Y EXTERNAL -H ldapi:///"
export DELETE
MODIFY="sudo ldapmodify -Y EXTERNAL -H ldapi:///"
export MODIFY
SUFFIX="dc=${DOMAIN},dc=${TOP_LEVEL}"
export SUFFIX
DOMAIN_UPPER_CASE=$(echo "${DOMAIN}" | sed 's/.*/\u&/')
export DOMAIN_UPPER_CASE
ORGANIZATION="${DOMAIN_UPPER_CASE} Organization"
export ORGANIZATION
