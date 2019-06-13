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