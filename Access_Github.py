from github import Github
import json

# Your GitHub Personal Access Token
token = ''

# Repository information
repo_owner = 'RoshankumarS14'
repo_name = 'streamlit-quiztube'
file_path = 'Questions.json'  # Path to the file in the repository

# Authenticate using your token
g = Github(token)

# Get the repository
repo = g.get_user(repo_owner).get_repo(repo_name)

# Get the file
file_content = repo.get_contents(file_path, ref="main")  # Change 'main' to your branch name if different

# Decode the file content from base64 and load as JSON
decoded_content = file_content.decoded_content.decode('utf-8')
json_content = json.loads(decoded_content)

# Print the loaded JSON content
print(json_content)

