from github import Github
import json

# Your GitHub Personal Access Token
token = ''

# Repository information
repo_owner = 'RoshankumarS14'
repo_name = 'streamlit-quiztube'
file_path = 'Questions.json'  # Path to the file in the repository

# List of lists to be written to the file
list_of_lists = [
    [1, 2, 3],
    ['a', 'b', 'c'],
    [True, False, True]
]

# Serialize the list of lists to JSON
content_json = json.dumps(list_of_lists)

# Authenticate using your token
g = Github(token)

# Get the repository
repo = g.get_user(repo_owner).get_repo(repo_name)

# Get the file
file = repo.get_contents(file_path, ref="main")  # Change 'main' to your branch name if different

# Update the file
repo.update_file(file.path, "Update file content", content_json, file.sha, branch="main")
