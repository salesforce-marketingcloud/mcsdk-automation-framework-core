from mcsdk.git.client import RepoClient
from bootstrap import *


def run(config, code_generator, code_setup, code_integration):
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

    # TODO: update this with env
    branch_name = '1.0'
    auto_branch = branch_name + '_automation'

    # Cloning the CORE repository in order to have access to swagger
    core_repo = RepoClient(TRAVIS_BUILD_DIR, GITHUB_TOKEN, repo_core_owner, repo_core_name, repo_core_dir)
    clone_status_code = core_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_core_dir):
        print('Could not clone repository')
        exit(255)

    # if core_repo.checkout(branch_name, False, False) != 0:
    #     print("Core branch {branch} does not exist and will not be created automatically".format(branch=branch_name))
    #     exit(255)

    # Cloning the SDK repo
    sdk_repo = RepoClient(TRAVIS_BUILD_DIR, GITHUB_TOKEN, repo_sdk_owner, repo_sdk_name, repo_sdk_dir)
    clone_status_code = sdk_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_sdk_dir):
        print('Could not clone repository')
        exit(255)

    if sdk_repo.checkout(branch_name) != 0:
        print("Could not checkout the base branch for the SDK")
        exit(255)

    if sdk_repo.checkout(auto_branch) != 0:
        print("Could not checkout the integration branch for the SDK")
        exit(255)

    # code generation
    code_generator.generate()

    # code base operations
    if code_setup.install_dependencies() != 0:
        print('Dependencies failed to install')
        exit(255)

    if code_integration.run_tests() != 0:
        print("Unit tests failed")
        exit(255)

    # Finishing touches
    if sdk_repo.stage_changes() == 0 and sdk_repo.commit('Auto-update') == 0:
        # Doing the push & PR (cascaded for readability)
        if sdk_repo.push('origin', auto_branch, True) == 0:
            sdk_repo.make_pull_request(branch_name, auto_branch)

    exit(0)