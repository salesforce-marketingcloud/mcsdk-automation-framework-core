import os

import requests
from requests.auth import HTTPBasicAuth

from ..integration.os.process import Command
from ..integration.os.utils import chdir


class RepoClient:
    """ The class handles the GIT processes """

    def __init__(self, root_dir, token, owner, repo, repo_dir):
        """ Git class constructor """
        self.__root_dir = root_dir
        self.__github_token = token
        self.__repo_owner = owner
        self.__repo_name = repo
        self.__repo_dir = repo_dir
        self.__repo_remote = 'origin'  # TODO: Make optional parameter

    def clone(self):
        """ Executes a git clone command on the target repository """
        chdir(self.__root_dir)

        # logging the working directory for debug
        print('----- Repo clone: -----')

        if os.path.isdir(self.__repo_dir) and os.path.isdir(os.path.join(self.__repo_dir, '.git')):
            print('Repository {repo_name} is already cloned'.format(repo_name=self.__repo_name) + '\n')
            return 0

        # Command to clone the repo
        cmd = 'git clone https://{owner}:{token}@github.com/{owner}/{repo}.git {repo_folder}'.format(
            owner=self.__repo_owner,
            token=self.__github_token,
            repo=self.__repo_name,
            repo_folder=self.__repo_dir
        )

        command = Command(cmd)
        command.run()

        if command.returned_errors():
            print('Error: ' + command.get_output())
            return 255

        print('Cloned repo {repo} to directory {dir}'.format(repo=self.__repo_name, dir=self.__repo_dir))
        return 0

    def __get_branches(self):
        """ Returns a list of current branches """
        if not os.path.isdir(self.__repo_dir):
            return ''

        chdir(self.__repo_dir)  # Go to repo dir

        command = Command('git branch --all', False)
        command.run()

        chdir(self.__root_dir)  # Go to root dir

        branches = command.get_output()
        branches = branches.split('\n')

        print("List of branches: " + '\n'.join(branches))

        return branches

    def branch_exists(self, branch):
        """ Checks if the branch exists """
        if not len(branch):
            raise ValueError('Branch name not provided')

        # Logging
        print('Searching for branch: ' + branch)

        lines = self.__get_branches()
        for line in lines:
            line = line.strip()
            for variant in ['* ' + branch, branch, 'remotes/' + self.__repo_remote + '/' + branch]:
                if len(line) == len(variant) and line == variant:
                    print('Branch found!')
                    return True

        print('Branch not found!')
        return False

    def branch_current(self):
        """ Returns the current branch """
        lines = self.__get_branches()
        for line in lines:
            if line.find('*') == 0:
                return line.lstrip('* ')

        raise RuntimeError("Could not determine current branch")

    def branch_delete(self, branch):
        """ Runs the branch delete command branch """
        if not len(branch):
            raise ValueError('Branch name not provided')

        # Logging
        print('Deleting branch `{branch}`'.format(branch=branch))

        self.checkout('master')

        chdir(self.__repo_dir)  # The checkout above changes the directory

        # Local delete
        command = Command('git branch -D {branch}'.format(branch=branch))
        command.run()
        print("Branch delete (local): " + command.get_output())

        if not command.returned_errors():
            # Remote delete
            command = Command('git push origin --delete {branch}'.format(branch=branch))
            command.run()
            print("Branch delete (remote): " + command.get_output())

        chdir(self.__root_dir)  # Get back to previous directory

        return command.returned_errors()

    def fetch(self):
        """ Runs the fetch command branch """
        chdir(self.__repo_dir)

        command = Command('git fetch --all')
        command.run()

        print("GIT fetch: " + command.get_output())

        chdir(self.__root_dir)  # Get back to previous directory

        return command.returned_errors()

    def push(self, remote, branch, new=False):
        """ Executes a git push command of the given branch """
        if not len(branch):
            raise ValueError('Branch name not provided')

        chdir(self.__repo_dir)

        # logging the working directory for debug
        print('----- Branch push: -----')
        print('Repo name: ' + self.__repo_name)
        print('Push to Branch: ' + branch)

        # Command spec
        cmd = 'git push {remote} {branch}'.format(remote=remote, branch=branch)
        if new:
            cmd = 'git push -u {remote} {branch}'.format(remote=remote, branch=branch)

        # Command to push to the repo
        command = Command(cmd)
        command.run()

        chdir(self.__root_dir)  # Get back to previous directory

        if command.returned_errors():
            print('Could not create a new branch {branch}: '.format(branch=branch) + command.get_output())
            return 255

        print('Branch {branch} has been pushed to {remote}'.format(remote=remote, branch=branch))

        return 0

    def checkout(self, branch, force=False, auto_create=False):
        """ Executes a git checkout command of the given branch """

        # logging the working directory for debug
        print('----- Branch checkout: -----')
        print('Repo name: ' + self.__repo_name)
        print('Checkout branch: ' + branch)

        current_branch = self.branch_current()
        if branch == current_branch:
            print('Already on branch `{branch}`'.format(branch=branch))
            return 0

        branch_exists = self.branch_exists(branch)

        if not auto_create and not branch_exists:
            print('Branch does not exist and will not be created')
            return 255

        chdir(self.__repo_dir)

        # Command spec
        cmd = 'git checkout{flag}{branch}'.format(
            flag=' -b ' if auto_create and not branch_exists else ' -f ' if force else ' ',
            branch=branch
        )

        # Command to checkout the repo
        command = Command(cmd)
        command.run()

        if command.returned_errors():
            if command.get_output().find('did not match any file(s) known to git') != -1:
                print('Branch does not exist. Trying to create it...\n')
                self.checkout(branch, False, True)  # Creating the branch
            else:
                print('Unknown error occurred')
                print(command.get_output())
                return 255
        else:
            print(command.get_output())
            print('Working branch: {branch}'.format(branch=self.branch_current()) + '\n')

        chdir(self.__root_dir)  # Get back to previous directory

        return 0

    def stage_changes(self):
        """ Executes a git add command on the working branch """
        print('----- Stage changes: -----')
        print('Current branch: ' + self.branch_current())

        chdir(self.__repo_dir)

        # Command to checkout the repo
        command = Command('git add --all')
        command.run()

        chdir(self.__root_dir)  # Get back to previous directory

        if command.returned_errors():
            print('Could not stage changes: ' + command.get_output())
            return 255
        else:
            print('Staged all the changes')
            print(command.get_output())

        return 0

    def commit(self, message):
        """ Executes a git commit on the working branch """
        chdir(self.__repo_dir)

        # logging the working directory for debug
        print('----- Committing changes: -----')

        # Command to checkout the repo
        command = Command('git commit -m {message}'.format(message=message))
        command.run()

        chdir(self.__root_dir)  # Get back to previous directory

        if command.returned_errors():
            print('Could not commit changes: ' + command.get_output())
            return 255
        else:
            print('Commit OK')

            output = command.get_output()
            if output.find('nothing to commit, working tree clean') != -1:
                print('There are no changes on the code, so the branch will not be pushed!')
                print(output)
                # No longer return error when no changes are detected
                return -1

        return 0

    def make_pull_request(self, base_branch, head_branch, title="Automated release"):
        """ The method creates a PR on the target repository """
        # logging the working directory for debug
        print('----- Creating a pull request: -----')

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Content-type": "application/json"
        }

        # Added the version to the title to make it easier to see
        title += ' ' + base_branch

        # Check if a PR is already present in the target branch
        response = requests.get(
            "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=self.__repo_owner, repo=self.__repo_name),
            auth=HTTPBasicAuth(self.__repo_owner, self.__github_token),
            headers=headers,
            params={"head": "{owner}:{head_branch}".format(owner=self.__repo_owner, head_branch=head_branch)}
        )

        if response.status_code != 200:
            print("Error response: " + response.content.decode("utf-8"))
            return response.status_code

        # Check if we have PR's open for the branch
        pull_requests = response.json()
        if len(pull_requests) > 0:
            for pr in pull_requests:
                if pr.get("title") == title:
                    print("Automated PR already exists")
                    return 0

        # Creating the pull request
        body = {
            "title": title,
            "body": "This release was done because the API spec may have changed",
            "head": "{owner}:{head_branch}".format(owner=self.__repo_owner, head_branch=head_branch),
            "base": base_branch
        }

        response = requests.post(
            "https://api.github.com/repos/{owner}/{repo}/pulls".format(owner=self.__repo_owner, repo=self.__repo_name),
            auth=HTTPBasicAuth(self.__repo_owner, self.__github_token),
            headers=headers,
            json=body
        )

        if response.status_code != 201:
            print("Error response: " + response.content.decode("utf-8"))
            return response.status_code

        print("Created the PR")

        return 0
