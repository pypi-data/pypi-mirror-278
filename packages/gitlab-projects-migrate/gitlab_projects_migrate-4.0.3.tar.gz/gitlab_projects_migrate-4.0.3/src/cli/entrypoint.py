#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from enum import Enum
import re
from tempfile import NamedTemporaryFile
from typing import Optional

# Modules libraries
from gitlab.exceptions import GitlabGetError
from gitlab.v4.objects import (
    Group as GitLabGroup,
    Namespace as GitLabNamespace,
    Project as GitLabProject,
    ProjectImport as GitLabProjectImport,
    User as GitLabUser,
)
import questionary

# Components
from ..features.gitlab import GitLabFeature
from ..package.bundle import Bundle
from ..prints.colors import Colors
from ..prints.themes import Themes
from ..system.platform import Platform
from ..types.namespaces import Namespaces
from ..types.paths import Paths

# Entrypoint class, pylint: disable=too-few-public-methods,too-many-nested-blocks,too-many-statements
class Entrypoint:

    # Constants
    EXPORTS_PREFIX: str = f'{Bundle.NAME}-exports-'

    # Enumerations
    Result = Enum('Result', ['SUCCESS', 'FINALIZE', 'ERROR', 'CRITICAL'])

    # CLI, pylint: disable=too-many-branches
    @staticmethod
    def cli(options: Namespace) -> Result:

        # Variables
        input_group: Optional[GitLabGroup] = None
        input_project: Optional[GitLabProject] = None
        input_user: Optional[GitLabUser] = None
        output_exists: bool = False
        output_namespace: Optional[GitLabNamespace] = None
        result: Entrypoint.Result = Entrypoint.Result.ERROR

        # Header
        print(' ')

        # Input client
        input_gitlab = GitLabFeature(
            options.input_gitlab,
            options.input_token,
            options.dry_run,
        )
        print(f'{Colors.BOLD} - GitLab input: '
              f'{Colors.GREEN}{input_gitlab.url}'
              f'{Colors.RESET}')
        Platform.flush()

        # Output client
        output_gitlab = GitLabFeature(options.output_gitlab, options.output_token,
                                      options.dry_run)
        print(f'{Colors.BOLD} - GitLab output: '
              f'{Colors.GREEN}{output_gitlab.url}'
              f'{Colors.RESET}')
        print(' ')
        Platform.flush()

        # Input path
        try:
            input_group = input_gitlab.group(options.input_path)
            print(f'{Colors.BOLD} - GitLab input group: '
                  f'{Colors.GREEN}{input_group.full_path}'
                  f'{Colors.CYAN} ({Namespaces.text(input_group.description)})'
                  f'{Colors.RESET}')
            Platform.flush()
        except GitlabGetError as exception:
            try:
                if '/' in options.input_path:
                    raise TypeError from exception
                input_user = input_gitlab.user(options.input_path)
                input_namespace = input_gitlab.namespace(options.input_path)
                print(f'{Colors.BOLD} - GitLab input user namespace: '
                      f'{Colors.GREEN}{input_namespace.full_path}'
                      f'{Colors.CYAN} ({input_namespace.name})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()
            except (GitlabGetError, TypeError):
                input_project = input_gitlab.project(options.input_path)
                print(f'{Colors.BOLD} - GitLab input project: '
                      f'{Colors.GREEN}{input_project.path_with_namespace}'
                      f'{Colors.CYAN} ({Namespaces.text(input_project.description)})'
                      f'{Colors.RESET}')
                Platform.flush()

        # Output group
        try:
            output_exists = False
            output_group = output_gitlab.group(options.output_namespace)
            output_namespace = output_gitlab.namespace(options.output_namespace)
            output_exists = True
            print(f'{Colors.BOLD} - GitLab output group: '
                  f'{Colors.GREEN}{output_group.full_path}'
                  f'{Colors.CYAN} ({Namespaces.text(output_group.description)})'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()

        # Output namespace
        except GitlabGetError as exception:
            try:
                if '/' in options.output_namespace:
                    raise TypeError from exception
                _output_user = output_gitlab.user(options.output_namespace)
                output_namespace = output_gitlab.namespace(options.output_namespace)
                print(f'{Colors.BOLD} - GitLab output user namespace: '
                      f'{Colors.GREEN}{output_namespace.full_path}'
                      f'{Colors.CYAN} ({output_namespace.name})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()

            # Output parent group
            except (GitlabGetError, TypeError): # pylint: disable=raise-missing-from

                # Validate options
                if (not input_group and not input_user) or options.exclude_group:
                    raise exception

                # Missing output group
                print(f'{Colors.BOLD} - GitLab output group: '
                      f'{Colors.GREEN}{options.output_namespace}'
                      f'{Colors.RED} (Non-existent output group)'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()

        # Validate options
        if options.rename_project and not input_project:
            raise RuntimeError(
                'Renaming project is only allowed with a single input project')

        # Handle single project
        if input_project:

            # Validate types
            assert output_namespace

            # Handle project
            Entrypoint.project(
                options,
                input_gitlab,
                output_gitlab,
                input_project.path_with_namespace,
                input_project.namespace['id'],
                output_namespace.full_path,
                options.rename_project,
            )

            # Handle sources
            if options.archive_sources or options.delete_sources:
                print(f'{Colors.BOLD} - GitLab input project: '
                      f'{Colors.GREEN}{input_project.path_with_namespace}'
                      f'{Colors.CYAN} ({Namespaces.text(input_project.description)})'
                      f'{Colors.RESET}')
                Platform.flush()

                # Archive input project
                if options.archive_sources:
                    input_gitlab.project_set_archive(
                        input_project.path_with_namespace,
                        enabled=True,
                    )
                    print(f'{Colors.BOLD}   - Archive sources project: '
                          f'{Colors.GREEN}Success'
                          f'{Colors.RESET}')
                    print(' ')
                    Platform.flush()

                # Delete input project
                elif options.delete_sources:

                    # Confirm project deletion
                    if not Entrypoint.confirm(
                            'Delete project',
                            input_project.path_with_namespace,
                            'deletion',
                    ):
                        raise PermissionError()

                    # Delete input project
                    input_gitlab.project_delete(input_project.path_with_namespace)
                    print(f'{Colors.BOLD}   - Delete sources project: '
                          f'{Colors.GREEN}Success'
                          f'{Colors.RESET}')
                    print(' ')
                    Platform.flush()

        # Handle group recursively
        elif input_group:

            # Handle group if missing
            if not options.exclude_group:
                result = Entrypoint.group(
                    options,
                    input_gitlab,
                    output_gitlab,
                    input_group.full_path,
                    options.output_namespace,
                    migration=not output_exists,
                )
                if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                    return result

                # Acquire output namespace
                output_namespace = output_gitlab.namespace(
                    options.output_namespace,
                    optional=True,
                )

            # Validate types
            assert output_namespace

            # Iterate through subgroups
            if not options.exclude_subgroups or not output_exists:
                for input_subgroup in sorted(
                        input_group.descendant_groups.list(
                            get_all=True,
                            include_subgroups=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.full_path,
                ):
                    result = Entrypoint.subgroup(
                        options,
                        input_gitlab,
                        output_gitlab,
                        input_group.full_path,
                        input_subgroup.full_path,
                        output_namespace.full_path,
                        migration=output_exists,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

            # Iterate through projects
            if not options.exclude_projects:
                for project in sorted(
                        input_group.projects.list(
                            get_all=True,
                            include_subgroups=not options.exclude_subgroups,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    result = Entrypoint.project(
                        options,
                        input_gitlab,
                        output_gitlab,
                        project.path_with_namespace,
                        input_group.full_path,
                        output_namespace.full_path,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

            # Delete input group after validation
            if options.delete_sources:
                print(f'{Colors.BOLD} - GitLab input group: '
                      f'{Colors.GREEN}{input_group.full_path}'
                      f'{Colors.CYAN} ({Namespaces.text(input_group.description)})'
                      f'{Colors.RESET}')
                Platform.flush()
                if not Entrypoint.confirm(
                        'Delete group',
                        input_group.full_path,
                        'deletion',
                ):
                    raise PermissionError()

                # Delete input group
                input_gitlab.group_delete(input_group.full_path)
                print(f'{Colors.BOLD}   - Delete sources group: '
                      f'{Colors.GREEN}Success'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()

        # Handle user
        elif input_user:

            # Validate types
            assert output_namespace

            # Iterate through projects
            if not options.exclude_projects:
                for project in sorted(
                        input_user.projects.list(
                            get_all=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    result = Entrypoint.project(
                        options,
                        input_gitlab,
                        output_gitlab,
                        project.path_with_namespace,
                        input_namespace.full_path,
                        output_namespace.full_path,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

                    # Handle sources
                    if options.archive_sources or options.delete_sources:
                        print(f'{Colors.BOLD} - GitLab input project: '
                              f'{Colors.GREEN}{project.path_with_namespace}'
                              f'{Colors.CYAN} ({Namespaces.text(project.description)})'
                              f'{Colors.RESET}')
                        Platform.flush()

                        # Archive input project
                        if options.archive_sources:
                            input_gitlab.project_set_archive(
                                project.path_with_namespace,
                                enabled=True,
                            )
                            print(f'{Colors.BOLD}   - Archive sources project: '
                                  f'{Colors.GREEN}Success'
                                  f'{Colors.RESET}')
                            print(' ')
                            Platform.flush()

                        # Delete input project
                        elif options.delete_sources:

                            # Confirm project deletion
                            if not Entrypoint.confirm(
                                    'Delete project',
                                    project.path_with_namespace,
                                    'deletion',
                            ):
                                print(' ')
                                Platform.flush()
                                return Entrypoint.Result.SUCCESS

                            # Delete input project
                            input_gitlab.project_delete(project.path_with_namespace)
                            print(f'{Colors.BOLD}   - Delete sources project: '
                                  f'{Colors.GREEN}Success'
                                  f'{Colors.RESET}')
                            print(' ')
                            Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS

    # Confirm
    @staticmethod
    def confirm(
        description: str,
        text: str = '',
        action: str = '',
    ) -> bool:

        # Header
        print(
            f'{Colors.BOLD}   - {description}: Confirm "'
            f'{Colors.RED}{text}'
            f'{Colors.BOLD}" {action}:'
            f'{Colors.RESET}', end='')
        Platform.flush()

        # Get user configuration
        answer: bool = questionary.confirm(
            message='',
            default=False,
            qmark='',
            style=Themes.confirmation_style(),
            auto_enter=True,
        ).ask()

        # Result
        return answer

    # Group, pylint: disable=too-many-arguments,too-many-locals
    @staticmethod
    def group(
        options: Namespace,
        input_gitlab: GitLabFeature,
        output_gitlab: GitLabFeature,
        criteria_input_group: str,
        criteria_output_group: str,
        migration: bool = True,
    ) -> Result:

        # Acquire input group
        input_group = input_gitlab.group(criteria_input_group)

        # Detect group or subgroup
        output_group_namespace, output_group_path = Namespaces.split_namespace(
            criteria_output_group,
            relative=False,
        )
        output_group_name = input_group.name \
            if input_group.name != input_group.path \
            else output_group_path

        # Show group details
        print(f'{Colors.BOLD} - GitLab group: '
              f'{Colors.YELLOW_LIGHT}{input_group.full_path} '
              f'{Colors.CYAN}({Namespaces.text(input_group.description)})'
              f'{Colors.RESET}')
        Platform.flush()

        # Migration mode
        if not migration:
            output_subgroup = output_gitlab.group(criteria_output_group)
            print(f'{Colors.BOLD}   - Already existing group in GitLab output: '
                  f'{Colors.GREEN}{output_subgroup.full_path}'
                  f'{Colors.CYAN} ({Namespaces.text(output_subgroup.description)})'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return Entrypoint.Result.SUCCESS

        # Confirm group is exportable
        export_limitations = input_gitlab.group_export_limitations(input_group.full_path)
        if export_limitations and not Entrypoint.confirm(
                'Limited group export',
                input_group.full_path,
                'which uses "' + ("\", \"").join(export_limitations) + '"',
        ):
            raise PermissionError()

        # Export group
        print(f'{Colors.BOLD}   - Exporting from: '
              f'{Colors.GREEN}{input_group.full_path}'
              f'{Colors.RESET}')
        Platform.flush()
        with NamedTemporaryFile(
                prefix=Paths.slugify(f'{Entrypoint.EXPORTS_PREFIX}'
                                     f'-{input_group.full_path}-'),
                suffix='.tar.gz',
                dir=options.archive_exports_dir,
                delete=not options.archive_exports_dir,
        ) as file_export:
            input_gitlab.group_export(
                file_export.name,
                input_group.full_path,
                options.keep_members,
            )

            # Import group
            print(f'{Colors.BOLD}   - Importing to: '
                  f'{Colors.GREEN}{criteria_output_group}'
                  f'{Colors.RESET}')
            Platform.flush()
            output_gitlab.group_import(
                file_export.name,
                output_group_namespace,
                output_group_path,
                output_group_name,
            )

        # Acquire output group
        output_group_criteria: str = ''
        if not options.dry_run:
            output_group = output_gitlab.group(criteria_output_group)
            output_group_criteria = output_group.full_path

        # Set group description
        description = Namespaces.describe(
            name=output_group_name,
            description=input_group.description,
        )
        output_gitlab.group_set_description(
            output_group_criteria,
            description,
        )
        print(f'{Colors.BOLD}   - Set description: '
              f'{Colors.CYAN}{description}'
              f'{Colors.RESET}')
        Platform.flush()

        # Set group avatar
        if options.set_avatar:
            output_gitlab.group_set_avatar(
                output_group_criteria,
                options.set_avatar,
            )
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Show group result
        print(f'{Colors.BOLD}   - Migrated group: '
              f'{Colors.GREEN}Success'
              f'{Colors.RESET}')
        Platform.flush()

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS

    # Project, pylint: disable=too-many-arguments,too-many-branches,too-many-locals
    @staticmethod
    def project(
        options: Namespace,
        input_gitlab: GitLabFeature,
        output_gitlab: GitLabFeature,
        criteria_project: str,
        criteria_input_namespace: str,
        criteria_output_namespace: str,
        rename_project: str = '',
    ) -> Result:

        # Variables
        output_project: GitLabProjectImport

        # Acquire input project
        input_project = input_gitlab.project(criteria_project)

        # Acquire input namespace
        input_namespace = input_gitlab.namespace(criteria_input_namespace)

        # Parse input subpath
        input_subpath = Namespaces.subpath(
            input_namespace.full_path,
            input_project.path_with_namespace,
        )

        # Acquire output namespace
        output_namespace = output_gitlab.namespace(
            criteria_output_namespace,
            optional=True,
        )

        # Project project name
        output_project_name: str = rename_project if rename_project else input_project.name

        # Parse output path
        output_subnamespace, output_path = Namespaces.split_namespace(
            input_subpath,
            relative=True,
        )
        if output_path:
            output_path = re.sub(
                f'{input_project.name}$',
                output_project_name,
                output_path,
            )

        # Parse output subpath
        output_subpath = Namespaces.subpath(
            output_namespace.full_path,
            f'{options.output_namespace}{output_subnamespace}/{output_path}',
        )

        # Show project details
        print(f'{Colors.BOLD} - GitLab input project: '
              f'{Colors.YELLOW_LIGHT}{input_project.path_with_namespace} '
              f'{Colors.CYAN}({Namespaces.text(input_project.description)})'
              f'{Colors.RESET}')
        Platform.flush()

        # Ignore existing projects
        if not options.overwrite and output_subpath in [
                Namespaces.subpath(
                    output_namespace.full_path,
                    output_project.path_with_namespace,
                ) for output_project in output_gitlab.namespace_projects(
                    criteria_output_namespace)
        ]:
            project = output_gitlab.project(
                f'{output_namespace.full_path}/{input_subpath}')
            print(f'{Colors.BOLD}   - Already existing project in GitLab output: '
                  f'{Colors.GREEN}{project.path_with_namespace}'
                  f'{Colors.CYAN} ({Namespaces.text(project.description)})'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return Entrypoint.Result.SUCCESS

        # Confirm project is exportable
        export_limitations = input_gitlab.project_export_limitations(
            input_project.path_with_namespace)
        if export_limitations and not Entrypoint.confirm(
                'Limited project export',
                input_project.path_with_namespace,
                'which uses "' + ("\", \"").join(export_limitations) + '"',
        ):
            raise PermissionError()

        # Export project
        print(f'{Colors.BOLD}   - Exporting from: '
              f'{Colors.GREEN}{output_namespace.full_path}'
              f'{Colors.CYAN} / {input_subpath}'
              f'{Colors.RESET}')
        Platform.flush()
        with NamedTemporaryFile(
                prefix=Paths.slugify(f'{Entrypoint.EXPORTS_PREFIX}'
                                     f'-{input_project.path_with_namespace}-'),
                suffix='.tar.gz',
                dir=options.archive_exports_dir,
                delete=not options.archive_exports_dir,
        ) as file_export:
            input_gitlab.project_export(
                file_export.name,
                input_project.path_with_namespace,
                options.keep_members,
            )

            # Existing project removal
            if options.overwrite:
                if not Entrypoint.confirm(
                        'Delete project',
                        f'{output_namespace.full_path}/{input_subpath}',
                        'deletion',
                ):
                    raise PermissionError()
                output_gitlab.project_delete(
                    f'{output_namespace.full_path}/{input_subpath}')

            # Import project
            print(f'{Colors.BOLD}   - Importing to: '
                  f'{Colors.GREEN}{options.output_namespace}'
                  f'{Colors.CYAN} / {output_subpath}'
                  f'{Colors.RESET}')
            Platform.flush()
            output_project = output_gitlab.project_import(
                file_export.name,
                f'{options.output_namespace}{output_subnamespace}',
                output_path,
                output_project_name,
                options.overwrite,
            )

        # Acquire subgroup description
        output_subgroup_description: str
        if options.dry_run:
            output_subgroup_description = input_project.description
        elif output_namespace.kind == 'user':
            output_subgroup_description = output_namespace.name
        else:
            output_subgroup = output_gitlab.group(
                f'{options.output_namespace}{output_subnamespace}')
            output_subgroup_description = output_subgroup.description

        # Update project description
        if options.update_description:
            group_description = Namespaces.describe(
                name=output_project_name,
                description=output_subgroup_description,
            )
            if not output_project.description or \
                    not output_project.description.endswith(f' - {group_description}'):
                description = f'{Namespaces.describe(name=output_project.name)}' \
                                f' - {group_description}'
                output_gitlab.project_set_description(
                    output_project.path_with_namespace,
                    description,
                )
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{Namespaces.text(output_project.description)}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset project members
        if not options.keep_members:
            output_gitlab.project_reset_members(output_project.path_with_namespace)
            print(f'{Colors.BOLD}   - Reset members: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Set project avatar
        if options.set_avatar:
            output_gitlab.project_set_avatar(
                output_project.path_with_namespace,
                options.set_avatar,
            )
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Show project result
        print(f'{Colors.BOLD}   - Migrated project: '
              f'{Colors.GREEN}Success'
              f'{Colors.RESET}')
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS

    # Subgroup, pylint: disable=too-many-arguments,too-many-statements
    @staticmethod
    def subgroup(
        options: Namespace,
        input_gitlab: GitLabFeature,
        output_gitlab: GitLabFeature,
        criteria_input_group: str,
        criteria_input_subgroup: str,
        criteria_output_group: str,
        migration: bool = True,
    ) -> Result:

        # Acquire input group
        input_group = input_gitlab.group(criteria_input_group)

        # Acquire input subgroup
        input_subgroup = input_gitlab.group(criteria_input_subgroup)

        # Acquire output group
        output_group = output_gitlab.group(criteria_output_group, optional=True)

        # Show subgroup details
        print(f'{Colors.BOLD} - GitLab subgroup: '
              f'{Colors.YELLOW_LIGHT}{input_subgroup.full_path} '
              f'{Colors.CYAN}({Namespaces.text(input_subgroup.description)})'
              f'{Colors.RESET}')
        Platform.flush()

        # Parse subgroup paths
        input_subpath = Namespaces.subpath(
            input_group.full_path,
            input_subgroup.full_path,
        )
        output_namespace, output_path = Namespaces.split_namespace(
            input_subpath,
            relative=True,
        )

        # Migration mode
        if migration:

            # Ignore existing subgroup
            if input_subpath in [
                    Namespaces.subpath(
                        output_group.full_path,
                        output_subgroup.full_path,
                    ) for output_subgroup in output_group.descendant_groups.list(
                        get_all=True,
                        include_subgroups=True,
                    )
            ]:
                output_subgroup = output_gitlab.group(
                    f'{output_group.full_path}/{input_subpath}')
                print(f'{Colors.BOLD}   - Already existing subgroup in GitLab output: '
                      f'{Colors.GREEN}{output_subgroup.full_path}'
                      f'{Colors.CYAN} ({Namespaces.text(output_subgroup.description)})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()
                return Entrypoint.Result.SUCCESS

            # Confirm subgroup is exportable
            export_limitations = input_gitlab.group_export_limitations(
                input_subgroup.full_path)
            if export_limitations and not Entrypoint.confirm(
                    'Limited subgroup export',
                    input_subgroup.full_path,
                    'which uses "' + ("\", \"").join(export_limitations) + '"',
            ):
                raise PermissionError()

            # Export subgroup
            print(f'{Colors.BOLD}   - Exporting from: '
                  f'{Colors.GREEN}{input_subgroup.full_path}'
                  f'{Colors.RESET}')
            Platform.flush()
            with NamedTemporaryFile(
                    prefix=Paths.slugify(f'{Entrypoint.EXPORTS_PREFIX}'
                                         f'-{input_subgroup.full_path}-'),
                    suffix='.tar.gz',
                    dir=options.archive_exports_dir,
                    delete=not options.archive_exports_dir,
            ) as file_export:
                input_gitlab.group_export(
                    file_export.name,
                    input_subgroup.full_path,
                    options.keep_members,
                )

                # Import subgroup
                print(
                    f'{Colors.BOLD}   - Importing to: '
                    f'{Colors.GREEN}{output_group.full_path}{output_namespace}/{output_path}'
                    f'{Colors.RESET}')
                Platform.flush()
                output_gitlab.group_import(
                    file_export.name,
                    f'{output_group.full_path}{output_namespace}',
                    output_path,
                    input_subgroup.name,
                )

        # Acquire subgroups
        output_subgroup_child_description: str
        output_subgroup_child_name: str
        output_subgroup_parent_description: str
        if not options.dry_run:
            output_subgroup_parent = output_gitlab.group(
                f'{output_group.full_path}{output_namespace}')
            output_subgroup_parent_description = output_subgroup_parent.description
            output_subgroup_child = output_gitlab.group(
                f'{output_group.full_path}/{input_subpath}')
            output_subgroup_child_description = output_subgroup_child.description
            output_subgroup_child_name = output_subgroup_child.name
        else:
            output_subgroup_parent_description = input_subgroup.description
            output_subgroup_child_description = input_subgroup.description
            output_subgroup_child_name = input_subgroup.name

        # Update group description
        if options.update_description:
            parent_description = Namespaces.describe(
                name=output_subgroup_child_name,
                description=output_subgroup_parent_description,
            )
            if not output_subgroup_child_description.endswith(f' - {parent_description}'):
                description = f'{Namespaces.describe(name=output_subgroup_child_name)}' \
                              f' - {parent_description}'
                output_gitlab.group_set_description(
                    f'{output_group.full_path}/{input_subpath}',
                    description,
                )
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{output_subgroup_child_description}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Set group avatar
        if options.set_avatar:
            output_gitlab.group_set_avatar(
                f'{output_group.full_path}/{input_subpath}',
                options.set_avatar,
            )
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Show subgroup result
        print(f'{Colors.BOLD}   - Migrated subgroup: '
              f'{Colors.GREEN}Success'
              f'{Colors.RESET}')
        Platform.flush()

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS
