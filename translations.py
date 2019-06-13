import argparse
import os
import shutil
from io import StringIO

from sh import git, msgmerge, rsync

import logging
import logging.config

import tempfile

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('translations')

parser = argparse.ArgumentParser()
parser.add_argument("repo", help="path to your github repo", type=str)
parser.add_argument(
    "mergefrom", help="the branch to be checked out with new translations"
)
parser.add_argument(
    "mergeto",
    help="the branch which the new translations will be merged into",
    default="master",
)
args = parser.parse_args()


tempdir = tempfile.mkdtemp()
# Some manual intervention might be required to run `./manage.py makemessages --no-wrap --no-location` on each branch to be merged

# 'Bake' some sh commands with params we use often
rsyncpo = rsync.bake(
    """-az --prune-empty-dirs --exclude=env/ --include=*/ --include=*.po --exclude=*""".split(
        " "
    )
)
gco = git.bake("checkout")
msgsort = msgmerge.bake("--sort-output", "--no-wrap")


def get_directory(branch):
    """
    Which directory do we use for a given branch
    """
    return os.path.join(tempdir, branch)

def git_checkout(repo, branch):
    """
    Switch to a directory, checkout, return
    """
    logger.info('Git checkout %s@%s', repo, branch)
    cwd = os.getcwd()
    os.chdir(repo)
    gco(branch)
    os.chdir(cwd)
    

def fetch_po_files(repo, branch):
    """
    Sync po files from a repo/branch to a directory in the working directory "branch"
    """
    dest = get_directory(branch)
    git_checkout(repo, branch)
    logger.info('rsync po files from %s@%s -> %s', repo, branch, dest)
    rsyncpo(repo, dest)
    


def put_po_files(
    repo, branch
):
    git_checkout(repo, branch)

    dest = get_directory(branch)
    # We need to "go back one step" in our temp to match up
    rsyncpo(os.path.join(dest, os.path.split(repo)[1]), repo)


def sort_po_tree(branch: str = "master"):
    directory = get_directory(branch)
    for root, _, files in os.walk(directory):
        for name in files:
            po_path = os.path.join(root, name)
            if name.endswith('~'):
                continue
            msgsort("--update", po_path, po_path)


def merge_po_trees(def_branch: str = "akhror", ref_branch: str = "master"):
    
    for root, _, files in os.walk(get_directory(def_branch)):
        for name in files:
            def_po = os.path.join(root, name)
            ref_po = os.path.join(get_directory(ref_branch), root, name)
            if def_po.endswith('~'):
                continue
            cmd = msgsort.bake("-o", ref_po + "_out.po", def_po, ref_po)
            cmd()
            # Replace the original file with the merged one
            os.remove(ref_po)
            shutil.move(ref_po + "_out.po", ref_po)

fetch_po_files(args.repo, args.mergefrom)
fetch_po_files(args.repo, args.mergeto)
sort_po_tree(args.mergefrom)
sort_po_tree(args.mergeto)
merge_po_trees(args.mergefrom, args.mergeto)
put_po_files(args.repo, args.mergeto)

logger.info('Removing temp files')
logger.info(f'Your repo at {args.repo}@{args.mergeto} ought to have translations synced from {args.repo}@{args.mergefrom}')

shutil.rmtree(tempdir)