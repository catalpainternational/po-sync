# po-sync
Merge .po files from different branches

 - Requires `msgmerge`, `rsync`, `git` to be installed
 - Uses the `.sh` module (`pip install sh` or `pipenv install`)


## Usage

```
REPO=~/github/catalpainternational/openly/
NEW_TRANSLATIONS_BRANCH=akhror
WORKING_BRANCH=master

# With pipenv:
pipenv run python ./translations.py ${REPO} {NEW_TRANSLATIONS_BRANCH} ${WORKING_BRANCH}
```

Note the slash on the end of the repo. *It's important for rsync.*

## Output

In the example shell file I sync branches in my repo at `~/github/catalpainternational/openly/`
This drops my merged files back into that repo on 'master' branch.

```
josh@josh-ThinkPad-T420:~/github/catalpainternational/po-sync$ pipenv run sh ./translations.sh
2019-06-13 16:46:58,303 - translations - INFO - Git checkout /home/josh/github/catalpainternational/openly/@akhror
2019-06-13 16:46:58,321 - translations - INFO - rsync po files from /home/josh/github/catalpainternational/openly/@akhror -> /tmp/tmplc34hnj8/akhror
2019-06-13 16:46:58,351 - translations - INFO - Git checkout /home/josh/github/catalpainternational/openly/@master
2019-06-13 16:46:58,372 - translations - INFO - rsync po files from /home/josh/github/catalpainternational/openly/@master -> /tmp/tmplc34hnj8/master
2019-06-13 16:46:59,726 - translations - INFO - Git checkout /home/josh/github/catalpainternational/openly/@master
2019-06-13 16:46:59,749 - translations - INFO - Removing temp files
2019-06-13 16:46:59,749 - translations - INFO - Your repo at /home/josh/github/catalpainternational/openly/@master ought to have translations synced from /home/josh/github/catalpainternational/openly/@akhror
```
