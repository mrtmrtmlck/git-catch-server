from itertools import chain

import requests
from string import Template
from decouple import config
from issue_catcher.models import Label, User


def get_issues():
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'token {config("GITHUB_API_TOKEN")}'}

    query_template = Template(
        """
        {
          search(first: 100, type: ISSUE, query: "state:open is:public label:$label created:2019-02-08T10:00..2019-02-08T15:00") {
            edges {
              node {
                ... on Issue {
                  id
                  title
                  url
                  createdAt
                  repository {
                    name
                    url
                    languages(first:10) {
                      edges {
                        node {
                          name
                        }
                      }
                    }
                  }
                  labels(first:10) {
                    edges {
                      node {
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }            
        """
    )

    issue_list = []
    all_labels = list(
        chain.from_iterable((label.name.replace(' ', '-'), fr'\"{label.name}\"') for label in Label.objects.all()))
    for label in all_labels:
        response = requests.post(url=url, json={'query': query_template.substitute(label=label)}, headers=headers)
        issue_list.extend([item['node'] for item in response.json()['data']['search']['edges']
                           if item['node'] and item['node'] not in issue_list])

    return issue_list


def get_issues_by_user(issues, user_id):
    user = User.objects.get(pk=user_id)
    user_labels = user.labels.values_list('name', flat=True)
    user_languages = user.languages.values_list('name', flat=True)
    user_issues = [issue for issue in issues
                   if any(label['node']['name'] in user_labels for label in issue['labels']['edges']) and
                   any(language['node']['name'] in user_languages for language in
                       issue['repository']['languages']['edges'])
                   ]

    return user_issues
