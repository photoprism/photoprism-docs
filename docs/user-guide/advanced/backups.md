In case you have backups enabled in your [Settings](../settings/advanced.md), PhotoPrism automatically creates YAML backup files for albums and photos.

We do this to give you full control over your data.

## Album Backups
Album backups are created for the following album types: album, folder, state, moment and month.
You find those backups inside of your `storage path` in `/albums`.

### Album backups
For each album the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Sort Order, Country, CreatedAt, UpdatedAt, Photos (UID + date the photo was added to the album)

### Folder backups
For each folder the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort order, Country, Year, Month, Day, CreatedAt, UpdatedAt

### Month backups
For each month the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, Month, CreatedAt, UpdatedAt

### State backups
For each state the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, CreatedAt, UpdatedAt

### Moment backups
For each moment the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, CreatedAt, UpdatedAt

## Photo Backups
PhotoPrism creates YAML backup files for each photo in your `sidecar path`.

The following metadata is stored:

* TakenAt + Source, UID, Type, Title + Source, Description + Source, OriginalName, TimeZone, PlaceSrc, Altitude, 
  Lat, Lng, Year, Month, Day, Iso, Exposure, FNumber, FocalLength, Quality, Favorite, Private, Keywords + Source, 
  Notes + Source, Subject + Source, Artist + Source, Copyright + Source, License + Source, CreatedAt, UpdatedAt, EditedAt, DeletedAt (Archived)

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

