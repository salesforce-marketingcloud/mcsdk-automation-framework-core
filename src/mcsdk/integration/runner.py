from mcsdk.git.client import RepoClient
from bootstrap import *


def run(config, code_generator, code_setup=None, code_integration=None):
    """
    Runs the integration

    Arguments:
        :type config: dict
        :type code_generator: mcsdk.code.generator.AbstractGenerator
        :type code_setup: mcsdk.code.codebase.AbstractCodeSetup
        :type code_integration: mcsdk.code.codebase.AbstractCodeIntegration
    """
    # Vars for the integration run
    repo_core_owner = config['repos']['core']['owner']
    repo_core_name = config['repos']['core']['name']
    repo_core_dir = config['repos']['core']['dir']

    repo_sdk_owner = config['repos']['sdk']['owner']
    repo_sdk_name = config['repos']['sdk']['name']
    repo_sdk_dir = config['repos']['sdk']['dir']

    base_branch = TRAVIS_BASE_BRANCH
    integration_branch = 'ci/' + base_branch


    # Cloning the CORE repository in order to have access to swagger
    core_repo = RepoClient(TRAVIS_REPO_OWNER_DIR, GITHUB_TOKEN, repo_core_owner, repo_core_name, repo_core_dir)
    clone_status_code = core_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_core_dir):
        print('Could not clone repository')
        exit(255)

    if core_repo.fetch() != 0 or core_repo.checkout(TRAVIS_HEAD_BRANCH, False, False) != 0:
        exit(255)

    # Cloning the SDK repo
    sdk_repo = RepoClient(TRAVIS_REPO_OWNER_DIR, GITHUB_TOKEN, repo_sdk_owner, repo_sdk_name, repo_sdk_dir)
    clone_status_code = sdk_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_sdk_dir):
        print('Could not clone repository')
        exit(255)

    if sdk_repo.checkout(base_branch, False, True) != 0:
        print("Could not checkout the base branch for the SDK")
        exit(255)

    if sdk_repo.checkout(integration_branch, False, True) != 0:
        print("Could not checkout the integration branch for the SDK")
        exit(255)

    exit(0)

    # code generation
    code_generator.generate()

    # code base operations
    if code_setup is not None and code_setup.install_dependencies() != 0:
        print('Dependencies failed to install')
        exit(255)

    if code_integration is not None and code_integration.run_tests() != 0:
        print("Unit tests failed")
        exit(255)

    # Finishing touches
    if sdk_repo.stage_changes() == 0 and sdk_repo.commit('Auto-update') == 0:
        # Pushing the created branches & creating the PR (cascaded for readability)
        if sdk_repo.push('origin', base_branch, True) == 0 and sdk_repo.push('origin', integration_branch, True) == 0:
            sdk_repo.make_pull_request(base_branch, integration_branch)

    exit(0)
