#!/bin/bash

# Backup date
backup_date=$(date +%Y%m%d)

# Name of the PostgreSQL container
container_name="pacmann-db"

# Create new db for restoration testing purpose
docker exec -it $container_name bash -c "createdb -U postgres pacmann_restore"

# Restore the backup file inside the container
docker exec -it $container_name bash -c "pg_restore -U postgres -d pacmann_restore /home/backup-$backup_date.dump"



