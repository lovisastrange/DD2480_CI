from unittest.mock import patch
import pytest
from src.main.builder import Builder
import os

def test_clone_repo():
    #Input: A mock dictionary containing repository information, including repository URL, branch, and commit.
    #Verifies that the clone_repo method correctly calls subprocess.run with the appropriate arguments
    #when cloning a repository from GitHub.
    data = {
        "repo": "https://github.com/user/repo.git",
        "clone_url": "https://github.com/user/repo.git",
        "commit": "123abc",
        "branch": "main"
    }
    builder = Builder(data)
    repo_path = os.path.join(os.getcwd(), "repository", builder.repo)

    with patch('subprocess.run') as mock_run:
        # Call the clone_repo method
        builder.clone_repo(data["repo"],data["branch"],data["clone_url"])
        
        # Assert that subprocess.run was called with the correct arguments
        mock_run.assert_called_with(
            ["git", "clone", "--single-branch", "--branch", "main", data["clone_url"], f"{repo_path}"],check=True)

if __name__ == "__main__":
    pytest.main([__file__])
