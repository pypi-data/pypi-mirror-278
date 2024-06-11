#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from enum import Enum
from typing import Optional

# Modules libraries
from gitlab.exceptions import GitlabGetError
from gitlab.v4.objects import (
    Group as GitLabGroup,
    Project as GitLabProject,
    User as GitLabUser,
)
import questionary

# Components
from ..features.gitlab import GitLabFeature
from ..prints.colors import Colors
from ..prints.themes import Themes
from ..system.platform import Platform
from ..types.namespaces import Namespaces

# Entrypoint class, pylint: disable=too-few-public-methods
class Entrypoint:

    # Enumerations
    Result = Enum('Result', ['SUCCESS', 'FINALIZE', 'ERROR', 'CRITICAL'])

    # CLI, pylint: disable=too-many-branches
    @staticmethod
    def cli(options: Namespace) -> Result:

        # Variables
        group: Optional[GitLabGroup] = None
        project: Optional[GitLabProject] = None
        result: Entrypoint.Result = Entrypoint.Result.ERROR
        user: Optional[GitLabUser] = None

        # Header
        print(' ')

        # GitLab client
        gitlab = GitLabFeature(
            options.gitlab,
            options.token,
            options.dry_run,
        )
        print(f'{Colors.BOLD} - GitLab host: '
              f'{Colors.GREEN}{gitlab.url}'
              f'{Colors.RESET}')
        Platform.flush()

        # GitLab path
        try:
            group = gitlab.group(options.path)
            print(f'{Colors.BOLD} - GitLab group: '
                  f'{Colors.GREEN}{group.full_path}'
                  f'{Colors.CYAN} ({group.description})'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
        except GitlabGetError as exception:
            try:
                if '/' in options.path:
                    raise TypeError from exception
                user = gitlab.user(options.path)
                namespace = gitlab.namespace(options.path)
                print(f'{Colors.BOLD} - GitLab user namespace: '
                      f'{Colors.GREEN}{namespace.full_path}'
                      f'{Colors.CYAN} ({namespace.name})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()
            except (GitlabGetError, TypeError):
                project = gitlab.project(options.path)
                print(f'{Colors.BOLD} - GitLab project: '
                      f'{Colors.GREEN}{project.path_with_namespace}'
                      f'{Colors.CYAN} ({project.description})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()

        # Handle available features
        if options.available_features:
            print(f'{Colors.BOLD} - GitLab project:'
                  f'{Colors.RESET}')
            print(f'{Colors.BOLD}   - Available features: '
                  f'{Colors.CYAN}{", ".join(GitLabFeature.project_features_available())}'
                  f'{Colors.RESET}')
            Platform.flush()
            return Entrypoint.Result.FINALIZE

        # Handle single project
        if project:
            Entrypoint.project(
                options,
                gitlab,
                project.path_with_namespace,
            )

        # Handle group recursively
        elif group:

            # Handle group
            if not options.exclude_group:
                result = Entrypoint.group(
                    options,
                    gitlab,
                    group.full_path,
                )
                if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                    return result

            # Iterate through subgroups
            if not options.exclude_subgroups:
                for group_subgroup in sorted(
                        group.descendant_groups.list(
                            get_all=True,
                            include_subgroups=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.full_path,
                ):
                    result = Entrypoint.group(
                        options,
                        gitlab,
                        group_subgroup.full_path,
                        True,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

            # Iterate through projects
            if not options.exclude_projects:
                for group_project in sorted(
                        group.projects.list(
                            get_all=True,
                            include_subgroups=not options.exclude_subgroups,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    result = Entrypoint.project(
                        options,
                        gitlab,
                        group_project.path_with_namespace,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

        # Handle user recursively
        elif user:

            # Iterate through projects
            if not options.exclude_projects:
                for user_project in sorted(
                        user.projects.list(
                            get_all=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    result = Entrypoint.project(
                        options,
                        gitlab,
                        user_project.path_with_namespace,
                    )
                    if result in [Entrypoint.Result.FINALIZE, Entrypoint.Result.ERROR]:
                        return result

        # Result
        return Entrypoint.Result.SUCCESS

    # Confirm
    @staticmethod
    def confirm(description: str, text: str = '') -> bool:

        # Header
        print(
            f'{Colors.BOLD}   - Delete {description}: Confirm "'
            f'{Colors.RED}{text}'
            f'{Colors.BOLD}" deletion:'
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

    # Group
    @staticmethod
    def group(
        options: Namespace,
        gitlab: GitLabFeature,
        criteria: str,
        subgroup: bool = False,
    ) -> Result:

        # Acquire group
        group = gitlab.group(criteria)

        # Acquire parent group
        parent_group: Optional[GitLabGroup] = None
        if group.parent_id:
            parent_group = gitlab.group(group.parent_id)

        # Get parent description
        parent_description: str = ''
        parent_name: str = ''
        if parent_group:
            parent_description = parent_group.description
            parent_name = parent_group.name

        # Show group details
        group_type = 'subgroup' if subgroup else 'group'
        print(f'{Colors.BOLD} - GitLab {group_type}: '
              f'{Colors.YELLOW_LIGHT}{group.full_path} '
              f'{Colors.CYAN}({group.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Delete group after validation
        if options.delete_group:
            if not Entrypoint.confirm(
                    group_type,
                    group.full_path,
            ):
                print(' ')
                Platform.flush()
                return Entrypoint.Result.SUCCESS

            # Delete group
            gitlab.group_delete(criteria)
            print(f'{Colors.BOLD}   - Delete {group_type}: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return Entrypoint.Result.SUCCESS if subgroup else Entrypoint.Result.FINALIZE

        # Set group description
        if options.set_description:
            gitlab.group_set_description(criteria, options.set_description)
            print(f'{Colors.BOLD}   - Set description: '
                  f'{Colors.CYAN}{options.set_description}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Update group description
        elif options.update_description:
            parent_description_text: str = ''
            if parent_name:
                parent_description_text = ' - ' + Namespaces.describe(
                    name=parent_name,
                    description=parent_description,
                )
            if not group.description or subgroup and ( \
                        not parent_description_text or \
                        not group.description.endswith(f'{parent_description_text}') \
                    ):
                description = f'{Namespaces.describe(name=group.name)}' \
                              f'{parent_description_text}'
                gitlab.group_set_description(criteria, description)
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{group.description}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset group members
        if options.reset_members:
            gitlab.group_reset_members(criteria)
            print(f'{Colors.BOLD}   - Reset members: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Set group avatar
        if options.set_avatar:
            gitlab.group_set_avatar(criteria, options.set_avatar)
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Dump group object
        if options.dump:
            print(' ')
            print(group.to_json())

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS

    # Project, pylint: disable=too-many-branches,too-many-statements
    @staticmethod
    def project(
        options: Namespace,
        gitlab: GitLabFeature,
        criteria: str,
    ) -> Result:

        # Acquire project
        project = gitlab.project(criteria)

        # Show project details
        print(f'{Colors.BOLD} - GitLab project: '
              f'{Colors.YELLOW_LIGHT}{project.path_with_namespace} '
              f'{Colors.CYAN}({project.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Delete project after validation
        if options.delete_project:
            if not Entrypoint.confirm(
                    'project',
                    project.path_with_namespace,
            ):
                print(' ')
                Platform.flush()
                return Entrypoint.Result.SUCCESS

            # Delete project
            gitlab.project_delete(criteria)
            print(f'{Colors.BOLD}   - Delete project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return Entrypoint.Result.SUCCESS

        # Set project description
        if options.set_description:
            gitlab.project_set_description(criteria, options.set_description)
            print(f'{Colors.BOLD}   - Set description: '
                  f'{Colors.CYAN}{options.set_description}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Update project description
        elif options.update_description:
            namespace_description: str
            if project.namespace['kind'] == 'user':
                namespace = gitlab.namespace(project.namespace['id'])
                namespace_description = namespace.name
            else:
                group = gitlab.group(project.namespace['id'])
                namespace_description = Namespaces.describe(
                    name=group.name,
                    description=group.description,
                )
            if not project.description or \
                    not project.description.endswith(f' - {namespace_description}'):
                description = f'{Namespaces.describe(name=project.name)}' \
                              f' - {namespace_description}'
                gitlab.project_set_description(criteria, description)
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{project.description}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset project features
        if options.reset_features is not None:
            features = ', '.join(
                gitlab.project_features_reset(
                    criteria,
                    GitLabFeature.project_features_parse(options.reset_features),
                ))
            if features:
                print(f'{Colors.BOLD}   - Reset features: '
                      f'{Colors.CYAN}{features}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Reset features: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Disable project features
        if options.disable_features:
            features = ', '.join(
                gitlab.project_features_disable(
                    criteria,
                    GitLabFeature.project_features_parse(options.disable_features),
                ))
            if features:
                print(f'{Colors.BOLD}   - Disable features: '
                      f'{Colors.CYAN}{features}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Disable features: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Enable project features
        if options.enable_features:
            features = ', '.join(
                gitlab.project_features_enable(
                    criteria,
                    GitLabFeature.project_features_parse(options.enable_features),
                ))
            if features:
                print(f'{Colors.BOLD}   - Enable features: '
                      f'{Colors.CYAN}{features}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Enable features: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset project members
        if options.reset_members:
            gitlab.project_reset_members(criteria)
            print(f'{Colors.BOLD}   - Reset members: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Set project avatar
        if options.set_avatar:
            gitlab.project_set_avatar(criteria, options.set_avatar)
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Run project housekeeping
        if options.run_housekeeping:
            gitlab.project_run_housekeeping(criteria)
            print(f'{Colors.BOLD}   - Ran housekeeping: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Archive project
        if options.archive_project:
            gitlab.project_set_archive(criteria, True)
            print(f'{Colors.BOLD}   - Archive project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Unarchive project
        elif options.unarchive_project:
            gitlab.project_set_archive(criteria, False)
            print(f'{Colors.BOLD}   - Unarchive project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Protect project branches
        if options.protect_branches:
            branches = ', '.join(gitlab.project_protect_branches(criteria))
            if branches:
                print(f'{Colors.BOLD}   - Protecting branches: '
                      f'{Colors.CYAN}{branches}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Protecting branches: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Protect project tags
        if options.protect_tags:
            tags = ', '.join(gitlab.project_protect_tags(criteria, options.protect_tags))
            if tags:
                print(f'{Colors.BOLD}   - Protecting tags: '
                      f'{Colors.CYAN}{tags}'
                      f'{Colors.GREEN} (level: {options.protect_tags})'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Protecting tags: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Dump group object
        if options.dump:
            print(' ')
            print(project.to_json())

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return Entrypoint.Result.SUCCESS
