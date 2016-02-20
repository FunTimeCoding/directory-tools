#!/bin/sh -e

if [ "$(command -v shyaml || true)" = "" ]; then
    echo "Command not found: shyaml"

    exit 1
fi

function_exists()
{
    declare -f -F "${1}" > /dev/null

    return $?
}

while true; do
    case ${1} in
        --help)
            echo "Global usage: ${0} [--help][--config CONFIG][--debug]"

            if function_exists usage; then
                usage
            fi

            exit 0
            ;;
        --config)
            CONFIG=${2-}
            shift 2
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

if [ "${CONFIG}" = "" ]; then
    CONFIG="${HOME}/.directory-tools.yml"
fi

if [ "$(command -v realpath || true)" = "" ]; then
    if [ "$(command -v grealpath || true)" = "" ]; then
        echo "Command not found: realpath"

        exit 1
    else
        REALPATH="grealpath"
    fi
else
    REALPATH="realpath"
fi

if [ -f "${CONFIG}" ]; then
    CONFIG=$(${REALPATH} "${CONFIG}")
    DOMAIN=$(shyaml get-value "domain" < "${CONFIG}" 2>/dev/null || true)
    export DOMAIN
    TOP_LEVEL=$(shyaml get-value "top_level" < "${CONFIG}" 2>/dev/null || true)
    export TOP_LEVEL
    MANAGER_PASSWORD=$(shyaml get-value "manager-password" < "${CONFIG}" 2>/dev/null || true)
    export MANAGER_PASSWORD

    if [ ! "$(command -v slappasswd || true)" = "" ]; then
        ENCRYPTED_MANAGER_PASSWORD=$(slappasswd -s "${MANAGER_PASSWORD}")
        export ENCRYPTED_MANAGER_PASSWORD
    fi
else
    CONFIG=""
fi

# -Q - Disable SASL output.
# -Y EXTERNAL - Use SASL mechanism EXTERNAL instead of specifying -D and -W.
# -H 'ldapi:///' - LDAP URI to connect to.
# -LLL - Reduce LDAP protocol output.
# -D - BindDN needed when authenticating.
# -W - Enter password interactively when authenticating.
# -w - Pass password as argument when authenticating.
SEARCH="sudo ldapsearch -o ldif-wrap=no -Q -Y EXTERNAL -H ldapi:/// -LLL"
export SEARCH
# Use slapcat if you want to confirm what ldapsearch is true.
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
