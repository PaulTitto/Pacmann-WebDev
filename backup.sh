#!/bin/bash


# Backup date
backup_date=$(date +%Y%m%d)

docker exec -it pacmann-db bash -c "pg_dump -U postgres -W -Fc pacmann > home/backup-$backup_date.dump"
docker cp pacmann-db:/home/backup-$backup_date.dump /mnt/d/Dev/Dokcer/backup/

# Permission to run in crontab
chmod +x backup.sh