# Components, pylint: disable=import-error
from gitlab_projects_migrate.package.version import Version

# Version
__version__ = Version.get()
