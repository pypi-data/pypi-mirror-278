# gitlab-projects-settings

<!-- markdownlint-disable no-inline-html -->

[![Build](https://gitlab.com/AdrianDC/gitlab-projects-settings/badges/main/pipeline.svg)](https://gitlab.com/AdrianDC/gitlab-projects-settings/-/commits/main/)

Configure GitLab groups and projects settings automatically

---

## Purpose

This tool can automatically configure and update the GitLab settings  
of groups, subgroups and projects, using multiple available options.

Repetitive tasks can be performed accross multiple projects at once,  
for example protecting tags and branches, or setting a new avatar recursively.

The following step is required before using the tool:

- The GitLab user tokens must be created with an `api` scope (a short expiration date is recommended)

---

## Examples

<!-- prettier-ignore-start -->

```bash
# Show the helper menu
gitlab-projects-settings

# Protect all projects' tags under a group
gitlab-projects-settings --protect-tags -- 'https://gitlab.com' 'group'

# Update all avatars and descriptions under a group
gitlab-projects-settings --set-avatar ./avatar.png --update-description 'https://gitlab.com' 'group'

# Automatically detect and reset features of projects based on usage
gitlab-projects-settings --reset-features 'https://gitlab.com' 'group/project'
```

<!-- prettier-ignore-end -->

---

## Usage

<!-- prettier-ignore-start -->
<!-- readme-help-start -->

```yaml
usage: gitlab-projects-settings [-h] [--version] [--update-check] [--settings] [--set GROUP KEY VAL] [-t TOKEN]
                                [--dry-run] [--dump] [--exclude-group] [--exclude-subgroups] [--exclude-projects]
                                [--available-features] [--reset-features [KEEP_FEATURES]]
                                [--disable-features FEATURES] [--enable-features FEATURES] [--reset-members]
                                [--set-avatar FILE] [--set-description TEXT] [--update-description]
                                [--run-housekeeping] [--archive-project | --unarchive-project] [--delete-group]
                                [--delete-project] [--protect-branches] [--protect-tags [LEVEL]] [--]
                                [gitlab] [path]

gitlab-projects-settings: Configure GitLab groups and projects settings automatically

internal arguments:
  -h, --help                        # Show this help message
  --version                         # Show the current version
  --update-check                    # Check for newer package updates
  --settings                        # Show the current settings path and contents
  --set GROUP KEY VAL               # Set settings specific 'VAL' value to [GROUP] > KEY
                                    # or unset by using 'UNSET' as 'VAL'

credentials arguments:
  -t TOKEN                          # GitLab API token (default: GITLAB_TOKEN environment)

common settings arguments:
  --dry-run                         # Enable dry run mode to check without saving
  --dump                            # Dump Python objects of groups and projects
  --exclude-group                   # Exclude parent group settings
  --exclude-subgroups               # Exclude children subgroups settings
  --exclude-projects                # Exclude children projects settings

general settings arguments:
  --available-features              # List the available GitLab project features known by the tool
  --reset-features [KEEP_FEATURES]  # Reset features of GitLab projects based on usage
                                    # (Optionally keep features separated by ",")
  --disable-features FEATURES       # List of features to disable separated by ","
  --enable-features FEATURES        # List of features to enable separated by ","
  --reset-members                   # Reset members of GitLab projects and groups
  --set-avatar FILE                 # Set avatar of GitLab projects and groups
  --set-description TEXT            # Set description of GitLab projects and groups
  --update-description              # Update description of GitLab projects and groups automatically

advanced settings arguments:
  --run-housekeeping                # Run housekeeping of project or projects GitLab in groups
  --archive-project                 # Archive project or projects in GitLab groups
  --unarchive-project               # Unarchive project or projects in GitLab groups
  --delete-group                    # Delete group or groups in GitLab groups
  --delete-project                  # Delete project or projects in GitLab groups

repository settings arguments:
  --protect-branches                # Protect branches with default master/main, develop and staging
  --protect-tags [LEVEL]            # Protect tags at level [no-one,admins,maintainers,developers] (default: no-one)

positional arguments:
  --                                # Positional arguments separator (recommended)
  gitlab                            # GitLab URL (default: https://gitlab.com)
  path                              # GitLab group, user namespace or project path
```

<!-- readme-help-stop -->
<!-- prettier-ignore-end -->

---

## Userspace available settings

`gitlab-projects-settings` creates a `settings.ini` configuration file in a userspace folder.

For example, it allows to disable the automated updates daily check (`[updates] > enabled`)

The `settings.ini` file location and contents can be shown with the following command:

```bash
gitlab-projects-settings --settings
```

---

## Environment available configurations

`gitlab-projects-settings` uses `colored` for colors outputs and `questionary` for interactive menus.

If colors of both outputs types do not match the terminal's theme,  
an environment variable `NO_COLOR=1` can be defined to disable colors.

---

## Dependencies

- [colored](https://pypi.org/project/colored/): Terminal colors and styles
- [python-gitlab](https://pypi.org/project/python-gitlab/): A python wrapper for the GitLab API
- [questionary](https://pypi.org/project/questionary/): Interactive terminal user interfaces
- [setuptools](https://pypi.org/project/setuptools/): Build and manage Python packages
- [update-checker](https://pypi.org/project/update-checker/): Check for package updates on PyPI

---

## References

- [git-chglog](https://github.com/git-chglog/git-chglog): CHANGELOG generator
- [gitlab-release](https://pypi.org/project/gitlab-release/): Utility for publishing on GitLab
- [gitlabci-local](https://pypi.org/project/gitlabci-local/): Launch .gitlab-ci.yml jobs locally
- [mypy](https://pypi.org/project/mypy/): Optional static typing for Python
- [PyPI](https://pypi.org/): The Python Package Index
- [twine](https://pypi.org/project/twine/): Utility for publishing on PyPI
