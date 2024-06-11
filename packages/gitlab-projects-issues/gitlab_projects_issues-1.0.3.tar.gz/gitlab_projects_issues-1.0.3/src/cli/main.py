#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, ArgumentParser, Namespace, RawTextHelpFormatter)
from os import environ
from shutil import get_terminal_size
from sys import exit as sys_exit

# Components
from ..package.bundle import Bundle
from ..package.settings import Settings
from ..package.updates import Updates
from ..package.version import Version
from ..prints.colors import Colors
from ..system.platform import Platform
from .entrypoint import Entrypoint

# Main, pylint: disable=too-many-statements
def main() -> None:

    # Variables
    group: _ArgumentGroup
    result: Entrypoint.Result = Entrypoint.Result.ERROR

    # Arguments creation
    parser: ArgumentParser = ArgumentParser(
        prog=Bundle.NAME,
        description=f'{Bundle.NAME}: {Bundle.DESCRIPTION}',
        add_help=False,
        formatter_class=lambda prog: RawTextHelpFormatter(
            prog,
            max_help_position=40,
            width=min(
                120,
                get_terminal_size().columns - 2,
            ),
        ),
    )

    # Arguments internal definitions
    group = parser.add_argument_group('internal arguments')
    group.add_argument(
        '-h',
        '--help',
        dest='help',
        action='store_true',
        help='Show this help message',
    )
    group.add_argument(
        '--version',
        dest='version',
        action='store_true',
        help='Show the current version',
    )
    group.add_argument(
        '--update-check',
        dest='update_check',
        action='store_true',
        help='Check for newer package updates',
    )
    group.add_argument(
        '--settings',
        dest='settings',
        action='store_true',
        help='Show the current settings path and contents',
    )
    group.add_argument(
        '--set',
        dest='set',
        action='store',
        metavar=('GROUP', 'KEY', 'VAL'),
        nargs=3,
        help='Set settings specific \'VAL\' value to [GROUP] > KEY\n' \
             'or unset by using \'UNSET\' as \'VAL\'',
    )

    # Arguments credentials definitions
    group = parser.add_argument_group('credentials arguments')
    group.add_argument(
        '-t',
        dest='token',
        default=environ.get(Bundle.ENV_GITLAB_TOKEN, ''), #
        help=f'GitLab API token (default: {Bundle.ENV_GITLAB_TOKEN} environment)',
    )

    # Arguments common definitions
    group = parser.add_argument_group('common arguments')
    group.add_argument(
        '--dump',
        dest='dump',
        action='store_true',
        help='Dump Python objects of projects',
    )

    # Arguments issues definitions
    group = parser.add_argument_group('issues arguments')
    group.add_argument(
        '--default-estimate',
        dest='default_estimate',
        default='8',
        action='store',
        help='Default issue time estimate if none provided'
        'in hours (default: %(default)s)',
    )
    group.add_argument(
        '--exclude-closed-issues',
        dest='exclude_closed_issues',
        action='store_true',
        help='Exclude issues in closed state',
    )

    # Arguments milestones definitions
    group = parser.add_argument_group('milestones arguments')
    group.add_argument(
        '--milestone',
        dest='milestone',
        action='store',
        help='Use a specific milestone by name, by ID, or "None"',
    )
    group.add_argument(
        '--milestones-statistics',
        dest='milestones_statistics',
        action='store_true',
        help='Inject milestones statistics into milestones\' description',
    )
    group.add_argument(
        '--exclude-closed-milestones',
        dest='exclude_closed_milestones',
        action='store_true',
        help='Exclude milestones in closed state',
    )

    # Arguments positional definitions
    group = parser.add_argument_group('positional arguments')
    group.add_argument(
        '--',
        dest='double_dash',
        action='store_true',
        help='Positional arguments separator (recommended)',
    )
    group.add_argument(
        dest='gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='GitLab URL (default: %(default)s)',
    )
    group.add_argument(
        dest='path',
        action='store',
        nargs='?',
        help='GitLab project path',
    )

    # Arguments parser
    options: Namespace = parser.parse_args()

    # Help informations
    if options.help:
        print(' ')
        parser.print_help()
        print(' ')
        Platform.flush()
        sys_exit(0)

    # Instantiate settings
    settings: Settings = Settings(name=Bundle.NAME)

    # Prepare colors
    Colors.prepare()

    # Settings setter
    if options.set:
        settings.set(options.set[0], options.set[1], options.set[2])
        settings.show()
        sys_exit(0)

    # Settings informations
    if options.settings:
        settings.show()
        sys_exit(0)

    # Instantiate updates
    updates: Updates = Updates(name=Bundle.NAME, settings=settings)

    # Version informations
    if options.version:
        print(
            f'{Bundle.NAME} {Version.get()} from {Version.path()} (python {Version.python()})'
        )
        Platform.flush()
        sys_exit(0)

    # Check for current updates
    if options.update_check:
        if not updates.check():
            updates.check(older=True)
        sys_exit(0)

    # Arguments validation
    if not options.token or not options.gitlab or not options.path:
        result = Entrypoint.Result.CRITICAL

    # Header
    print(' ')
    Platform.flush()

    # CLI entrypoint
    if result != Entrypoint.Result.CRITICAL:
        result = Entrypoint.cli(options)

    # CLI helper
    else:
        parser.print_help()

    # Footer
    print(' ')
    Platform.flush()

    # Check for daily updates
    if updates.enabled and updates.daily:
        updates.check()

    # Result
    if result in [Entrypoint.Result.SUCCESS, Entrypoint.Result.FINALIZE]:
        sys_exit(0)
    else:
        sys_exit(1)

# Entrypoint
if __name__ == '__main__': # pragma: no cover
    main()
