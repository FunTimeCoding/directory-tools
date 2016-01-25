#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)

usage()
{
    echo "Usage: ${0} DOMAIN"
    echo "Example: ${0} example.org"
}

. "${SCRIPT_DIR}/../lib/directory_tools.sh"
DOMAIN="${1}"

if [ "${DOMAIN}" = "" ]; then
    usage

    exit 1
fi

INTERCHANGE_FILE="/tmp/enable_security.ldif"
echo "dn: cn=config
changeType: modify
replace: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/${DOMAIN}.intermediate-certificate.pem
-
replace: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ssl/private/ldap.${DOMAIN}.node-private-key.pem
-
replace: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ssl/certs/ldap.${DOMAIN}.node-certificate.pem" > "${INTERCHANGE_FILE}"
${MODIFY} -f "${INTERCHANGE_FILE}"
rm "${INTERCHANGE_FILE}"
