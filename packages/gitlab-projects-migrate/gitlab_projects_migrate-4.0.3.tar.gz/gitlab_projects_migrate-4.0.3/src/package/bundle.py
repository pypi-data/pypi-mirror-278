#!/usr/bin/env python3

# Bundle class, pylint: disable=too-few-public-methods
class Bundle:

    # Names
    NAME: str = 'gitlab-projects-migrate'

    # Details
    DESCRIPTION: str = 'Migrate GitLab projects from a GitLab group to another GitLab\'s group'

    # Sources
    REPOSITORY: str = 'https://gitlab.com/AdrianDC/gitlab-projects-migrate'

    # Releases
    RELEASE_FIRST_TIMESTAMP: int = 1579337311

    # Environment
    ENV_DEBUG_UPDATES_DAILY: str = 'DEBUG_UPDATES_DAILY'
    ENV_DEBUG_UPDATES_DISABLE: str = 'DEBUG_UPDATES_DISABLE'
    ENV_DEBUG_UPDATES_FAKE: str = 'DEBUG_UPDATES_FAKE'
    ENV_DEBUG_UPDATES_OFFLINE: str = 'DEBUG_UPDATES_OFFLINE'
    ENV_DEBUG_VERSION_FAKE: str = 'DEBUG_VERSION_FAKE'
    ENV_GITLAB_INPUT_TOKEN: str = 'GITLAB_INPUT_TOKEN'
    ENV_GITLAB_OUTPUT_TOKEN: str = 'GITLAB_OUTPUT_TOKEN'
    ENV_GITLAB_TOKEN: str = 'GITLAB_TOKEN'
