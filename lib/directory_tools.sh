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

SUFFIX="dc=${DOMAIN},dc=${TOP_LEVEL}"
export SUFFIX
DOMAIN_UPPER_CASE=$(echo "${DOMAIN}" | sed 's/.*/\u&/')
export DOMAIN_UPPER_CASE
ORGANIZATION="${DOMAIN_UPPER_CASE} Organization"
export ORGANIZATION

# Use slapcat if you want to confirm what ldapsearch is true.
CAT="sudo slapcat -o ldif-wrap=no -F /etc/ldap/slapd.d"
export CAT

# Used arguments.
# -H ldap://ldap.shiin.org - Connect via TCP.
# -LLL - Reduce LDAP protocol output.
# -D - BindDN needed when authenticating.
# -W - Enter password interactively when authenticating.

# Arguments to avoid:
# -H ldapi:/// - Connect via socket file.
# -x - Use simple authentication. This is not what I want.
# -w - Pass password as argument when authenticating.

# Arguments to examine:
# -Y EXTERNAL - Use SASL mechanism EXTERNAL instead of specifying -D and -W.

# Confirm locally that the manager exists and can log in.
#ldapwhoami -D cn=admin,dc=shiin,dc=org -W
# Confirm remotely that the manager exists and can log in.
#ldapwhoami -H ldap://ldap.shiin.org -D 'cn=admin,dc=shiin,dc=org' -W

SEARCH="ldapsearch -o ldif-wrap=no -LLL -H ldap://ldap.shiin.org -D cn=admin,${SUFFIX} -W"
export SEARCH
ADD="ldapadd -H ldap://ldap.shiin.org -D cn=admin,${SUFFIX} -W"
export ADD
DELETE="ldapdelete -H ldap://ldap.shiin.org -D cn=admin,${SUFFIX} -W"
export DELETE
MODIFY="ldapmodify -H ldap://ldap.shiin.org -D cn=admin,${SUFFIX} -W"
export MODIFY
