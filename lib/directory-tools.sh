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
            echo "Global usage: ${0} [--help][--config CONFIG]"

            if function_exists usage; then
                usage
            fi

            exit 0
            ;;
        --config)
            CONFIG=${2-}
            shift 2
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

SUFFIX="dc=${DOMAIN},dc=${TOP_LEVEL}"
export SUFFIX
DOMAIN_UPPER_CASE=$(echo "${DOMAIN}" | sed 's/.*/\u&/')
export DOMAIN_UPPER_CASE
ORGANIZATION="${DOMAIN_UPPER_CASE} Organization"
export ORGANIZATION

# Use slapcat if you want to confirm what ldapsearch is true.
CAT="sudo slapcat -F /etc/ldap/slapd.d -o ldif-wrap=no"
export CAT

# -Q - Reduce SASL output.
# -LLL - Reduce LDAP output.

# For network connections.
# -H ldap://ldap.example.org - Connect via TCP.
# -D - BindDN needed when authenticating.
# -W - Enter password interactively.

# For socket file connections.
# -H ldapi:/// - Connect via socket file.
# -Y EXTERNAL - Use SASL mechanism EXTERNAL, as opposed to specifying -D and -W.

# Avoid using these.
# -x - Use simple authentication.
# -w - Pass password as argument when authenticating.

HOST_NAME="ldap.greenshininglake.org"
HOST_PARAMETER="ldap://${HOST_NAME}"

# Basic reusable commands.
WHO="ldapwhoami -H ${HOST_PARAMETER} -W"
export WHO
SEARCH="ldapsearch -H ${HOST_PARAMETER} -W -LLL -o ldif-wrap=no"
export SEARCH
ADD="ldapadd -H ${HOST_PARAMETER} -W"
export ADD
MODIFY="ldapmodify -H ${HOST_PARAMETER} -W"
export MODIFY
DELETE="ldapdelete -H ${HOST_PARAMETER} -W"
export DELETE

MANAGER_DN="cn=admin,${SUFFIX}"

# Convenience commands for manager access.
WHO_MANAGER="${WHO} -D ${MANAGER_DN}"
export WHO_MANAGER
SEARCH_MANAGER="${SEARCH} -D ${MANAGER_DN}"
export SEARCH_MANAGER
ADD_MANAGER="${ADD} -D ${MANAGER_DN}"
export ADD_MANAGER
MODIFY_MANAGER="${MODIFY} -D ${MANAGER_DN}"
export MODIFY_MANAGER
DELETE_MANAGER="${DELETE} -D ${MANAGER_DN}"
export DELETE_MANAGER

SEARCH_PASSWORD="ldapsearch -H ${HOST_PARAMETER}"
export SEARCH_PASSWORD
ADD_PASSWORD="ldapadd -H ${HOST_PARAMETER}"
export ADD_PASSWORD
MODIFY_PASSWORD="ldapmodify -H ${HOST_PARAMETER}"
export MODIFY_PASSWORD
DELETE_PASSWORD="ldapdelete -H ${HOST_PARAMETER}"
export DELETE_PASSWORD

SEARCH_MANAGER_PASSWORD="${SEARCH_PASSWORD} -LLL -D ${MANAGER_DN} -w ${MANAGER_PASSWORD}"
export SEARCH_MANAGER_PASSWORD
ADD_MANAGER_PASSWORD="${ADD_PASSWORD} -D ${MANAGER_DN} -w ${MANAGER_PASSWORD}"
export ADD_MANAGER_PASSWORD
MODIFY_MANAGER_PASSWORD="${MODIFY_PASSWORD} -D ${MANAGER_DN} -w ${MANAGER_PASSWORD}"
export MODIFY_MANAGER_PASSWORD
DELETE_MANAGER_PASSWORD="${DELETE_PASSWORD} -D ${MANAGER_DN} -w ${MANAGER_PASSWORD}"
export DELETE_MANAGER_PASSWORD

# Access to cn=config requires socket access, so these must be run as root.
WHO_SOCKET="sudo ldapwhoami -H ldapi:/// -Y EXTERNAL -Q"
export WHO_SOCKET
SEARCH_SOCKET="sudo ldapsearch -H ldapi:/// -Y EXTERNAL -Q -LLL -o ldif-wrap=no"
export SEARCH_SOCKET
ADD_SOCKET="sudo ldapadd -H ldapi:/// -Y EXTERNAL -Q"
export ADD_SOCKET
MODIFY_SOCKET="sudo ldapmodify -H ldapi:/// -Y EXTERNAL -Q"
export MODIFY_SOCKET
DELETE_SOCKET="sudo ldapdelete -H ldapi:/// -Y EXTERNAL -Q"
export DELETE_SOCKET
