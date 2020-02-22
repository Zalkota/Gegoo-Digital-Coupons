#!/bin/bash
# stop on errors
set -e

### Create a database backup.
###
### Usage:
###     $ docker-compose -f <environment>.yml (exec |run --rm) postgres backup
###
### How to copy backup from docker container to local computer:
###     $ docker cp '<postgres_container_name>':/backups/<backup_file_name> .
###     $ docker cp 'reliable_carriers_postgres_1':/backups/backup_2019_03_19T05_46_41.sql.gz .

# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "creating a backup as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD
#export PGHOST="${POSTGRES_HOST}"
#export PGPORT="${POSTGRES_PORT}"
#export PGUSER="${POSTGRES_USER}"
#export PGDATABASE="${POSTGRES_DB}"

echo "creating backup"
echo "---------------"

FILENAME=backup_$(date +'%Y_%m_%dT%H_%M_%S').sql.gz

# DOCS: https://www.postgresql.org/docs/9.6/app-pgdump.html
# -d = database name. This is equivalent to specifying dbname as the first non-option argument on the command line. If this parameter contains an = sign or starts with a valid URI prefix (postgresql:// or postgres://), it is treated as a conninfo string.
# -U = username
# -h = host
# -p = port
pg_dump -h $POSTGRES_HOST -d $POSTGRES_DB -p $POSTGRES_PORT -U $POSTGRES_USER | gzip > /backups/$FILENAME

echo "successfully created backup at /backups/$FILENAME"
