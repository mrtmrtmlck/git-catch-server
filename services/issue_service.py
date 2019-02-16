import datetime
from itertools import chain
from string import Template

import requests
from decouple import config

from issue_catcher.models import Label, User, GithubRequestLog


def get_issues():
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'token {config("GITHUB_API_TOKEN")}'}

    query_template = Template(
        """
        {
          search(first: 100, type: ISSUE, query: "state:open is:public label:$label created:$start_time..$end_time") {
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
        request_log = GithubRequestLog.objects.filter(label=label)
        if request_log.count() > 0:
            last_request_date = request_log.latest('id').request_date
        else:
            last_request_date = datetime.datetime.now() - datetime.timedelta(hours=5)

        start_time = f'{last_request_date:%Y-%m-%dT%H:%M}'
        end_time = f'{datetime.datetime.now():%Y-%m-%dT%H:%M}'
        response = requests.post(url=url,
                                 json={'query': query_template.substitute(label=label, start_time=start_time,
                                                                          end_time=end_time)},
                                 headers=headers).json()

        if 'errors' not in response:
            GithubRequestLog.objects.update_or_create(label=label, defaults={'request_date': datetime.datetime.now()})

        issue_list.extend([item['node'] for item in response['data']['search']['edges']
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
