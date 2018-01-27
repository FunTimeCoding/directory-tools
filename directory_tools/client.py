from _ssl import PROTOCOL_TLSv1_2, CERT_REQUIRED
from os.path import dirname, realpath, join

from ldap3 import AUTO_BIND_TLS_BEFORE_BIND, SIMPLE
from ldap3 import Server, Connection, Tls
from ldap3.core.exceptions import LDAPSSLConfigurationError, LDAPStartTLSError
from ldap3.core.exceptions import LDAPSocketOpenError, LDAPBindError
from ldap3.core.exceptions import LDAPInvalidFilterError


class Client:
    def __init__(
            self,
            server_name: str,
            manager_distinguished_name: str,
            manager_password: str,
            suffix: str,
            secure: bool = False,
    ) -> None:
        self.server_name = server_name
        self.manager_distinguished_name = manager_distinguished_name
        self.manager_password = manager_password
        self.suffix = suffix
        self.secure = secure
        self.connection = None

    def create_server(self) -> Server:
        # PyCharm wants this here to not complain about the return statement.
        transport_layer_security = None

        if self.secure:
            certificate_chain = join(
                dirname(realpath(__file__)),
                'certificate_chain.pem',
            )

            try:
                transport_layer_security = Tls(
                    validate=CERT_REQUIRED,
                    ca_certs_file=certificate_chain,
                    version=PROTOCOL_TLSv1_2,
                )
            except LDAPSSLConfigurationError as exception:
                print('LDAPSSLConfigurationError: ' + str(exception))
                print('certificate_chain: ' + certificate_chain)
                print('server_name: ' + self.server_name)

                exit(4)

        return Server(
            host=self.server_name,
            port=389,
            # TODO: Why no get_info?
            get_info=False,
            tls=transport_layer_security,
        )

    def create_connection(self) -> Connection:
        server = self.create_server()
        # PyCharm wants this to not complain about the return statement.
        connection = None

        try:
            # TODO: auto_bind is somehow important. Document why.
            if self.secure:
                auto_bind = AUTO_BIND_TLS_BEFORE_BIND
            else:
                auto_bind = True

            connection = Connection(
                server,
                auto_bind=auto_bind,
                user=self.manager_distinguished_name,
                password=self.manager_password,
                authentication=SIMPLE,
                version=3
            )
        except LDAPSocketOpenError as exception:
            print('LDAPSocketOpenError: ' + str(exception))

            exit(1)
        except LDAPBindError as exception:
            print('LDAPBindError: ' + str(exception))

            exit(2)
        except LDAPStartTLSError as exception:
            print('LDAPStartTLSError: ' + str(exception))
            print('TLS settings: ' + str(server.tls))

            exit(3)

        return connection

    def lazy_get_connection(self) -> Connection:
        if self.connection is None:
            self.connection = self.create_connection()

        return self.connection

    def search(self, query: str, attributes=None) -> any:

        if attributes is None:
            attributes = []

        connection = self.lazy_get_connection()
        # Need to assign this to make the static analysis happy.
        result = None

        try:
            result = connection.search(
                search_base=self.suffix,
                search_filter=query,
                attributes=attributes,
            )
        except LDAPInvalidFilterError as exception:
            print('LDAPInvalidFilterError: ' + str(exception) + ': ' + query)

            exit(5)

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
        return self.connection.response_to_json(response)

    def search_user(self, query: str) -> any:
        return self.search(
            query=query,
            attributes=[
                'cn',
                'uid',
                'displayName',
                'uidNumber',
                'gidNumber'
                'homeDirectory',
                'loginShell',
                'gecos',
                'mail',
            ],
        )
