#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
DATABASE_DIRECTORY="/var/lib/ldap/${DOMAIN}.${TOP_LEVEL}"

if [ -f "${DATABASE_DIRECTORY}" ]; then
    echo "Tree already exists."
else
    sudo mkdir -p "${DATABASE_DIRECTORY}"
    sudo chown openldap:openldap "${DATABASE_DIRECTORY}"
    INTERCHANGE_FILE="/tmp/create_tree.ldif"
    echo "dn: olcDatabase=mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
olcDbDirectory: ${DATABASE_DIRECTORY}
olcSuffix: ${SUFFIX}
olcRootDN: cn=admin,${SUFFIX}
olcRootPW: ${PASSWORD}
olcDbIndex: objectClass eq" > "${INTERCHANGE_FILE}"
    ${ADD} -f "${INTERCHANGE_FILE}"
    rm "${INTERCHANGE_FILE}"
fi
