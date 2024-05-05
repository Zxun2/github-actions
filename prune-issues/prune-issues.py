# prune-issues.py

import os
from github import Github

# GitHub token with repository access
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')

g = Github(github_token)
repo = g.get_repo(repo_name)

# Iterate through open issues and close them
for issue in repo.get_issues(state='open'):
    issue.edit(state='closed')
    print(f"Issue #{issue.number} closed: {issue.title}")