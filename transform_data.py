import pandas as pd
from bs4 import BeautifulSoup
from schema import jira_project, jira_issue


def transform_jira_issue(issue):
    fields = issue['fields']
    ticket = jira_issue()
    ticket['title'] = fields['summary']
    ticket['ticket_number'] = issue['key']
    ticket['assignee'] = fields['assignee']['displayName'] if fields['assignee'] is not None else None
    ticket['reporter'] = fields['reporter']['displayName'] if fields['reporter'] is not None else None
    ticket['status'] = fields['status']['name']
    ticket['type'] = fields['issuetype']['name']
    ticket['description'] = fields['description']
    ticket['comments'] = fields['comment']
    ticket['priority'] = fields['priority']['name']
    ticket['link'] = 'https://myabsolute.atlassian.net/browse/' + issue['key']
    ticket['date_created'] = fields['created']

    return ticket


def transform_jira_project(project):
    project_obj = jira_project()
    project_obj['key'] = project['key']
    project_obj['title'] = project['name']
    project_obj['type'] = project['projectTypeKey']
    return project_obj


def transform_jira_issues_from_project(proj_issues):
    issues = []
    for issue in proj_issues:
        issues.append(transform_jira_issue(issue))
    return issues


def transform_confluence_page(resp):
    page_breakdown = convert_html(resp['body']['storage']['value'])
    page = {
        'id': resp['id'],
        'title': resp['title'],
        'link': resp['_links']['self'],
        'contents': page_breakdown['content'],
        'table': page_breakdown['table'] if 'table' in page_breakdown else None
    }
    return page


def convert_html(html_page):
    page = {}
    content = []
    data = []
    list_header = []
    soup = BeautifulSoup(html_page, 'html.parser')
    header = soup.find_all("table")[0].find("tr")

    if header:
        for items in header:
            try:
                list_header.append(items.get_text())
            except:
                continue

        # get table data
        html_data = soup.find_all("table")[0].find_all("tr")[1:]

        for element in html_data:
            sub_data = []
            for sub_element in element:
                try:
                    sub_data.append(sub_element.get_text())
                except:
                    continue
            data.append(sub_data)

        data_frame = pd.DataFrame(data=data, columns=list_header)
        content.append('table')
        page['table'] = data_frame
    page['content'] = content
    return page
