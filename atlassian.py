from atlassian import Jira
from atlassian import Confluence
import os
import variables

class AbsoluteAtlassian:

    def __init__(self):
        self.jira = Jira(
            url=variables.ATLASSIAN_DOMAIN,
            username=variables.ATLASSIAN_EMAIL,
            password=variables.ATLASSIAN_ACCESS_KEY
        )
        self.confluence = Confluence(
            url=variables.ATLASSIAN_DOMAIN,
            username=variables.ATLASSIAN_EMAIL,
            password=variables.ATLASSIAN_ACCESS_KEY)

    # CONFLUENCE
    def get_pages(self):
        pass

    def get_confluence_page_contents(self, page_id):
        return self.confluence.get_page_by_id(page_id, expand='body.storage', status=None, version=None)

    # JIRA
    def get_projects(self):
        return self.jira.projects()

    def get_tickets_from_project(self, project_id):
        return self.jira.get_all_project_issues(project_id, fields='*all', start=100, limit=500)