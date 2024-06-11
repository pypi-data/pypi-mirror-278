
<a name="1.0.3"></a>
## [1.0.3](https://gitlab.com/AdrianDC/gitlab-projects-issues/compare/1.0.2...1.0.3) (2024-06-11)

### CI

* **gitlab-ci:** use 'buildah' instead of 'docker' to pull images
* **gitlab-ci:** install 'coreutils' in the deployed container image

### Documentation

* **readme:** improve milestones statistics outputs example


<a name="1.0.2"></a>
## [1.0.2](https://gitlab.com/AdrianDC/gitlab-projects-issues/compare/1.0.1...1.0.2) (2024-06-02)

### CI

* **gitlab-ci:** set '/bin/sh' as 'CMD' rather than 'ENTRYPOINT'


<a name="1.0.1"></a>
## [1.0.1](https://gitlab.com/AdrianDC/gitlab-projects-issues/compare/1.0.0...1.0.1) (2024-06-01)

### CI

* **gitlab-ci:** change commit messages to tag name

### Documentation

* **chglog:** add 'ci' as 'CI' configuration for 'CHANGELOG.md'
* **readme:** update 'README.md' for 'gitlab-projects-issues'


<a name="1.0.0"></a>
## 1.0.0 (2024-06-01)

### CI

* **gitlab-ci:** implement 'deploy:container' release container image
* **gitlab-ci:** rehost 'quay.io/buildah/stable:latest' image
* **gitlab-ci:** rehost 'docker:latest' image in 'images' job
* **gitlab-ci:** use 'CI_DEFAULT_BRANCH' to access 'develop' branch

### Features

* **gitlab-projects-issues:** initial sources implementation

