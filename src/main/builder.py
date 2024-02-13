import os
import shutil
import subprocess

class Builder:
    """
     A class to clone repos from github and build the code from the repo.

    Attributes
    ----------
    data: dict
        Data retrieved from a Github webhook

    Methods
    -------
    clone_repo(repo,branch,clone_url):
        Clones the repository from the clone url specified in the webhook payload and checks out the branch
    build():
        Builds the project from the cloned github repo
    """

    def __init__(self, data):
        self.data = data
        self.branch = data['branch']
        self.repo = data['repo']
        #change this to clone url from webhook, only implemented now for testing
        self.clone_url = data['clone_url']

    def clone_repo(self,repo,branch,clone_url):
        """
        Clones the repository from the clone url specified in the webhook payload and checks out the branch

        Parameters
        ----------
        repo: str
            name of the repo from which the webhook was triggered
        branch: str
            name of the github branch
        clone_url: str
            url to clone the github repo
        """

        repo_path = os.path.join(os.getcwd(), repo)

        if(os.path.exists(repo_path)):
            shutil.rmtree(repo_path)

        try:
            subprocess.run(["git", "clone", "--single-branch", "--branch", branch, clone_url, repo_path], check=True)
        except subprocess.CalledProcessError:
            raise Exception(f"Failed to clone {branch}")
        
        return repo_path
    
    def build(self):
        """
        Changes to the directory the cloned project is stored in
        and tests the code using pytest.
        """

        repo_path = self.clone_repo(self.repo, self.branch, self.clone_url)
        os.chdir(repo_path)
        result = None

        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        except subprocess.CalledProcessError:
            raise Exception("Failed to install requirements")

        try:
            result = subprocess.run(["pytest"], capture_output=True, text=True, check=True)
            
            print(result.stdout)
        except subprocess.CalledProcessError:
            raise Exception("Build process failed")

        finally:
            shutil.rmtree(repo_path)

        os.chdir(os.getcwd())

        return {
            "repo": self.repo,
            "commit": self.data['commit'],
            "branch": self.branch,
            "test_result": result
        }


