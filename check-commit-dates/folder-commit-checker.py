# folder_commit_checker.py

import os
from datetime import datetime, timedelta, timezone
from github import Github

# GitHub token with repository access
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')

g = Github(github_token)
repo = g.get_repo(repo_name)

# Get current date in UTC timezone
current_date = datetime.now(timezone.utc)

# Get number of files in directory
def get_number_of_files_in_directory(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(name)])

# Iterate through folders
for folder in os.listdir():
    if os.path.isdir(folder):
        commits = repo.get_commits(path=folder)
        last_commit_date = commits[0].commit.committer.date
        # Ensure last_commit_date is in UTC timezone
        if last_commit_date.tzinfo is None or last_commit_date.tzinfo.utcoffset(last_commit_date) is None:
            last_commit_date = last_commit_date.replace(tzinfo=timezone.utc)
        # Check if last commit was more than 3 weeks ago
        if current_date - last_commit_date > timedelta(weeks=4 * 3):
            # Create folder link
            owner, repo_shortname = repo_name.split('/')
            folder_link = f"https://github.com/{owner}/{repo_shortname}/tree/main/{folder}"

            # Create detailed issue body
            issue_body = f"""
              The last commit in the {folder} folder is more than 3 months old. 

              - Folder: {folder}
              - Last commit date: {last_commit_date}
              - Commit details: 
                  - Author: {commits[0].commit.author.name}
                  - Email: {commits[0].commit.author.email}
                  - Message: {commits[0].commit.message}
              - Number of files in the folder: {get_number_of_files_in_directory(folder)}

              You can check the folder [here]({folder_link}).
              """
            # Create an issue
            issue = repo.create_issue(
                title=f"Please review: {folder}",
                body=issue_body
            )
            
            # Immediate assignment of labels and assignees (optional)
            issue.add_to_labels("to-be-reviewed", "outdated-folder", "auto-generated")  
            issue.add_to_assignees("Zxun2")
