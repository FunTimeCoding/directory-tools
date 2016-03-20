from os import path
from ssl import CERT_REQUIRED

from ldap3 import LDAPSocketOpenError
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

            raise exception

        return connection

    def _lazy_get_connection(self) -> Connection:
        if self._connection is None:
            self._connection = self._create_connection()

        return Connection

    def search(self, query: str, attributes: list) -> [any, object]:
        connection = self._lazy_get_connection()
        result = connection.search(
            search_base=self._suffix,
            search_filter=query,
            attributes=attributes
        )

        # TODO: Distinguish better between result and response.

        if isinstance(result, bool):
            response = connection.response
            result = connection.result
        else:
            response, result = connection.get_response(result)

        print('response type: ' + str(type(response)))
        print('result type: ' + str(type(result)))

        return response, result

    def search_user(self, query: str) -> [any, object]:
        attributes = [
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
