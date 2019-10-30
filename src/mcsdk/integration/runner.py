import re
from ..git.client import RepoClient
from ..integration.open_api_spec_validator import *
from bootstrap import *


def __push_branches(sdk_repo, base_branch, integration_branch, using_pr_branch=False):
    """
    The function performs the necessary logic to push the required branches to the remote

    Parameters
    ----------
         sdk_repo : RepoClient
         base_branch : str
         integration_branch : str
         using_pr_branch : bool

     Returns
     -------
    int
        Execution status code: 0 success, 255 failure
    """

    # Using version branch to do the build
    if not using_pr_branch:
        if sdk_repo.push('origin', base_branch, True) != 0:
            print("Could not push branch {branch} to remote!".format(branch=base_branch))
            return 255

    if sdk_repo.push('origin', integration_branch, True) != 0:
        print("Could not push branch {branch} to remote!".format(branch=integration_branch))
        return 255

    return 0


def run(config, code_generator, code_setup=None, code_integration=None):
    """
    Runs the integration

    Parameters
    ----------
        config : dict
        code_generator : mcsdk.code.codebase.AbstractGenerator
        code_setup : mcsdk.code.codebase.AbstractCodeSetup
        code_integration : mcsdk.code.codebase.AbstractCodeIntegration

    Returns
    -------
    None

    """
    # Vars for the integration run
    repo_core_owner = config['repos']['core']['owner']
    repo_core_name = config['repos']['core']['name']
    repo_core_dir = config['repos']['core']['dir']

    repo_sdk_owner = config['repos']['sdk']['owner']
    repo_sdk_name = config['repos']['sdk']['name']
    repo_sdk_dir = config['repos']['sdk']['dir']

    # The build process should never run for non-release branches (like 'feature/' or 'hotfix/')
    if not re.search("^[0-9]+.0$", TRAVIS_BASE_BRANCH):
        print('The base branch is not for a release version. No need to build / trigger anything!')
        exit(0)

    pr_branch = str(os.environ.get('TRAVIS_PULL_REQUEST_BRANCH'))
    base_branch = TRAVIS_BASE_BRANCH
    integration_branch = 'ci/' + base_branch
    using_pr_branch = False

    print("Travis PR branch: " + pr_branch)

    # Cloning the CORE repository in order to have access to swagger
    core_repo = RepoClient(TRAVIS_REPO_OWNER_DIR, GITHUB_TOKEN, repo_core_owner, repo_core_name, repo_core_dir)
    clone_status_code = core_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_core_dir):
        print('Could not clone repository')
        exit(255)

    if core_repo.fetch() != 0 or core_repo.checkout(TRAVIS_HEAD_BRANCH) != 0:
        exit(255)

    # Cloning the SDK repo
    sdk_repo = RepoClient(TRAVIS_REPO_OWNER_DIR, GITHUB_TOKEN, repo_sdk_owner, repo_sdk_name, repo_sdk_dir)
    clone_status_code = sdk_repo.clone()

    # Check if repo folder exists or the clone just failed
    if 0 != clone_status_code and not os.path.isdir(repo_sdk_dir):
        print('Could not clone repository')
        exit(255)

    if len(pr_branch) and sdk_repo.branch_exists(pr_branch):
        using_pr_branch = True
        if sdk_repo.checkout(pr_branch) != 0:
            print("Could not checkout the PR branch for the SDK {pr_branch}".format(pr_branch=pr_branch))
            exit(255)
    elif sdk_repo.checkout(base_branch) != 0:
        print("Could not checkout the base branch for the SDK")
        exit(255)

    if sdk_repo.checkout(integration_branch, False, True) != 0:
        print("Could not checkout the integration branch for the SDK")
        exit(255)

    # Open API spec validation
    if validate_spec() != 0:
        print('Open API spec validation failed!')
        exit(255)

    # code generation
    if code_generator.generate() != 0:
        print('Code generation failed!')
        exit(255)

    # code base operations
    if code_setup is not None and code_setup.install_dependencies() != 0:
        print('Dependencies failed to install')
        exit(255)

    if code_integration is not None and code_integration.run_tests() != 0:
        print("Unit tests failed!")
        exit(255)

    # Stage the change to the SDK repository
    if sdk_repo.stage_changes() != 0:
        print("Could not stage changes on the SDK repo")
        exit(255)

    # Commit the change to the SDK repository
    commit_status = sdk_repo.commit('Auto-update')
    if commit_status > 0:
        print("Could not commit changes on the SDK repo")
        exit(255)
    elif commit_status == 0:
        # Pushing the necessary branches on the remote
        if __push_branches(sdk_repo, base_branch, integration_branch, using_pr_branch) != 0:
            exit(255)  # Message is displayed from the function

        # Creating the PR
        if sdk_repo.make_pull_request(base_branch, integration_branch) != 0:
            print("PR creation failed!")
            exit(255)

    exit(0)
