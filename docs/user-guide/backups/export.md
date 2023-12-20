# Metadata Exports

Control over your data doesn't end with the [ability to create](index.md) and [restore a database](restore.md) backup.
PhotoPrism additionally provides you [with human-readable YAML files](../../developer-guide/technologies/yaml.md) that allow you to view and restore the metadata of your albums and pictures, even if you didn't create a regular database backup or have lost it.

If backups have not been disabled in the [Advanced Settings](../settings/advanced.md), metadata exports of all your albums and pictures are automatically created in your *storage* folder. They will also be updated when changes are made.

Be aware that the original data remains in your database. Any changes you make to the files therefore have no effect on it and will not become visible on the user interface, unless your database gets lost and the index is restored from the files.

## Album Backups
Album backups are created for the following album types: album, folder, state, moment and month.
You find those backups inside your `storage path` in `/albums`.

### Album Backups
For each album the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Sort Order, Country, CreatedAt, UpdatedAt, Photos (UID + date the photo was added to the album)

### Folder Backups
For each folder the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort order, Country, Year, Month, Day, CreatedAt, UpdatedAt

### Month Backups
For each month the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, Month, CreatedAt, UpdatedAt

### State Backups
For each state the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, CreatedAt, UpdatedAt

### Moment Backups
For each moment the following metadata is stored in the YAML file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, CreatedAt, UpdatedAt

## Photo Backups
PhotoPrism creates YAML backup files for each photo in your `sidecar path`.

The following metadata is stored:

* TakenAt + Source, UID, Type, Title + Source, Description + Source, OriginalName, TimeZone, PlaceSrc, Altitude, 
  Lat, Lng, Year, Month, Day, Iso, Exposure, FNumber, FocalLength, Quality, Favorite, Private, Keywords + Source, 
  Notes + Source, Subject + Source, Artist + Source, Copyright + Source, License + Source, CreatedAt, UpdatedAt, EditedAt, DeletedAt (Archived)


Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.