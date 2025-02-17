import sys
from pathlib import Path
import zlib


def list_branches(repo_path):
    git_dir = Path(repo_path) / ".git"
    heads_dir = git_dir / "refs" / "heads"
    if not heads_dir.exists():
        print(heads_dir)
        raise ValueError("Not a valid git repository")

    for branch in heads_dir.glob("*"):
        print(branch.name)


def show_commit(repo_path, branch):
    git_dir = Path(repo_path) / ".git"
    ref_path = git_dir / "refs/heads" / branch

    if not ref_path.exists():
        raise ValueError(f"Branch {branch} not found")

    with open(ref_path, "r") as f:
        commit_sha = f.read().strip()

    obj_path = git_dir / "objects" / commit_sha[:2] / commit_sha[2:]
    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())

    header, _, body = raw.partition(b'\x00')
    return body.decode()


def show_tree(repo_path, branch):
    commit_body = show_commit(repo_path, branch)
    tree_line = (next(line for line in commit_body.split('\n') if line.startswith('tree'))).split()[1]
    obj_path = Path(repo_path) / ".git/objects" / tree_line[:2] / tree_line[2:]

    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())

    _, _, body = raw.partition(b'\x00')

    tree_entries = []
    while body:
        mode_name, _, rest = body.partition(b'\x00')
        sha = rest[:20].hex()
        body = rest[20:]
        mode, name = mode_name.split(b' ', 1)

        if mode.decode() == '40000':
            mode = "tree"
        else: mode = "blob"

        tree_entries.append(f"{mode} {sha}    {name.decode()}")
    return "\n".join(tree_entries)


if __name__ == "__main__":
    repo_path = sys.argv[1]

    if len(sys.argv) == 2:
        list_branches(repo_path)
    elif len(sys.argv) == 3:
        print(show_commit(sys.argv[1], sys.argv[2]))
        print(show_tree(sys.argv[1], sys.argv[2]))
    else:
        print("Usage: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)
