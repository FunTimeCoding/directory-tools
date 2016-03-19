from argparse import ArgumentDefaultsHelpFormatter

from python_utility.custom_argument_parser import CustomArgumentParser


class Parser:
    def __init__(self, arguments: list):
        self._parser = self._create_parser()
        self.parsed_arguments = self._parser.parse_args(arguments)
        print(self.parsed_arguments)

    def print_help(self):
        self._parser.print_help()

    @staticmethod
    def _create_parser() -> CustomArgumentParser:
        parser = CustomArgumentParser(
            description='directory administration tool',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        subparsers = parser.add_subparsers()
        Parser._add_user_child_parser(subparsers)
        Parser._add_status_child_parser(subparsers)

        return parser

    @staticmethod
    def _add_user_child_parser(subparsers) -> None:
        user_parent = CustomArgumentParser(add_help=False)
        user_parser = subparsers.add_parser(
            'user',
            parents=[user_parent],
            help='manage users'
        )
        user_parser.add_argument('user', action='store_true')
        user_subparsers = user_parser.add_subparsers()

        add_parent = CustomArgumentParser(add_help=False)
        add_parent.add_argument('--user-name')
        add_parent.add_argument('--full-name', required=True)
        add_parent.add_argument('--password', required=True)
        add_parent.add_argument('--mail', required=True)
        add_parent.add_argument(
            '--groups',
            nargs='+',
            metavar='GROUP',
        )
        add_parser = user_subparsers.add_parser(
            'add',
            parents=[add_parent],
            help='add a user'
        )
        add_parser.add_argument('add', action='store_true')

        delete_parent = CustomArgumentParser(add_help=False)
        delete_parent.add_argument('--user-name', required=True)
        delete_parent.add_argument('--full-name', required=True)
        delete_parser = user_subparsers.add_parser(
            'delete',
            parents=[delete_parent],
            help='delete a user'
        )
        delete_parser.add_argument('delete', action='store_true')

        search_parent = CustomArgumentParser(add_help=False)
        search_group = search_parent.add_mutually_exclusive_group(required=True)
        search_group.add_argument('--user-name')
        search_group.add_argument('--full-name')
        search_parser = user_subparsers.add_parser(
            'search',
            parents=[search_parent],
            help='search for users'
        )
        search_parser.add_argument('search', action='store_true')

        list_parser = user_subparsers.add_parser('list', help='list all users')
        list_parser.add_argument('list', action='store_true')

    @staticmethod
    def _add_status_child_parser(subparsers) -> None:
        status_parent = CustomArgumentParser(add_help=False)
        status_parser = subparsers.add_parser(
            'status',
            parents=[status_parent],
            help='show status information'
        )
        status_parser.add_argument('status', action='store_true')
