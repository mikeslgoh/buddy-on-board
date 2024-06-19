import csv
import logging

import transform_data
from absolute_atlassian import AbsoluteAtlassian
from utils import Utils

from enum import Enum

logger = logging.getLogger('main')
logger.setLevel("INFO")

demo_project_id = ['TEST']
demo_page_ids = [12345678]


class SourceType(Enum):
    JIRA = 1
    CONFLUENCE = 2


def create_test_data_jira(project_id):
    absolute_atlassian = AbsoluteAtlassian()
    jira_projects = absolute_atlassian.get_projects()
    projects = []
    for jira_project in jira_projects:
        project = transform_data.transform_jira_project(jira_project)
        projects.append(project)

        if project['key'] == project_id:
            resp = absolute_atlassian.get_tickets_from_project(project_id)
            issues = transform_data.transform_jira_issues_from_project(resp)
            filename = f"{project['title'].strip().lower().replace(' ', '_')}_issues.csv"

            with open(f"jira/{filename}", 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=issues[0].keys())
                writer.writeheader()
                writer.writerows(issues)

    with open('jira/absolute_projects.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=projects[0].keys())
        writer.writeheader()
        writer.writerows(projects)


def create_test_data_confluence(page_id):
    absolute_atlassian = AbsoluteAtlassian()
    resp = absolute_atlassian.get_confluence_page_contents(page_id)
    page = transform_data.transform_confluence_page(resp)
    filename = f"{page['title'].strip().lower().replace(' ', '_')}"
    if 'table' in page:
        page['table'].to_csv(f"confluence/{filename}_table.csv")
    f = open(f"confluence/{filename}.txt", "w")
    f.write(str(page))
    f.close()


def create_test_data(ids, source_type):
    if source_type == SourceType.CONFLUENCE:
        for id in ids:
            create_test_data_confluence(id)
    if source_type == SourceType.JIRA:
        for id in ids:
            create_test_data_jira(id)


def load_data(source_type, ids):
    create_test_data(ids=ids, source_type=source_type)
    Utils().upload_files_to_s3(source_type.name)


if __name__ == '__main__':
    load_data(SourceType.CONFLUENCE, demo_page_ids)
    load_data(SourceType.JIRA, demo_project_id)

    # for s in SourceType:
    #     Utils().clear_local_data(s.name.lower())
    # Utils().sync_knowledge_base()
    # Utils().query_agent()
