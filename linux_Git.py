#!/usr/bin/env python3
import os
import requests
import base64
from getpass import getpass

# GitHub API URL
GITHUB_API_URL = "https://api.github.com"

# Function to get the GitHub token
def get_github_token():
    token = getpass("Enter your GitHub Personal Access Token: ")
    return token

# Function to get the GitHub headers
def get_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

# Function to initialize a repository
def init_repo(token, username, repo_name):
    url = f"{GITHUB_API_URL}/user/repos"
    payload = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(url, json=payload, headers=get_headers(token))
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
    else:
        print(f"Failed to create repository: {response.json()}")

# Function to add a file to the repository
def add_file(token, username, repo_name, file_path):
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")
    filename = os.path.basename(file_path)
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/contents/{filename}"
    payload = {
        "message": f"Add {filename}",
        "content": content
    }
    response = requests.put(url, json=payload, headers=get_headers(token))
    if response.status_code == 201:
        print(f"File '{filename}' added to repository '{repo_name}'.")
    else:
        print(f"Failed to add file: {response.json()}")

# Function to commit changes
def commit(token, username, repo_name, message):
    # Committing changes is handled during file addition in GitHub API
    print(f"Commit message: '{message}'")
    # As each file addition with a message in GitHub is equivalent to a commit

# Function to view commit logs
def log(token, username, repo_name):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/commits"
    response = requests.get(url, headers=get_headers(token))
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            print(f"Commit ID: {commit['sha']}")
            print(f"Message: {commit['commit']['message']}")
            print(f"Timestamp: {commit['commit']['author']['date']}")
            print("-" * 40)
    else:
        print(f"Failed to fetch commit logs: {response.json()}")

# Function to check repository status (list files)
def status(token, username, repo_name):
    url = f"{GITHUB_API_URL}/repos/{username}/{repo_name}/contents"
    response = requests.get(url, headers=get_headers(token))
    if response.status_code == 200:
        files = response.json()
        print(f"Files in repository '{repo_name}':")
        for file in files:
            print(f" - {file['name']}")
    else:
        print(f"Failed to fetch repository status: {response.json()}")

# Menu system
def menu():
    token = get_github_token()
    username = input("Enter your GitHub username: ")
    while True:
        print("\nGitHub Version Control System (GVCS)")
        print("1. Initialize Repository")
        print("2. Add File to Repository")
        print("3. Commit Changes")
        print("4. View Commit Logs")
        print("5. Check Repository Status")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            repo_name = input("Enter repository name: ")
            init_repo(token, username, repo_name)
        elif choice == '2':
            repo_name = input("Enter repository name: ")
            file_path = input("Enter file path to add: ")
            add_file(token, username, repo_name, file_path)
        elif choice == '3':
            repo_name = input("Enter repository name: ")
            message = input("Enter commit message: ")
            commit(token, username, repo_name, message)
        elif choice == '4':
            repo_name = input("Enter repository name: ")
            log(token, username, repo_name)
        elif choice == '5':
            repo_name = input("Enter repository name: ")
            status(token, username, repo_name)
        elif choice == '6':
            print("Exiting GVCS. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()
