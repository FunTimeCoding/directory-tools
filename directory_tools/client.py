from _ssl import PROTOCOL_TLSv1_2, CERT_REQUIRED
from os import path

from ldap3 import AUTO_BIND_TLS_BEFORE_BIND, AUTH_SIMPLE
from ldap3 import LDAPSSLConfigurationError
from ldap3 import LDAPSocketOpenError, LDAPBindError, LDAPStartTLSError
from ldap3 import Server, Connection, Tls


class Client:
    def __init__(
        self,
        server_name: str,
        manager_dn: str,
        manager_password: str,
        suffix: str,
    ):
        self._server_name = server_name
        self._manager_dn = manager_dn
        self._manager_password = manager_password
        self._suffix = suffix
        self._connection = None

    def _create_server(self) -> Server:
        base_path = path.dirname(path.realpath(__file__))
        ca_certificates_file = path.join(
            base_path, '..', 'ldap.shiin.org.node-certificate.crt'
        )
        print(ca_certificates_file)
        tls = None

        try:
            # TODO: Why is PROTOCOL_SSLv23 possible?
            tls = Tls(
                validate=CERT_REQUIRED,
                ca_certs_file=ca_certificates_file,
                version=PROTOCOL_TLSv1_2
            )
        except LDAPSSLConfigurationError as exception:
            print(str(exception))

            exit(4)

        return Server(
            host=self._server_name,
            port=389,
            get_info=False,
            tls=tls
        )

    def _create_connection(self) -> Connection:
        server = self._create_server()

        # PyCharm wants this to not complain on return.
        connection = None

        try:
            connection = Connection(
                server,
                auto_bind=AUTO_BIND_TLS_BEFORE_BIND,
                user=self._manager_dn,
                password=self._manager_password,
                authentication=AUTH_SIMPLE,
                version=3
            )
        except LDAPSocketOpenError as exception:
            print(str(exception))

            exit(1)
        except LDAPBindError as exception:
            print(str(exception))

            exit(2)
        except LDAPStartTLSError as exception:
            print(str(exception))

            exit(3)

        return connection

    def _lazy_get_connection(self) -> Connection:
        if self._connection is None:
            self._connection = self._create_connection()

        return self._connection

    def search(self, query: str, attributes: list) -> any:
        connection = self._lazy_get_connection()
        suffix = self._suffix
        result = connection.search(
            search_base=suffix,
            search_filter=query,
            attributes=attributes
        )

        if isinstance(result, bool):
            response = connection.response
            result = connection.result
        else:
            response, result = connection.get_response(result)

        # TODO: See about handling errors based on result.
        if result['result'] is not 0:
            print('Result was not 0.')

        return response

    def response_to_json(self, response) -> str:
        return self._connection.response_to_json(response)

    def search_user(self, query: str) -> any:
        attributes = [
            'cn',
            'uid',
            'displayName',
            'uidNumber',
            'gidNumber'
            'homeDirectory',
            'loginShell',
            'gecos',
            'mail'
        ]

        return self.search(query=query, attributes=attributes)
