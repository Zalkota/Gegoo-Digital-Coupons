# FROM postgres:9.3
FROM mdillon/postgis:9.6

# add backup scripts
COPY ./compose/postgres/backup.sh /usr/local/bin/backup/.backup.sh
COPY ./compose/postgres/restore.sh /usr/local/bin/restore/restore.sh
COPY ./compose/postgres/list-backups.sh /usr/local/bin/list-backups/list-backups.sh

# make them executable
RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup
