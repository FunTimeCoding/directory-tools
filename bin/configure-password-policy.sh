#!/bin/sh -e

# TODO: This SHOULD work. It worked once before. Do not run twice.

DIRECTORY=$(dirname "${0}")
SCRIPT_DIRECTORY=$(
    cd "${DIRECTORY}" || exit 1
    pwd
)
# shellcheck source=/dev/null
. "${SCRIPT_DIRECTORY}/../lib/directory-tools.sh"

sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f src/load-ppolicy-module.ldif

dt unit add --name policies

sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/ppolicy.ldif

echo "dn: olcOverlay=ppolicy,olcDatabase={1}mdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcPPolicyConfig
olcOverlay: ppolicy
olcPPolicyDefault: cn=passwordDefault,ou=policies,${SUFFIX}
olcPPolicyHashCleartext: FALSE
olcPPolicyUseLockout: FALSE
olcPPolicyForwardUpdates: FALSE" >tmp/configure-ppolicy-module.ldif
sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f tmp/configure-ppolicy-module.ldif

echo "dn: cn=passwordDefault,ou=policies,${SUFFIX}
objectClass: pwdPolicy
objectClass: person
objectClass: top
cn: passwordDefault
sn: passwordDefault
pwdAttribute: userPassword
pwdCheckQuality: 0
pwdMinAge: 0
pwdMaxAge: 0
pwdMinLength: 14
pwdInHistory: 5
pwdMaxFailure: 3
pwdFailureCountInterval: 0
pwdLockout: TRUE
pwdLockoutDuration: 0
pwdAllowUserChange: TRUE
pwdExpireWarning: 0
pwdGraceAuthNLimit: 0
pwdMustChange: FALSE
pwdSafeModify: TRUE" >tmp/configure-ppolicy.ldif
ldapadd -W -D "${MANAGER_DN}" -f tmp/configure-ppolicy.ldif
