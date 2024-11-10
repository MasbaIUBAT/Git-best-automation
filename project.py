import os
import shutil
import subprocess

# GitHub personal access token
GITHUB_TOKEN = "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"

# List of GitHub repository URLs and the specific paths within the repo where index.php should go
repos = [
    {
        "repo_url": "https://github.com/MasbaIUBAT/Django-CRUD",  # Main repository URL
        "target_folder": "templates"  # Folder inside the repository where index.php will be copied
    },
    {
        "repo_url": "https://github.com/MasbaIUBAT/DRF_angular",  # Main repository URL
        "target_folder": "static/images"  # Folder inside the repository where index.php will be copied
    },
]

# Path to the local index.php file you want to push
index_file_path = r'C:\Users\NEPTUNE TECH\Desktop\Python-projectscript\index.php'

# Commit message
commit_message = "Add index.php file"

# Temporary folder to clone repositories
temp_folder = 'temp_repos'

# Ensure the temporary folder exists
os.makedirs(temp_folder, exist_ok=True)

def push_file_to_github(repo_url, target_folder):
    # Extract the repository name from the URL
    repo_name = repo_url.split("/")[-1]
    repo_path = os.path.join(temp_folder, repo_name)
    target_path_in_repo = os.path.join(repo_path, target_folder)

    try:
        # Clone the repository into the temporary folder
        subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
        print(f"Cloned repository {repo_url} into {repo_path}")

        # Ensure target folder exists in the cloned repository
        os.makedirs(target_path_in_repo, exist_ok=True)
        print(f"Created target path: {target_path_in_repo}")

        # Check if the index.php file exists before copying
        if os.path.exists(index_file_path):
            # Copy the index.php file to the target directory in the repository
            shutil.copy(index_file_path, target_path_in_repo)
            print(f"Copied index.php to {target_path_in_repo}")
        else:
            print(f"index.php file not found at {index_file_path}. Skipping.")

        # Change to the repository directory
        os.chdir(repo_path)

        # Git add, commit, and push
        subprocess.run(['git', 'add', os.path.join(target_folder, 'index.php')], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)

        # Push with GitHub token for authentication
        subprocess.run(['git', 'push', f'https://{GITHUB_TOKEN}@github.com/{repo_url.split("github.com/")[1]}.git'], check=True)

        print(f"Successfully pushed index.php to {repo_url} in {target_folder}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing {repo_url}: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Path not found.")
    finally:
        # Change back to the root directory and delete the cloned repo if it exists
        os.chdir('..')
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            print(f"Removed temporary repository folder: {repo_path}")
        else:
            print(f"Temporary folder {repo_path} does not exist, so it was not removed.")

# Run the script for each repository URL and target folder
for repo in repos:
    push_file_to_github(repo["repo_url"], repo["target_folder"])

# Clean up the temporary folder if it still exists
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)
    print(f"Removed temporary folder: {temp_folder}")
else:
    print(f"Temporary folder {temp_folder} does not exist.")
