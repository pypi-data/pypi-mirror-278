
<a name="4.2.1"></a>
## [4.2.1](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/4.2.0...4.2.1) (2024-06-11)

### Bug Fixes

* **gitlab:** restore support for old GitLab 13.12 instances

### CI

* **gitlab-ci:** change commit messages to tag name
* **gitlab-ci:** use 'CI_DEFAULT_BRANCH' to access 'develop' branch
* **gitlab-ci:** support docker pull and push without remote
* **setup:** update Python package keywords hints

### Documentation

* **chglog:** add 'ci' as 'CI' configuration for 'CHANGELOG.md'


<a name="4.2.0"></a>
## [4.2.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/4.1.0...4.2.0) (2024-05-27)

### Documentation

* **readme:** add 'gitlab-projects-settings' examples documentation

### Features

* **entrypoint:** improve outputs logs upon delections
* **main:** show newer updates message upon incompatible arguments


<a name="4.1.0"></a>
## [4.1.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/4.0.0...4.1.0) (2024-05-17)

### Features

* **entrypoint:** implement prompt confirmation upon deletions
* **gitlab:** isolate 'ProtectionLevels' enumeration
* **requirements:** prepare 'questionary' library integration


<a name="4.0.0"></a>
## [4.0.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/3.0.0...4.0.0) (2024-05-15)

### Bug Fixes

* **entrypoint:** refactor to return no error upon final actions
* **entrypoint:** avoid missing 'namespace_id' in 'User' responses
* **entrypoint:** use full paths instead of 'id' integer fields
* **gitlab:** disable all 'Repository' member features too
* **gitlab:** disable 'Repository' group feature after its members
* **gitlab:** accept deletion denials in 'project_reset_members'

### CI

* **gitlab-ci:** support multiple 'METAVAR' words in 'readme' job
* **gitlab-ci:** deprecate requirements install in 'lint' job
* **gitlab-ci:** implement 'images' and use project specific images
* **gitlab-ci:** detect 'README.md' issues in 'readme' job
* **gitlab-ci:** handle optional parameters and multiline in 'readme'

### Cleanups

* **entrypoint:** minor Python codestyle improvement

### Code Refactoring

* **gitlab:** optimize and centralize GitLab features handlings
* **gitlab:** isolate GitLab types to 'types/gitlab.py'
* **gitlab:** isolate 'GitLabFeature.AccessLevels' constants

### Features

* **gitlab:** parse input features list and accept similar texts
* **gitlab:** prepare future access levels in 'project_reset_features'
* **gitlab:** isolate GitLab project features enumeration
* **gitlab:** automatically wait for group and project deletions
* **main:** document optional '--' positional arguments separator

### Test

* **version:** add 'DEBUG_VERSION_FAKE' for debugging purposes


<a name="3.0.0"></a>
## [3.0.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.1.0...3.0.0) (2024-05-06)

### Bug Fixes

* **entrypoint:** resolve support for private user namespaces
* **entrypoint:** detect if GitLab actions can continue
* **entrypoint:** enforce against missing '.description' values
* **gitlab:** enforce 'group_delete' usage in '--dry-run' mode
* **gitlab:** delay groups deletion by 10s and projects by 5s
* **gitlab:** get all branches and tags upon 'list()' calls
* **gitlab:** get all members in 'project_reset_members'

### CI

* **gitlab-ci:** move 'readme' job after 'build' and local 'install'

### Cleanups

* **gitlab:** minor comments changes in 'project_reset_features'

### Features

* **entrypoint:** preserve main group description if exists
* **entrypoint:** always flush progress output logs
* **gitlab:** detect multiple branches to keep 'Merge requests'
* **gitlab:** detect 'Token Access' usage for 'CI/CD' features
* **namespaces:** migrate 'Helper' class to 'Namespaces' class


<a name="2.1.0"></a>
## [2.1.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.2...2.1.0) (2024-04-28)

### Bug Fixes

* **entrypoint:** fix project '--update-description' logs output

### Features

* **entrypoint:** sort groups and projects recursively
* **entrypoint:** keep description if already contains group


<a name="2.0.2"></a>
## [2.0.2](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.1...2.0.2) (2024-04-28)

### CI

* **gitlab-ci:** disable 'typing' mypy caching with 'MYPY_CACHE_DIR'

### Documentation

* **readme:** document GitLab tokens' creation instructions

### Features

* **main:** limit '--help' width to terminal width or 120 chars


<a name="2.0.1"></a>
## [2.0.1](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.0...2.0.1) (2024-04-28)

### Bug Fixes

* **entrypoint:** fix description updates faulty descriptions


<a name="2.0.0"></a>
## [2.0.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.1.0...2.0.0) (2024-04-27)

### Bug Fixes

* **gitlab:** enforce '--dry-run' usage and improve Python codestyle
* **settings:** apply 'subgroup' feature to subgroup groups

### CI

* **gitlab-ci:** implement 'readme' local job to update README details

### Cleanups

* **gitlab:** minor Python codestyle improvements
* **settings:** minor Python codestyle improvements
* **src:** ignore 'import-error' over '__init__' and '__main__'

### Code Refactoring

* **entrypoint:** minor Python codestyle improvements
* **src:** isolate all sources under 'src/'

### Documentation

* **readme:** regenerate '--help' details in 'README.md'

### Features

* **cli:** isolate 'features/settings.py' to 'cli/entrypoint.py'
* **main:** align 'RawTextHelpFormatter' to 30 chars columns
* **main:** change '--set-description' metavar to 'TEXT'
* **settings:** change project/group descriptions color


<a name="1.1.0"></a>
## [1.1.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.0.1...1.1.0) (2024-04-25)

### Code Refactoring

* **settings:** minor functions codestyle improvement

### Features

* **main:** rename '--avoid-*' parameters to '--exclude-*'


<a name="1.0.1"></a>
## [1.0.1](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.0.0...1.0.1) (2024-04-24)

### Documentation

* **setup:** fix PyPI 'gitlab-projects-settings' documentation


<a name="1.0.0"></a>
## 1.0.0 (2024-04-24)

### Features

* **gitlab-projects-settings:** initial sources implementation

