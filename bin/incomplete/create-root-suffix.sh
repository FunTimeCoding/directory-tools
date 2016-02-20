#!/bin/sh -e

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(cd "${DIRECTORY}" || exit 1; pwd)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory_tools.sh"
DATABASE_DIRECTORY="/var/lib/ldap/${DOMAIN}.${TOP_LEVEL}"

if [ -f "${DATABASE_DIRECTORY}" ]; then
    echo "Tree already exists."
else
    sudo mkdir -p "${DATABASE_DIRECTORY}"
    sudo chown openldap:openldap "${DATABASE_DIRECTORY}"
    echo "dn: olcDatabase=mdb,cn=config
objectClass: olcDatabaseConfig
objectClass: olcMdbConfig
olcDatabase: mdb
olcDbDirectory: ${DATABASE_DIRECTORY}
olcSuffix: ${SUFFIX}
olcRootDN: ${MANAGER_DN}
olcRootPW: ${PASSWORD}
olcDbIndex: objectClass eq" | ${ADD_SOCKET}
fi

# TODO: Find out the exact index of the olcDatabase that was just created.
INDEX="2"

echo "dn: olcDatabase={${INDEX}}mdb,cn=config
changeType: modify
add: olcDbIndex
olcDbIndex: uid eq" | ${MODIFY_SOCKET}

echo "dn: ${SUFFIX}
objectClass: dcObject
objectclass: organization
o: ${ORGANIZATION}
dc: ${DOMAIN}
description: ${ORGANIZATION} Organization" | ${ADD_MANAGER}

echo "dn: olcDatabase={${INDEX}}mdb,cn=config
changeType: modify
add: olcAccess
olcAccess: to attrs=userPassword,shadowLastChange by self write by anonymous auth by * none
add: olcAccess
olcAccess: to dn.base=\"\" by * read
add: olcAccess
olcAccess: to * by * read" | ${MODIFY_SOCKET}
