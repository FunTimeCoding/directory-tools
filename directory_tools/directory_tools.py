from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC
from python_utility.yaml_config import YamlConfig


class DirectoryTools:
    def __init__(self, arguments: list):
        config = YamlConfig(path='~/.directory-tools.yml')
        host = config.get('host')
        domain = config.get('domain')
        top_level = config.get('top_level')
        self.manager_password = config.get('manager-password')
        self.suffix = 'dc='+domain+',dc='+top_level
        manager_name = config.get('manager-name')
        manager_relative_dn = 'cn='+manager_name
        self.manager_dn = manager_relative_dn+','+self.suffix
        self.server_name = host+'.'+domain+'.'+top_level

    def run(self):
        server = Server(
            host=self.server_name,
            port=389,
            get_info=False
        )

        connection = Connection(
            server,
            auto_bind=True,
            version=3,
            client_strategy=STRATEGY_SYNC,
            user=self.manager_dn,
            password=self.manager_password,
            authentication=AUTH_SIMPLE,
            lazy=False,
            check_names=False
        )

        result = connection.search(
            search_base=self.suffix,
            search_filter='(cn=admin)',
            attributes=['cn', 'description']
        )

        if not isinstance(result, bool):
            response, result = connection.get_response(result)
        else:
            response = connection.response
            result = connection.result

        print(result)
        print(response)

        return 0
