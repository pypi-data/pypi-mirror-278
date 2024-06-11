#!/usr/bin/env python3

# Standard libraries
from argparse import (_ArgumentGroup, ArgumentParser, Namespace, RawTextHelpFormatter,
                      SUPPRESS)
from os import environ
from pathlib import Path
from shutil import get_terminal_size
from sys import exit as sys_exit

# Components
from ..package.bundle import Bundle
from ..package.settings import Settings
from ..package.updates import Updates
from ..package.version import Version
from ..prints.colors import Colors
from ..system.platform import Platform
from ..types.paths import Paths
from .entrypoint import Entrypoint

# Main, pylint: disable=too-many-branches,too-many-statements
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
            max_help_position=30,
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
        '-I',
        dest='input_token',
        default=environ.get(
            Bundle.ENV_GITLAB_INPUT_TOKEN,
            environ.get(
                Bundle.ENV_GITLAB_TOKEN,
                '',
            ),
        ),
        help=f'Input GitLab API token (default: {Bundle.ENV_GITLAB_INPUT_TOKEN}'
        f' or {Bundle.ENV_GITLAB_TOKEN} environments)',
    )
    group.add_argument(
        '-O',
        dest='output_token',
        action='store',
        default=environ.get(
            Bundle.ENV_GITLAB_OUTPUT_TOKEN,
            environ.get(
                Bundle.ENV_GITLAB_TOKEN,
                '',
            ),
        ), #
        help=f'Output GitLab API token (default: {Bundle.ENV_GITLAB_OUTPUT_TOKEN}'
        f', {Bundle.ENV_GITLAB_TOKEN} environments,'
        ' or INPUT_TOKEN argument)',
    )

    # Arguments migration definitions
    group = parser.add_argument_group('migration arguments')
    group.add_argument(
        '--archive-exports',
        dest='archive_exports',
        action='store',
        metavar='FOLDER',
        help='Store exported projects and groups to a folder',
    )
    subgroup = group.add_mutually_exclusive_group()
    subgroup.add_argument(
        '--archive-sources',
        dest='archive_sources',
        action='store_true',
        help='Archive sources after successful migration',
    )
    subgroup.add_argument(
        '--delete-sources',
        dest='delete_sources',
        action='store_true',
        help='Delete sources after successful migration',
    )
    group.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='Enable dry run mode to check without saving',
    )
    group.add_argument(
        '--exclude-group',
        dest='exclude_group',
        action='store_true',
        help='Exclude parent group migration',
    )
    group.add_argument(
        '--exclude-subgroups',
        dest='exclude_subgroups',
        action='store_true',
        help='Exclude children subgroups migration',
    )
    group.add_argument(
        '--exclude-projects',
        dest='exclude_projects',
        action='store_true',
        help='Exclude children projects migration',
    )
    group.add_argument(
        '--keep-members',
        dest='keep_members',
        action='store_true',
        help='Keep input members after importing on output GitLab',
    )
    group.add_argument(
        '--overwrite',
        dest='overwrite',
        action='store_true',
        help='Overwrite existing projects on output GitLab',
    )
    group.add_argument(
        '--rename-project',
        dest='rename_project',
        action='store',
        metavar='NAME',
        help='Rename GitLab output project (only for single input project)',
    )

    # Arguments general settings definitions
    group = parser.add_argument_group('general settings arguments')
    group.add_argument(
        '--set-avatar',
        dest='set_avatar',
        action='store',
        metavar='FILE',
        help='Set avatar of GitLab output projects and groups',
    )
    group.add_argument(
        '--update-description',
        dest='update_description',
        action='store_true',
        help='Update description of GitLab output projects and groups automatically',
    )

    # Arguments hidden definitions
    group = parser.add_argument_group('hidden arguments')
    group.add_argument(
        '--archive-exports-dir',
        dest='archive_exports_dir',
        action='store',
        default=None,
        help=SUPPRESS,
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
        dest='input_gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='Input GitLab URL (default: https://gitlab.com)',
    )
    group.add_argument(
        dest='input_path',
        action='store',
        nargs='?',
        help='Input GitLab group, user namespace or project path',
    )
    group.add_argument(
        dest='output_gitlab',
        action='store',
        nargs='?',
        default='https://gitlab.com',
        help='Output GitLab URL (default: https://gitlab.com)',
    )
    group.add_argument(
        dest='output_namespace',
        action='store',
        nargs='?',
        default='',
        help='Output GitLab group or user namespace',
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
    if not options.input_token or not options.input_gitlab or not options.input_path \
            or not options.output_gitlab or not options.output_namespace:
        result = Entrypoint.Result.CRITICAL

    # Prepare archive exports
    if options.archive_exports:
        options.archive_exports_dir = Paths.resolve(Path('.') / options.archive_exports)
        Path(options.archive_exports_dir).mkdir(parents=True, exist_ok=True)

    # Arguments adaptations
    if not options.output_token:
        options.output_token = options.input_token

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
