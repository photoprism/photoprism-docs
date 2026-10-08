# Metadata Exports

Control over your data does not end with the [ability to create](index.md) and [restore a database](restore.md) backup. PhotoPrism also creates [human-readable YAML files](../../developer-guide/technologies/yaml.md) that let you view and restore album and photo metadata, even if you did not create a regular database backup or no longer have it.

If backups have not been disabled in the [Advanced Settings](../settings/advanced.md#backups), PhotoPrism automatically creates YAML exports for your [albums](#album-backups) and [photos](#photo-backups). Album backups are stored in the album backup directory, and photo metadata is written to your configured *sidecar* path. These files are updated when related records change.

Keep in mind that the original metadata remains in your database. Changes you make to the YAML files do not affect the user interface unless the index is later restored from those files.

## Album Backups
Album backups are created for the following album types: `album`, `folder`, `state`, `moment`, and `month`. By default, they are stored in `storage/backup/albums`. Existing legacy installations may still use `storage/albums`.

Album backup files are not affected by the [backup retention](../../getting-started/config-options.md#backup) setting, and the backup file of a deleted album you created is kept and marked as deleted. Like other YAML files, they are created with the [default file permissions](../../getting-started/config-options.md#docker-image). If they should not be readable by other users on the server, restrict access to the *storage* folder or set a stricter `PHOTOPRISM_UMASK`, such as `0077`.

### Albums
Each album YAML file stores the following metadata:

- UID, slug, type, title, location, category, description, sort order, country, creation time, update time, and photo assignments including the date each photo was added

### Folder Backups
Each folder YAML file stores the following metadata:

- UID, slug, type, title, location, category, description, filter, sort order, country, year, month, day, creation time, and update time

### Month Backups
Each month YAML file stores the following metadata:

- UID, slug, type, title, location, category, description, filter, sort order, country, year, month, creation time, and update time

### State Backups
Each state YAML file stores the following metadata:

- UID, slug, type, title, location, category, description, filter, sort order, country, creation time, and update time

### Moment Backups
Each moment YAML file stores the following metadata:

- UID, slug, type, title, location, category, description, filter, sort order, country, year, creation time, and update time

## Photo Backups
PhotoPrism creates a YAML sidecar file for each primary photo in your configured `sidecar path`.

The following metadata is stored:

- TakenAt and source, UID, type, title and source, caption and source, original name, time zone, place source, altitude, latitude, longitude, year, month, day, ISO, exposure, f-number, focal length, quality, favorite state, private state, keywords and source, notes and source, subject and source, artist and source, copyright and source, license and source, creation time, update time, edit time, and deletion state
