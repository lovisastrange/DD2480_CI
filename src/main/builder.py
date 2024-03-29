import os
import shutil
import subprocess
import yaml
from dotenv import load_dotenv
import requests
import uuid
from .syntax_checker import Syntax_Checker
from .database import db_session
from .database import BuildHistory

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

        repo_path = os.path.join(os.getcwd(), "repository",repo)

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
        build_id = str(uuid.uuid4())

        repo_path = self.clone_repo(self.repo, self.branch, self.clone_url)
        os.chdir(repo_path)

        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        except Exception as e:
            return {
            "id": build_id,
            "repo": self.repo,
            "commit": self.data['commit'],
            "branch": self.branch,
            "test_result": "fail",
            "message": str(e),
        }

        checker = Syntax_Checker()
        checker.do_syntax_check(os.getcwd())
        first_line = checker.message.split("\n")[0]
        if first_line == "The code contains syntax errors. ":
            return {
            "id": build_id,
            "repo": self.repo,
            "commit": self.data['commit'],
            "branch": self.branch,
            "test_result": "fail",
            "message": checker.message
            }

        try:
            with open(".github/workflows/python-app.yml", 'r') as file:
                yaml_content = yaml.safe_load(file)
                commands = [step['run'] for step in yaml_content["jobs"]["build"].get('steps', []) if step.get('name') == 'Test with pytest']

            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)

        except Exception as e:
            return {
            "id": build_id,
            "repo": self.repo,
            "commit": self.data['commit'],
            "branch": self.branch,
            "test_result": "fail",
            "message": str(e)
        }

        finally:
            os.chdir("..")
            shutil.rmtree(repo_path)
            load_dotenv()
            os.environ['PYTHONPATH'] = 'src'

        return {
            "id": str(uuid.uuid4()),
            "repo": self.repo,
            "commit": self.data['commit'],
            "branch": self.branch,
            "test_result": "success"
        }
    
    def send_status(self, data, build, token):
        if build["test_result"] == "fail":
            url = f"https://api.github.com/repos/{data['owner']}/{data['repo']}/statuses/{data['commit']}"
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
            }
            payload = {
                "state": "failure",
                "description": build["message"],
                "context": "ci/build"
            }
            requests.post(url, headers=headers, json=payload)
            # add data to database
            bh=BuildHistory(branch=build["branch"], event=build["commit"], status="fail")
            db_session.add(bh)
            db_session.commit()

        else:
            url = f"https://api.github.com/repos/{data['owner']}/{data['repo']}/statuses/{data['commit']}"
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json',
            }
            payload = {
                "state": "success",
                "description": "Build successful",
                "context": "ci/build"
            }
            requests.post(url, headers=headers, json=payload)
            # add data to database
            bh=BuildHistory(branch=build["branch"], event=build["commit"], status="success")
            db_session.add(bh)
            db_session.commit()


