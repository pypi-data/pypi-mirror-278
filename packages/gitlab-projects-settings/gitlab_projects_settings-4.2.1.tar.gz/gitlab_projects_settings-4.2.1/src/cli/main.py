#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, _MutuallyExclusiveGroup, ArgumentParser, Namespace,
                      RawTextHelpFormatter)
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
from ..types.gitlab import ProtectionLevels
from .entrypoint import Entrypoint

# Main, pylint: disable=too-many-statements
def main() -> None:

    # Variables
    group: _ArgumentGroup
    result: Entrypoint.Result = Entrypoint.Result.ERROR
    subgroup: _MutuallyExclusiveGroup

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

    # Arguments common settings definitions
    group = parser.add_argument_group('common settings arguments')
    group.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='Enable dry run mode to check without saving',
    )
    group.add_argument(
        '--dump',
        dest='dump',
        action='store_true',
        help='Dump Python objects of groups and projects',
    )
    group.add_argument(
        '--exclude-group',
        dest='exclude_group',
        action='store_true',
        help='Exclude parent group settings',
    )
    group.add_argument(
        '--exclude-subgroups',
        dest='exclude_subgroups',
        action='store_true',
        help='Exclude children subgroups settings',
    )
    group.add_argument(
        '--exclude-projects',
        dest='exclude_projects',
        action='store_true',
        help='Exclude children projects settings',
    )

    # Arguments general settings definitions
    group = parser.add_argument_group('general settings arguments')
    group.add_argument(
        '--available-features',
        dest='available_features',
        action='store_true',
        help='List the available GitLab project features known by the tool',
    )
    group.add_argument(
        '--reset-features',
        dest='reset_features',
        action='store',
        metavar='KEEP_FEATURES',
        nargs='?',
        const='',
        help='Reset features of GitLab projects based on usage\n'
        '(Optionally keep features separated by ",")',
    )
    group.add_argument(
        '--disable-features',
        dest='disable_features',
        metavar='FEATURES',
        help='List of features to disable separated by ","',
    )
    group.add_argument(
        '--enable-features',
        dest='enable_features',
        metavar='FEATURES',
        help='List of features to enable separated by ","',
    )
    group.add_argument(
        '--reset-members',
        dest='reset_members',
        action='store_true',
        help='Reset members of GitLab projects and groups',
    )
    group.add_argument(
        '--set-avatar',
        dest='set_avatar',
        action='store',
        metavar='FILE',
        help='Set avatar of GitLab projects and groups',
    )
    group.add_argument(
        '--set-description',
        dest='set_description',
        action='store',
        metavar='TEXT',
        help='Set description of GitLab projects and groups',
    )
    group.add_argument(
        '--update-description',
        dest='update_description',
        action='store_true',
        help='Update description of GitLab projects and groups automatically',
    )

    # Arguments advanced settings definitions
    group = parser.add_argument_group('advanced settings arguments')
    group.add_argument(
        '--run-housekeeping',
        dest='run_housekeeping',
        action='store_true',
        help='Run housekeeping of project or projects GitLab in groups',
    )
    subgroup = group.add_mutually_exclusive_group()
    subgroup.add_argument(
        '--archive-project',
        dest='archive_project',
        action='store_true',
        help='Archive project or projects in GitLab groups',
    )
    subgroup.add_argument(
        '--unarchive-project',
        dest='unarchive_project',
        action='store_true',
        help='Unarchive project or projects in GitLab groups',
    )
    group.add_argument(
        '--delete-group',
        dest='delete_group',
        action='store_true',
        help='Delete group or groups in GitLab groups',
    )
    group.add_argument(
        '--delete-project',
        dest='delete_project',
        action='store_true',
        help='Delete project or projects in GitLab groups',
    )

    # Arguments repository settings definitions
    group = parser.add_argument_group('repository settings arguments')
    group.add_argument(
        '--protect-branches',
        dest='protect_branches',
        action='store_true',
        help='Protect branches with default master/main, develop and staging',
    )
    group.add_argument(
        '--protect-tags',
        dest='protect_tags',
        action='store',
        metavar='LEVEL',
        nargs='?',
        const=ProtectionLevels.default(),
        help=f'Protect tags at level [{",".join(ProtectionLevels.names())}]'
        ' (default: %(const)s)',
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
        help='GitLab group, user namespace or project path',
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
