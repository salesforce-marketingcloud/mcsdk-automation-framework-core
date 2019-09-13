import os
from urllib import parse
import requests

repo = 'salesforce-marketingcloud/MCSDK-Automation-Framework-PHP'
url = 'https://api.travis-ci.com/repo/{repo}/requests'.format(repo=parse.quote(repo, safe=''))
base_branch = os.environ.get('TRAVIS_BRANCH')
head_branch = os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')

print('Automatic PR will be made from {base} to {head}'.format(base=base_branch, head=head_branch))

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
print(response.content)
