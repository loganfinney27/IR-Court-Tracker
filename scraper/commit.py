# scraper/commit.py
from git import Repo
import os


def commit_and_push_outputs():
    print("Starting commit and push...")

    os.environ["GIT_COMMITTER_NAME"] = "github-actions[bot]"
    os.environ["GIT_COMMITTER_EMAIL"] = "github-actions[bot]@users.noreply.github.com"

    repo = Repo(os.getcwd())
    print("Repo loaded...")

    try:
        repo.git.add("output.csv")
        repo.git.add("failed_urls.csv")
        print("Files staged.")
    except Exception as e:
        print(f"Error staging files: {e}")
        return

    if repo.is_dirty(untracked_files=True):
        try:
            repo.index.commit("Auto-update output files from GitHub Action run")
            print("Commit created.")
        except Exception as e:
            print(f"Commit failed: {e}")
            return

        try:
            if "origin" in repo.remotes:
                origin = repo.remote(name="origin")
                origin.push()
                print("Pushed to origin.")
            else:
                print("No remote named 'origin' found.")
        except Exception as e:
            print(f"Push failed: {e}")
    else:
        print("No changes to commit.")
