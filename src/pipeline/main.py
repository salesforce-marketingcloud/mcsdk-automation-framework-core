import os
from urllib import parse
import requests


def request_new_build(repo):
    url = 'https://api.travis-ci.com/repo/{repo}/requests'.format(repo=parse.quote(repo, safe=''))
    base_branch = os.environ.get('TRAVIS_BRANCH')
    head_branch = os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')

    print('API call for repository: ' + repo)

    data = {
        'request': {
            'branch': base_branch,
            'config': {
                'env': {
                    'BASE_BRANCH': base_branch,
                    'HEAD_BRANCH': head_branch
                }
            }
        }
    }

    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Travis-API-Version': '3',
        'Authorization': 'token {token}'.format(token=os.environ.get('TRAVIS_TOKEN'))
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=data
    )

    print(response.status_code)


# Code vars
owner = 'salesforce-marketingcloud'

repos = [
    '{owner}/mcsdk-automation-framework-csharp'.format(owner=owner),
    # '{owner}/mcsdk-automation-framework-java'.format(owner=owner),
    # '{owner}/mcsdk-automation-framework-php'.format(owner=owner),
    # '{owner}/mcsdk-automation-framework-node'.format(owner=owner)
]

# Triggering the builds
for repository in repos:
    request_new_build(repository)
