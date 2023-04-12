""" interface to git """
import subprocess


def clone(url, path):
    """clone a repo"""
    subprocess.check_call(["git", "clone", "--depth 1", url, path])


def pull(path):
    """pull a repo"""
    subprocess.check_call(["git", "pull"], cwd=path)


def push(path):
    """push a repo"""
    subprocess.check_call(["git", "push"], cwd=path)


def iterate_commits(path):
    """iterate over commits"""
    for line in subprocess.check_output(
        ["git", "log", "--pretty=format:%H"], cwd=path
    ).splitlines():
        yield line


def iterate_files(path):
    """iterate over files"""
    for line in subprocess.check_output(["git", "ls-files"], cwd=path).splitlines():
        yield str(line, "utf-8")
