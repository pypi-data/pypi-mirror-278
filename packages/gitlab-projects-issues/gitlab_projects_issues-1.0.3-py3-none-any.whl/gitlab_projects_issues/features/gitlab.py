#!/usr/bin/env python3

# Modules libraries
from gitlab import Gitlab
from gitlab.v4.objects import Project

# GitLabFeature class, pylint: disable=too-many-public-methods
class GitLabFeature:

    # Members
    __gitlab: Gitlab

    # Constructor
    def __init__(self, url: str, token: str) -> None:
        self.__gitlab = Gitlab(url, private_token=token)
        self.__gitlab.auth()

    # Project
    def project(self, criteria: str) -> Project:
        return self.__gitlab.projects.get(criteria)

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)
