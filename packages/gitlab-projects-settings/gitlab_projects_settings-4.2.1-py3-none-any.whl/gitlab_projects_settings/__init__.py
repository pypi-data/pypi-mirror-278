# Components, pylint: disable=import-error
from gitlab_projects_settings.package.version import Version

# Version
__version__ = Version.get()
