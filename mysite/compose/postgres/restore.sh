#!/bin/bash

# #TODO: #FIXME: Get this up to date with https://github.com/pydanny/cookiecutter-django/tree/179adb4f30dfeeace03e6c5fe876e473b0737d02
# stop on errors
set -e

# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "restoring as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD

# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'usage:'
    echo '    docker-compose run postgres restore <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f $BACKUPFILE ]; then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

echo "beginning restore from $1"
echo "-------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
# Docs: https://www.postgresql.org/docs/9.6/app-dropdb.html
# IDEA: Should I use the dropdb --interactive option to issue a verification prompt before doing anything destructive?
echo "deleting old database $POSTGRES_DB"
if dropdb -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER $POSTGRES_DB
then echo "deleted $POSTGRES_DB database"
else echo "database $POSTGRES_DB does not exist, continue"
fi

# create a new database
# docs: https://www.postgresql.org/docs/9.6/app-createdb.html
# #TODO: #FIXME: -O option is for db owner, this should not use app db user
echo "creating new database $POSTGRES_DB"
createdb -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -O $POSTGRES_USER $POSTGRES_DB

# restore the database
# docs: https://www.postgresql.org/docs/9.6/app-psql.html
echo "restoring database $POSTGRES_DB"
gunzip -c $BACKUPFILE | psql -h $POSTGRES_HOST -p $POSTGRES_PORT -d $POSTGRES_DB -U $POSTGRES_USER
