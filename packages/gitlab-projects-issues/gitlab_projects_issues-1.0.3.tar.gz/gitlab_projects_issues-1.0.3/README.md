# gitlab-projects-issues

<!-- markdownlint-disable no-inline-html -->

[![Build](https://gitlab.com/AdrianDC/gitlab-projects-issues/badges/main/pipeline.svg)](https://gitlab.com/AdrianDC/gitlab-projects-issues/-/commits/main/)

Generate GitLab project issues and milestones statistics automatically

---

## Purpose

This tool can automatically generate issues and milestones statistics,  
by analyzing project's issues, detecting milestones and assignees.

If issues without time estimations are found, `~?` will be shown before time outputs.

Milestone statistics will automatically be injected in the milestone description,  
with a markdown table of assignees, timings, progress and issues total.

The following step is required before using the tool:

- The GitLab user tokens must be created with an `api` scope (a short expiration date is recommended)

---

## Outputs

Milestones statistics will automatically be added to each milestone's description.

The following example shows how milestones statistics may look on a project:

> ## Milestone statistics - MILESTONE NAME
>
> | Assignees | Issues | Estimated | Spent | Remaining | Progress |
> |-----------|--------|-----------|-------|-----------|----------|
> | **Without assignee** | 10 | 18d | 18d | / | ██████████ 100.00% |
> | **USER ONE** | 22 | 42d | 5d | 37d | █▂▁▁▁▁▁▁▁▁ 11.90% |
> | **USER TWO** | 29 | 50d 2h | 20d 6h | 29d 4h | ████▂▁▁▁▁▁ 41.29% |
> | **USER THREE** | 7 | 9d 2h | 3d 4h | 5d 6h | ███▅▁▁▁▁▁▁ 37.84% |
> | **USER FOUR** | 6 | 21d | / | 21d | ▁▁▁▁▁▁▁▁▁▁ 0.00% |
> | _**Total**_ | _74_ | _135d 4h_ | _47d 2h_ | 93d 2h | _███▄▁▁▁▁▁▁ 34.87%_ |
>
> _Last update using gitlab-projects-issues : 2024-06-01 19:38:48 UTC_

---

## Examples

<!-- prettier-ignore-start -->

```bash
# Show the helper menu
gitlab-projects-issues

# Inject milestones statistics into milestones' description
gitlab-projects-issues --milestones-statistics 'https://gitlab.com' 'group/project'

# Inject milestones statistics into milestones' description (with default 20h time per unestimated issues)
gitlab-projects-issues --milestones-statistics --default-estimate '20' 'https://gitlab.com' 'group/project'
```

<!-- prettier-ignore-end -->

---

## Usage

<!-- prettier-ignore-start -->
<!-- readme-help-start -->

```yaml
usage: gitlab-projects-issues [-h] [--version] [--update-check] [--settings] [--set GROUP KEY VAL] [-t TOKEN] [--dump]
                              [--default-estimate DEFAULT_ESTIMATE] [--exclude-closed-issues] [--milestone MILESTONE]
                              [--milestones-statistics] [--exclude-closed-milestones] [--]
                              [gitlab] [path]

gitlab-projects-issues: Generate GitLab project issues and milestones statistics automatically

internal arguments:
  -h, --help                           # Show this help message
  --version                            # Show the current version
  --update-check                       # Check for newer package updates
  --settings                           # Show the current settings path and contents
  --set GROUP KEY VAL                  # Set settings specific 'VAL' value to [GROUP] > KEY
                                       # or unset by using 'UNSET' as 'VAL'

credentials arguments:
  -t TOKEN                             # GitLab API token (default: GITLAB_TOKEN environment)

common arguments:
  --dump                               # Dump Python objects of projects

issues arguments:
  --default-estimate DEFAULT_ESTIMATE  # Default issue time estimate if none providedin hours (default: 8)
  --exclude-closed-issues              # Exclude issues in closed state

milestones arguments:
  --milestone MILESTONE                # Use a specific milestone by name, by ID, or "None"
  --milestones-statistics              # Inject milestones statistics into milestones' description
  --exclude-closed-milestones          # Exclude milestones in closed state

positional arguments:
  --                                   # Positional arguments separator (recommended)
  gitlab                               # GitLab URL (default: https://gitlab.com)
  path                                 # GitLab project path
```

<!-- readme-help-stop -->
<!-- prettier-ignore-end -->

---

## Userspace available settings

`gitlab-projects-issues` creates a `settings.ini` configuration file in a userspace folder.

For example, it allows to disable the automated updates daily check (`[updates] > enabled`)

The `settings.ini` file location and contents can be shown with the following command:

```bash
gitlab-projects-issues --settings
```

---

## Environment available configurations

`gitlab-projects-issues` uses `colored` for colors outputs.

If colors of both outputs types do not match the terminal's theme,  
an environment variable `NO_COLOR=1` can be defined to disable colors.

---

## Dependencies

- [colored](https://pypi.org/project/colored/): Terminal colors and styles
- [python-gitlab](https://pypi.org/project/python-gitlab/): A python wrapper for the GitLab API
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
