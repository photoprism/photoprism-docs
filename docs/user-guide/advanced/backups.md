## Backup Command

PhotoPrism automatically creates the album and photo backup YAML files.
If you want to update album backups or create a database backup you can use the backup command:

`docker-compose exec photoprism photoprism backup -a --albums-path PATH -i --index-path PATH [FILENAME]`

* -a = create album backups
* --albums-path = optional, path where album backups will be stored
* -i = create database backup
* --index-path = optional, path for the database backup
* -f = overwrite existing backup files
* A custom index sql backup FILENAME may be passed as first argument. Use - for stdout.

