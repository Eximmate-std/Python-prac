import sys
from pathlib import Path
import zlib


def list_branches(repo_path):
    git_dir = Path(repo_path) / ".git"
    heads_dir = git_dir / "refs"/"heads"
    if not heads_dir.exists():
        print(heads_dir)
        raise ValueError("Not a valid git repository")
    
    for branch in heads_dir.glob("*"):
        print(branch.name)

def show_commit(repo_path, branch):
    git_dir = Path(repo_path) / ".git"
    br_path = git_dir / "refs/heads" / branch
    if not br_path.exists():
        raise ValueError(f"Branch {branch} not found")

    with open(br_path, "r") as f:
        commit_hash = f.read().strip()

    obj_path = git_dir / "objects" / commit_hash[:2] / commit_hash[2:]
    with open(obj_path, "rb") as f:
        commit = zlib.decompress(f.read())

    header, _, body = commit.partition(b'\x00')
    print(body.decode())

if __name__ == "__main__":

    repo_path = sys.argv[1]
    if len(sys.argv) == 2:
        list_branches(repo_path)
    elif len(sys.argv) == 3:
        show_commit(sys.argv[1], sys.argv[2])
    else:
        print("Usage: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)