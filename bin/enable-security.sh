#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)

usage() {
    echo "Usage: ${0} DOMAIN"
    echo "Example: ${0} example.org"
}

# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"
DOMAIN="${1}"

if [ "${DOMAIN}" = '' ]; then
    usage

    exit 1
fi

echo "dn: cn=config
changeType: modify
replace: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/${DOMAIN}.intermediate-certificate.pem
-
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/ldap.${DOMAIN}.node-private-key.pem
-
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/ldap.${DOMAIN}.node-certificate.pem" | ${MODIFY_SOCKET}

echo "dn: cn=config
changeType: modify
add: olcDisallows
olcDisallows: bind_anon" | ${MODIFY_SOCKET}

echo "dn: olcDatabase={1}mdb,cn=config
changeType: modify
add: olcRequires
olcRequires: authc" | ${MODIFY_SOCKET}
