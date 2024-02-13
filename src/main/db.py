from datetime import datetime
from flask import current_app

test_builds = [
        {
        "id": 10, 
        "date": datetime(2024, 2, 1).strftime("%d/%m/%Y, %H:%M:%S"),
        "branch": "new-branch",
        "event": "pull request",
        "status": "fail", 
        },
        {
        "id": 11, 
        "date": datetime(2024, 2, 3).strftime("%d/%m/%Y, %H:%M:%S"),
        "branch": "new-branch",
        "event": "push",
        "status": "success", 
        },
        {
        "id": 12, 
        "date": datetime(2024, 2, 5).strftime("%d/%m/%Y, %H:%M:%S"),
        "branch": "another-new-branch",
        "event": "push",
        "status": "success", 
        },
        {
        "id": 13, 
        "date": datetime(2024, 2, 7).strftime("%d/%m/%Y, %H:%M:%S"),
        "branch": "fix-wrong-type",
        "event": "pull request",
        "status": "fail", 
        },
    ]
builds = test_builds #temporary

def query_build(build_id):
    """
    Function returning a specific build from the database.
    """
    data_source = test_builds if current_app.config.get("TESTING") else builds
    return next((build for build in data_source if build["id"] == build_id), None)

def query_builds():
    """
    Function returning the list of all builds from the database.
    """
    return test_builds if current_app.config.get("TESTING") else builds