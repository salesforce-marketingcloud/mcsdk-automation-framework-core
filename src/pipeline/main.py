import os
from urllib import parse
import requests

repo = 'salesforce-marketingcloud/MCSDK-Automation-Framework-PHP'
url = 'https://api.travis-ci.com/repo/{repo}/requests'.format(repo=parse.quote(repo, safe=''))

data = {
    'request': {
        'branch': os.environ.get('TRAVIS_BRANCH'),
        'config': {
            'env': {
                'INTEGRATION_BRANCH': os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')
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
