import os
import shutil
import subprocess

class Builder:
    def __init__(self, data):
        self.data = data
        self.branch = data['branch']
        self.repo = data['repo']
        #change this to clone url from webhook, only implemented now for testing
        self.clone_url = data['clone']

    def clone_repo(self):
        print(self.data)
        repo_path = os.path.join(os.getcwd(), self.repo)
        print(repo_path)

        try:
            subprocess.run(["git", "clone", "--single-branch", "--branch", self.branch, self.clone_url, repo_path], check=True)
        except subprocess.CalledProcessError:
            raise Exception(f"Failed to clone {self.branch}")
        
        return repo_path
    
    def build(self):
        repo_path = self.clone_repository(self.clone_url, self.branch)
        os.chdir(repo_path)

        subprocess.run(["python", "test.py"])

        # Change directory back to the original directory
        os.chdir(os.getcwd())


