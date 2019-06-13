
REPO=/home/josh/github/catalpainternational/openly/
NEW_TRANSLATIONS_BRANCH=akhror
WORKING_BRANCH=master

pipenv run python ./translations.py ${REPO} ${NEW_TRANSLATIONS_BRANCH} ${WORKING_BRANCH}