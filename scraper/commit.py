# scraper/commit.py
from git import Repo
import os

def commit_and_push_outputs():
    repo = Repo(os.getcwd())
    repo.git.add("output.csv")
    repo.git.add("failed_urls.csv")

    if repo.is_dirty(untracked_files=True):
        repo.index.commit("Auto-update output files from GitHub Action run")
        origin = repo.remote(name="origin")
        origin.push()