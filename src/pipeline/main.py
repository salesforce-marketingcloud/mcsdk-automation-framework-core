import os
import requests
from mcsdk.integration.os import process

# Environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
TRAVIS_TOKEN = os.environ.get('TRAVIS_TOKEN')
TRAVIS_BUILD_DIR = os.path.dirname(os.environ.get('TRAVIS_BUILD_DIR'))
TRAVIS_BASE_BRANCH = os.environ.get('TRAVIS_BRANCH')

command = process.Command("travis login --github-token {token} && travis token".format(token=GITHUB_TOKEN))
command.run()

print(command.get_output())

# data = {
#     'request': {
#         'branch': TRAVIS_BASE_BRANCH,
#         'config': {
#             'env': {
#                 'INTEGRATION_BRANCH': os.environ.get('TRAVIS_PULL_REQUEST_BRANCH')
#             }
#         }
#     }
# }
#
# headers = {
#     'Accept': 'application/json',
#     'Content-type': 'application/json',
#     'Travis-API-Version': '3',
#     'Authorization': 'token {token}'.format(token=TRAVIS_TOKEN)
# }
#
# response = requests.get(
#     'https://api.travis-ci.com/repo/salesforce-marketingcloud/MCSDK-Automation-Framework-PHP/requests',
#     headers=headers,
#     data=data
# )
