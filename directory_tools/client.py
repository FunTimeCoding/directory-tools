from os import path
from ssl import CERT_REQUIRED

from ldap3 import LDAPSocketOpenError, LDAPBindError
from ldap3 import Server, Connection, Tls, AUTH_SIMPLE, STRATEGY_SYNC


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
        certificate_path = path.join(
            base_path, '..', 'ldap.shiin.org.node-certificate.crt'
        )

        tls = Tls(
            validate=CERT_REQUIRED,
            ca_certs_file=certificate_path
        )

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
                auto_bind=True,
                version=3,
                client_strategy=STRATEGY_SYNC,
                user=self._manager_dn,
                password=self._manager_password,
                authentication=AUTH_SIMPLE,
                lazy=False,
                check_names=False
            )
        except LDAPSocketOpenError as exception:
            print(str(exception))

            exit(1)
        except LDAPBindError as exception:
            print(str(exception))

            exit(2)

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
