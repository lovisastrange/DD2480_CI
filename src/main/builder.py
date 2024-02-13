import os
import shutil
import subprocess

class Builder:
    def __init__(self, data):
        self.data = data
        self.branch = data['branch']
        self.repo = data['repo']
        #change this to clone url from webhook, only implemented now for testing
        self.clone_url = data['clone_url']

    def clone_repo(self,repo,branch,clone_url):
        repo_path = os.path.join(os.getcwd(), repo)

        if(os.path.exists(repo_path)):
            shutil.rmtree(repo_path)

        try:
            subprocess.run(["git", "clone", "--single-branch", "--branch", branch, clone_url, repo_path], check=True)
        except subprocess.CalledProcessError:
            raise Exception(f"Failed to clone {branch}")
        
        return repo_path
    
    def build(self):
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


