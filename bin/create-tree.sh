#!/bin/sh -e

DIR=$(dirname "${0}")
SCRIPT_DIR=$(cd "${DIR}" || exit 1; pwd)
. "${SCRIPT_DIR}/../lib/directory_tools.sh"
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
olcSuffix: dc=${DOMAIN},dc=${TOP_LEVEL}
olcRootDN: cn=admin,dc=${DOMAIN},dc=${TOP_LEVEL}
olcRootPW: ${PASSWORD}
olcDbIndex: objectClass eq" > "${INTERCHANGE_FILE}"
    ${ADD} -f "${INTERCHANGE_FILE}"
    rm "${INTERCHANGE_FILE}"
fi
