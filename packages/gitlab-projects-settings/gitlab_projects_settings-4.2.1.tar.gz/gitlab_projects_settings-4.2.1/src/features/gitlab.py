#!/usr/bin/env python3

# Standard libraries
from time import sleep
from typing import cast, List

# Modules libraries
from gitlab import Gitlab
from gitlab.exceptions import GitlabDeleteError, GitlabGetError, GitlabListError
from gitlab.v4.objects import Group, Namespace, Project, User

# Components
from ..types.gitlab import AccessLevels, ProjectFeatures, ProtectionLevels

# GitLabFeature class, pylint: disable=too-many-public-methods
class GitLabFeature:

    # Constants
    TIMEOUT_DELETION: int = 300

    # Members
    __dry_run: bool = False
    __gitlab: Gitlab

    # Constructor
    def __init__(self, url: str, token: str, dry_run: bool = False) -> None:
        self.__dry_run = dry_run
        self.__gitlab = Gitlab(url, private_token=token)
        self.__gitlab.auth()

    # Group
    def group(self, criteria: str) -> Group:
        return self.__gitlab.groups.get(criteria)

    # Group delete
    def group_delete(self, criteria: str) -> None:

        # Delete group
        if not self.__dry_run:
            group = self.group(criteria)
            group.delete()

            # Wait for deletion
            for _ in range(GitLabFeature.TIMEOUT_DELETION):
                try:
                    self.group(criteria)
                    sleep(1)
                except GitlabGetError:
                    break

    # Group reset members
    def group_reset_members(self, criteria: str) -> None:

        # Remove group members
        group = self.group(criteria)
        for member in group.members.list(get_all=True):
            if not self.__dry_run:
                group.members.delete(member.id)

        # Save group
        if not self.__dry_run:
            group.save()

    # Group set avatar
    def group_set_avatar(self, criteria: str, file: str) -> None:

        # Set group avatar
        if not self.__dry_run:
            group = self.group(criteria)
            with open(file, 'rb') as avatar:
                group.avatar = avatar

                # Save group
                group.save()

    # Group set description
    def group_set_description(self, criteria: str, description: str) -> None:

        # Set group description
        if not self.__dry_run:
            group = self.group(criteria)
            group.description = description

            # Save group
            group.save()

    # Namespace
    def namespace(self, criteria: str) -> Namespace:
        return self.__gitlab.namespaces.get(criteria)

    # Project
    def project(self, criteria: str) -> Project:
        return self.__gitlab.projects.get(criteria)

    # Project delete
    def project_delete(self, criteria: str) -> None:

        # Delete project
        project = self.project(criteria)
        if not self.__dry_run:
            project.delete()

            # Wait for deletion
            for _ in range(GitLabFeature.TIMEOUT_DELETION):
                try:
                    self.project(criteria)
                    sleep(1)
                except GitlabGetError:
                    break

    # Project protect branches
    def project_protect_branches(self, criteria: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.branches.list(get_all=True)
        except (AssertionError, GitlabListError):
            return result

        # Acquire project, branches and protected branches
        branches = [branch.name for branch in project.branches.list(get_all=True)]
        protectedbranches = [
            protectedbranch.name
            for protectedbranch in project.protectedbranches.list(get_all=True)
        ]

        # Protect main/master
        for branch in ['main', 'master']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': False
                    })
                result += [branch]

        # Protect develop
        for branch in ['develop']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': True
                    })
                result += [branch]

        # Protect staging
        for branch in ['staging']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 30,
                        'push_access_level': 30,
                        'allow_force_push': True
                    })
                result += [branch]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project available features
    @staticmethod
    def project_features_available() -> List[str]:
        return ProjectFeatures.names()

    # Project parse features
    @staticmethod
    def project_features_parse(input_string: str) -> List[str]:

        # Handle empty input
        if not input_string:
            return []

        # Parse features from input
        return [
            key # Key
            for search in input_string.split(',') # Input features
            for key in ProjectFeatures.keys() # GitLab features
            if ProjectFeatures.get(key).name.lower().startswith(search.strip().lower())
        ]

    # Project disable features
    def project_features_disable(
        self,
        criteria: str,
        features: List[str],
    ) -> List[str]:

        # Variables
        result: List[str] = []
        project = self.__gitlab.projects.get(criteria, statistics=True)

        # Iterate through features
        for key in features:
            if key in ProjectFeatures.keys():
                changed: bool = False
                feature = ProjectFeatures.get(key)

                # Disable 'access_level' feature
                for level in feature.access_level:
                    if hasattr(project, level.key) \
                            and getattr(project, level.key) != AccessLevels.DISABLED:
                        changed = True
                        setattr(
                            project,
                            level.key,
                            AccessLevels.DISABLED,
                        )

                # Disable 'enabled' feature
                for key in feature.enabled:
                    if hasattr(project, key) \
                            and getattr(project, key):
                        changed = True
                        setattr(
                            project,
                            key,
                            False,
                        )

                # Add changed feature
                if changed:
                    result.append(feature.name)

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project enable features
    def project_features_enable(
        self,
        criteria: str,
        features: List[str],
    ) -> List[str]:

        # Variables
        result: List[str] = []
        project = self.__gitlab.projects.get(criteria, statistics=True)

        # Iterate through features
        for key in features:
            if key in ProjectFeatures.keys():
                changed: bool = False
                feature = ProjectFeatures.get(key)

                # Enable 'access_level' feature
                for level in feature.access_level:
                    if hasattr(project, level.key) \
                            and getattr(project, level.key) == AccessLevels.DISABLED:
                        changed = True
                        setattr(
                            project,
                            level.key,
                            level.settings[project.visibility],
                        )

                # Enable 'enabled' feature
                for key in feature.enabled:
                    if hasattr(project, key) \
                            and not getattr(project, key):
                        changed = True
                        setattr(
                            project,
                            key,
                            True,
                        )

                # Add changed feature
                if changed:
                    result.append(feature.name)

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project reset features
    def project_features_reset(
        self,
        criteria: str,
        keep_features: List[str],
    ) -> List[str]:

        # Variables
        result: List[str] = []
        project = self.__gitlab.projects.get(criteria, statistics=True)

        # Iterate through features
        for key in ProjectFeatures.keys():
            if key not in keep_features:
                changed: bool = False
                feature = ProjectFeatures.get(key)

                # Disable 'access_level' feature
                for level in feature.access_level:
                    if changed or (hasattr(project, level.key) \
                            and getattr(project, level.key) != AccessLevels.DISABLED \
                            and not ProjectFeatures.test(self.__gitlab, project, feature.tests)):
                        changed = True
                        setattr(
                            project,
                            level.key,
                            AccessLevels.DISABLED,
                        )

                # Disable 'enabled' feature
                for key in feature.enabled:
                    if changed or (hasattr(project, key) \
                            and getattr(project, key) \
                            and not ProjectFeatures.test(self.__gitlab, project, feature.tests)):
                        changed = True
                        setattr(
                            project,
                            key,
                            False,
                        )

                # Add changed feature
                if changed:
                    result.append(feature.name)

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project protect tags, pylint: disable=too-many-branches
    def project_protect_tags(self, criteria: str, protect_level: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.tags.list(get_all=True)
        except (AssertionError, GitlabListError):
            return result

        # Prepare access level
        access_level: int
        if protect_level == ProtectionLevels.NO_ONE:
            access_level = 0
        elif protect_level == ProtectionLevels.ADMINS:
            access_level = 60
        elif protect_level == ProtectionLevels.MAINTAINERS:
            access_level = 40
        elif protect_level == ProtectionLevels.DEVELOPERS:
            access_level = 30
        else:
            raise SyntaxError(f'Unknown protection level: {access_level}')

        # Acquire protected tags
        protectedtags = [
            protectedtag.name for protectedtag in project.protectedtags.list(get_all=True)
        ]

        # Update protected tags
        for protectedtag in project.protectedtags.list(get_all=True):
            protectedtag_level = protectedtag.create_access_levels[0]['access_level']
            if protectedtag_level != 0 and (access_level == 0
                                            or protectedtag_level < access_level):
                name = protectedtag.name
                if not self.__dry_run:
                    protectedtag.delete()
                    project.protectedtags.create({
                        'name': name,
                        'create_access_level': access_level
                    })
                result += [name]

        # Protect unprotected tags
        for tag in project.tags.list(get_all=True):
            if tag.name not in protectedtags:
                if not self.__dry_run:
                    project.protectedtags.create({
                        'name': tag.name,
                        'create_access_level': access_level
                    })
                result += [tag.name]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        result.sort()
        return result

    # Project reset members
    def project_reset_members(self, criteria: str) -> None:

        # Remove project members
        if not self.__dry_run:
            project = self.project(criteria)
            for member in project.members.list(get_all=True):
                try:
                    project.members.delete(member.id)
                except GitlabDeleteError:
                    pass

            # Save project
            project.save()

    # Project run housekeeping
    def project_run_housekeeping(self, criteria: str) -> None:

        # Run project housekeeping
        if not self.__dry_run:
            project = self.project(criteria)
            project.housekeeping()

    # Project set archive
    def project_set_archive(self, criteria: str, enabled: bool) -> None:

        # Archive project
        if not self.__dry_run and enabled:
            project = self.project(criteria)
            project.archive()

        # Unarchive project
        elif not self.__dry_run:
            project = self.project(criteria)
            project.unarchive()

    # Project set avatar
    def project_set_avatar(self, criteria: str, file: str) -> None:

        # Set project avatar
        if not self.__dry_run:
            project = self.project(criteria)
            with open(file, 'rb') as avatar:
                project.avatar = avatar

                # Save project
                project.save()

    # Project set description
    def project_set_description(self, criteria: str, description: str) -> None:

        # Set project description
        if not self.__dry_run:
            project = self.project(criteria)
            project.description = description

            # Save project
            project.save()

    # User
    def user(self, criteria: str) -> User:
        users = self.__gitlab.users.list(all=True, iterator=True, username=criteria)
        for user in users:
            return cast(User, user)
        raise RuntimeError()

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)
