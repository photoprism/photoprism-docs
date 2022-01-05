# Exporting your data

Control of your data does not only refer to being able to restore a backup in PhotoPrism.
It also refers to providing users with multiple ways of accessing the metadata they've added to their libraries independent from the software itself.
People that don't know what to do with a database will probably not feel in control when they only get a sql file that a regular backup provides.

Because of this, PhotoPrism has handy features for exporting your metadata in a human-readable format as well as a regular database-backup.

In case you have backups enabled in your [Settings](../settings/advanced.md), PhotoPrism automatically creates [YAML](../../developer-guide/technologies/yaml.md) backup files for albums and photos.

Keep in mind that the data still resides in your database, and any changes made to the files will not be reflected in PhotoPrism.
This is comparable to doing a backup, but to a human readable format.

## Album Backups
Album backups are created for the following album types: album, folder, state, moment and month.
You find those backups inside of your `storage path` in `/albums`.

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