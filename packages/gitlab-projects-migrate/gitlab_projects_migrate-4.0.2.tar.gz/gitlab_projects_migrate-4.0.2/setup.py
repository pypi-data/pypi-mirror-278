#!/usr/bin/env python3

# Standard libraries
from typing import List

# Modules libraries
from setuptools import find_packages, setup

# Requirements
requirements: List[str] = []
with open('requirements/runtime.txt', encoding='utf8', mode='r') as f:
    requirements = [line for line in f.read().splitlines() if not line.startswith('#')]

# Long description
long_description: str = '' # pylint: disable=invalid-name
with open('README.md', encoding='utf8', mode='r') as f:
    long_description = f.read()

# Project configurations
PROJECT_AUTHOR = 'Adrian DC'
PROJECT_DESCRIPTION = 'Migrate GitLab projects from a GitLab group to another GitLab\'s group'
PROJECT_EMAIL = 'radian.dc@gmail.com'
PROJECT_KEYWORDS = 'gitlab projects migrate group project'
PROJECT_NAME = 'gitlab-projects-migrate'
PROJECT_OWNER = 'AdrianDC'
PROJECT_PACKAGE = 'gitlab_projects_migrate'
PROJECT_SCRIPTS = [
    'gitlab-projects-migrate = gitlab_projects_migrate.cli.main:main',
]

# Setup configurations
setup(
    name=PROJECT_NAME,
    use_scm_version=True,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    license='Apache License 2.0',
    description=PROJECT_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://gitlab.com/{PROJECT_OWNER}/{PROJECT_NAME}',
    project_urls={
        'Bug Reports': f'https://gitlab.com/{PROJECT_OWNER}/{PROJECT_NAME}/-/issues',
        'Changelog': f'https://gitlab.com/{PROJECT_OWNER}/{PROJECT_NAME}/blob/main/CHANGELOG.md',
        'Documentation': f'https://gitlab.com/{PROJECT_OWNER}/{PROJECT_NAME}#{PROJECT_NAME}',
        'Source': f'https://gitlab.com/{PROJECT_OWNER}/{PROJECT_NAME}',
        'Statistics': f'https://pypistats.org/packages/{PROJECT_NAME}'
    },
    packages=[
        PROJECT_PACKAGE,
    ] + [
        f'{PROJECT_PACKAGE}.{module}' for module in find_packages(
            where='src',
            exclude=['tests'],
        )
    ],
    package_dir={
        PROJECT_PACKAGE: 'src',
    },
    setup_requires=['setuptools_scm'],
    install_requires=requirements,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    keywords=PROJECT_KEYWORDS,
    python_requires='>=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    entry_points={
        'console_scripts': PROJECT_SCRIPTS,
    },
)
