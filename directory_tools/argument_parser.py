from argparse import ArgumentDefaultsHelpFormatter

from python_utility.custom_argument_parser import CustomArgumentParser


class Parser:
    def __init__(self, arguments: list) -> None:
        self.parser = CustomArgumentParser(
            description='directory administration tool',
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        subparsers = self.parser.add_subparsers()
        self.add_user_child_parser(subparsers)
        self.add_group_child_parser(subparsers)
        self.add_unit_child_parser(subparsers)
        self.add_status_child_parser(subparsers)
        self.add_authenticate_child_parser(subparsers)
        self.parsed_arguments = self.parser.parse_args(arguments)

    def print_help(self) -> None:
        self.parser.print_help()

    @staticmethod
    def add_user_child_parser(subparsers) -> None:
        user_parent = CustomArgumentParser(add_help=False)
        user_parser = subparsers.add_parser(
            'user',
            parents=[user_parent],
            help='manage users'
        )
        user_parser.add_argument('user', action='store_true')
        user_subparsers = user_parser.add_subparsers()

        add_parent = CustomArgumentParser(add_help=False)
        add_parent.add_argument('--name', required=True)
        add_parent.add_argument('--first-name', required=True)
        add_parent.add_argument('--last-name', required=True)
        add_parent.add_argument('--password', required=True)
        add_parent.add_argument('--email', required=True)
        add_parser = user_subparsers.add_parser(
            'add',
            parents=[add_parent],
            help='add a user'
        )
        add_parser.add_argument('add', action='store_true')

        remove_parent = CustomArgumentParser(add_help=False)
        remove_parent.add_argument('--name', required=True)
        remove_parser = user_subparsers.add_parser(
            'remove',
            parents=[remove_parent],
            help='remove a user'
        )
        remove_parser.add_argument('remove', action='store_true')

        show_parent = CustomArgumentParser(add_help=False)
        show_parent.add_argument('--name', required=True)
        show_parser = user_subparsers.add_parser(
            'show',
            parents=[show_parent],
            help='show a user'
        )
        show_parser.add_argument('show', action='store_true')

        list_parser = user_subparsers.add_parser('list', help='list all users')
        list_parser.add_argument('list', action='store_true')

    @staticmethod
    def add_group_child_parser(subparsers) -> None:
        group_parent = CustomArgumentParser(add_help=False)
        group_parser = subparsers.add_parser(
            'group',
            parents=[group_parent],
            help='manage groups'
        )
        group_parser.add_argument('group', action='store_true')
        group_subparsers = group_parser.add_subparsers()

        add_parent = CustomArgumentParser(add_help=False)
        add_parent.add_argument('--name', required=True)
        add_parser = group_subparsers.add_parser(
            'add',
            parents=[add_parent],
            help='add a group'
        )
        add_parser.add_argument('add', action='store_true')

        remove_parent = CustomArgumentParser(add_help=False)
        remove_parent.add_argument('--name', required=True)
        remove_parser = group_subparsers.add_parser(
            'remove',
            parents=[remove_parent],
            help='remove a group'
        )
        remove_parser.add_argument('remove', action='store_true')

        show_parent = CustomArgumentParser(add_help=False)
        show_parent.add_argument('--name', required=True)
        show_parser = group_subparsers.add_parser(
            'show',
            parents=[show_parent],
            help='show a group'
        )
        show_parser.add_argument('show', action='store_true')

        list_parser = group_subparsers.add_parser(
            'list',
            help='list all groups'
        )
        list_parser.add_argument('list', action='store_true')

    @staticmethod
    def add_unit_child_parser(subparsers) -> None:
        unit_parent = CustomArgumentParser(add_help=False)
        unit_parser = subparsers.add_parser(
            'unit',
            parents=[unit_parent],
            help='manage units'
        )
        unit_parser.add_argument('unit', action='store_true')
        unit_subparsers = unit_parser.add_subparsers()

        add_parent = CustomArgumentParser(add_help=False)
        add_parent.add_argument('--name', required=True)
        add_parser = unit_subparsers.add_parser(
            'add',
            parents=[add_parent],
            help='add a unit'
        )
        add_parser.add_argument('add', action='store_true')

        remove_parent = CustomArgumentParser(add_help=False)
        remove_parent.add_argument('--name', required=True)
        remove_parser = unit_subparsers.add_parser(
            'remove',
            parents=[remove_parent],
            help='remove a unit'
        )
        remove_parser.add_argument('remove', action='store_true')

        show_parent = CustomArgumentParser(add_help=False)
        show_parent.add_argument('--name', required=True)
        show_parser = unit_subparsers.add_parser(
            'show',
            parents=[show_parent],
            help='show a unit'
        )
        show_parser.add_argument('show', action='store_true')

        list_parser = unit_subparsers.add_parser(
            'list',
            help='list all units'
        )
        list_parser.add_argument('list', action='store_true')

    @staticmethod
    def add_status_child_parser(subparsers) -> None:
        status_parent = CustomArgumentParser(add_help=False)
        status_parser = subparsers.add_parser(
            'status',
            parents=[status_parent],
            help='show status information'
        )
        status_parser.add_argument('status', action='store_true')

    @staticmethod
    def add_authenticate_child_parser(subparsers) -> None:
        authenticate_parent = CustomArgumentParser(add_help=False)
        authenticate_parser = subparsers.add_parser(
            'authenticate',
            parents=[authenticate_parent],
            help='authenticate a user'
        )
        authenticate_parser.add_argument('authenticate', action='store_true')
        authenticate_parser.add_argument('--name', required=True)
        authenticate_parser.add_argument('--password', default='')
