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
    br_path = git_dir / "refs/heads" / branch

    if not br_path.exists():
        raise ValueError(f"Branch {branch} not found")

    with open(br_path, "r") as f:
        commit_sha = f.read().strip()

    obj_path = git_dir / "objects" / commit_sha[:2] / commit_sha[2:]
    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())

    header, _, body = raw.partition(b'\x00')
    return body.decode()


def show_tree(repo_path, branch):
    commit_body = show_commit(repo_path, branch)
    tree_line = next(line for line in commit_body.split('\n') if line.startswith('tree'))
    tree_sha = tree_line.split()[1]

    obj_path = Path(repo_path) / ".git/objects" / tree_sha[:2] / tree_sha[2:]
    with open(obj_path, "rb") as f:
        raw = zlib.decompress(f.read())

    _, _, body = raw.partition(b'\x00')

    tree_entries = []
    while body:
        mode_name, _, rest = body.partition(b'\x00')
        ob_hash = rest[:20].hex()
        body = rest[20:]
        mode, name = mode_name.split(b' ', 1)

        entry_type = "tree" if mode == b'40000' else "blob"
        tree_entries.append(f"{entry_type} {ob_hash}    {name.decode()}")

    return "\n".join(tree_entries)


def show_history(repo_path, branch):
    br_path = Path(repo_path) / ".git" / "refs/heads" / branch
    current_hash = br_path.read_text().strip()

    while current_hash:
        obj_path = Path(repo_path) / ".git/objects" / current_hash[:2] / current_hash[2:]
        with open(obj_path, "rb") as f:
            commit_body = zlib.decompress(f.read()).split(b'\x00')[1].decode()

        tree_line = (next(line for line in commit_body.split('\n') if line.startswith('tree'))).split()[1]

        print(f"TREE for commit {current_hash}")
        print(show_tree(repo_path, branch).replace(tree_line, current_hash))  # Костыль для совместимости

        parent_lines = [line for line in commit_body.split('\n') if line.startswith('parent')]
        current_hash = parent_lines[0].split()[1] if parent_lines else None


if __name__ == "__main__":
    repo_path = sys.argv[1]

    if len(sys.argv) == 2:
        list_branches(repo_path)
    elif len(sys.argv) == 3:
        branch = sys.argv[2]
        try:
            print(show_commit(repo_path, branch).strip())
            print(show_tree(repo_path, branch))
            show_history(repo_path, branch)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Expected: prog.py REPO_PATH [BRANCH]")
        sys.exit(1)
