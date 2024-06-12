
<a name="4.0.3"></a>
## [4.0.3](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/4.0.2...4.0.3) (2024-06-11)

### Bug Fixes

* **gitlab:** fix namespace detections upon '--dry-run' executions


<a name="4.0.2"></a>
## [4.0.2](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/4.0.1...4.0.2) (2024-06-11)

### CI

* **gitlab-ci:** change commit messages to tag name
* **gitlab-ci:** use 'CI_DEFAULT_BRANCH' to access 'develop' branch
* **gitlab-ci:** support docker pull and push without remote
* **setup:** update Python package keywords hints

### Documentation

* **chglog:** add 'ci' as 'CI' configuration for 'CHANGELOG.md'


<a name="4.0.1"></a>
## [4.0.1](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/4.0.0...4.0.1) (2024-05-27)

### Bug Fixes

* **entrypoint:** resolve already existing nested subgroups check
* **gitlab:** resolve '.variables.list' on old GitLab instances


<a name="4.0.0"></a>
## [4.0.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/3.1.0...4.0.0) (2024-05-27)

### Bug Fixes

* **gitlab:** fix project import 'path_with_namespace' in dry run
* **main:** exclusive '--archive-sources' and '--delete-sources'

### Cleanups

* **entrypoint:** turn 'confirm' function into generic handler

### Documentation

* **readme:** add '--archive-sources' and '--delete-sources' examples

### Features

* **entrypoint:** identify already existing project, group, subgroup
* **entrypoint:** improve outputs logs upon delections
* **main:** show newer updates message upon incompatible arguments


<a name="3.1.0"></a>
## [3.1.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/3.0.1...3.1.0) (2024-05-17)

### Bug Fixes

* **gitlab:** restore 'import_project' file argument as BufferedReader
* **gitlab:** raise runtime error upon failed project imports

### Cleanups

* **gitlab:** ignore 'import_project' file argument typing

### Features

* **entrypoint:** implement prompt confirmation upon deletions
* **entrypoint:** implement '--archive-exports FOLDER' to keep exports
* **requirements:** prepare 'questionary' library integration


<a name="3.0.1"></a>
## [3.0.1](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/3.0.0...3.0.1) (2024-05-15)

### Bug Fixes

* **entrypoint:** resolve 'output_namespace' assertion tests


<a name="3.0.0"></a>
## [3.0.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/2.1.0...3.0.0) (2024-05-15)

### Bug Fixes

* **entrypoint:** refactor to return no error upon final actions
* **entrypoint:** use full paths instead of 'id' integer fields
* **entrypoint:** minor Python codestyle improvement
* **entrypoint:** detect if GitLab actions can continue
* **entrypoint:** enforce against missing '.description' values
* **gitlab:** accept deletion denials in 'project_reset_members'
* **gitlab:** add 'description' field to fake project in '--dry-run'
* **gitlab:** try to get real group before faking in '--dry-run'
* **gitlab:** fix 'Any' and 'Optional' typings imports
* **gitlab:** get all members in 'project_reset_members'

### CI

* **gitlab-ci:** support multiple 'METAVAR' words in 'readme' job
* **gitlab-ci:** deprecate requirements install in 'lint' job
* **gitlab-ci:** implement 'images' and use project specific images
* **gitlab-ci:** detect 'README.md' issues in 'readme' job
* **gitlab-ci:** handle optional parameters and multiline in 'readme'
* **gitlab-ci:** move 'readme' job after 'build' and local 'install'

### Features

* **entrypoint:** always flush progress output logs
* **gitlab:** automatically wait for group and project deletions
* **main:** document optional '--' positional arguments separator
* **namespaces:** migrate 'Helper' class to 'Namespaces' class

### Test

* **version:** add 'DEBUG_VERSION_FAKE' for debugging purposes


<a name="2.1.0"></a>
## [2.1.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/2.0.0...2.1.0) (2024-04-28)

### Bug Fixes

* **entrypoint:** resolve input group detection for projects
* **entrypoint:** resolve input group for single project migration

### Features

* **entrypoint:** sort groups and projects recursively
* **entrypoint:** keep description if already contains group


<a name="2.0.0"></a>
## [2.0.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/1.1.0...2.0.0) (2024-04-28)

### Bug Fixes

* **entrypoint:** safeguard group handlings for '--dry-run'
* **gitlab:** resolve '--dry-run' usage upon projects migration
* **main:** ensure GitLab token has been defined

### CI

* **gitlab-ci:** disable 'typing' mypy caching with 'MYPY_CACHE_DIR'
* **gitlab-ci:** implement 'readme' local job to update README details

### Cleanups

* **src:** ignore 'import-error' over '__init__' and '__main__'

### Code Refactoring

* **migration:** isolate project migration feature sources
* **migration:** refactor into 'entrypoint' main function
* **src:** isolate all sources under 'src/'

### Documentation

* **readme:** regenerate '--help' details in 'README.md'

### Features

* **cli:** isolate 'features/migration.py' to 'cli/entrypoint.py'
* **entrypoint:** isolate 'group' function to 'subgroup'
* **gitlab:** prepare group settings functions for future usage
* **main:** enforce 'output_group' value is always passed by CLI
* **main:** align 'RawTextHelpFormatter' to 30 chars columns
* **main:** add support for 'GITLAB_TOKEN' environment variable
* **main:** isolate CLI argument into specific sections
* **main:** limit '--help' width to terminal width or 120 chars
* **migration:** implement nested projects migration support
* **migration:** implement GitLab subgroups creation
* **migration:** implement support for input project along group
* **migration:** sort group projects in ascending 'path' order
* **settings:** change project/group descriptions color


<a name="1.1.0"></a>
## [1.1.0](https://gitlab.com/AdrianDC/gitlab-projects-migrate/compare/1.0.0...1.1.0) (2024-04-22)

### Bug Fixes

* **migration:** prevent '--set-avatar' already closed input file

### Cleanups

* **migration:** minor output flush improvements

### Features

* **migration:** implement '--overwrite' to delete and reimport


<a name="1.0.0"></a>
## 1.0.0 (2024-04-21)

### Features

* **gitlab-projects-migrate:** initial sources implementation

