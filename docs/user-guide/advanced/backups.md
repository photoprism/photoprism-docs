In case you have backups enabled in your [Settings](../settings/advanced.md), PhotoPrism automatically creates yml backup files for albums and photos.

We do this to give you full control over your data. 

Other services store the result of the work, you put into your library (e.g. adding tags, adding descriptions, creating albums, marking photos as favorites etc), 
in a way that is not accessible to you. Often they do not even provide you with an option to export all of this data.

We chose yml files for the following reasons:

* human-readable
* ...

## Album Backups
Album backups are created for the following album types: album, folder, state, moment and month.
You find those backups inside of your `storage path` in `/albums`.

### Album backups
For each album the following metadata is stored in the yml file:

* UID, Slug, Type, Title, Location, Category, Description, Sort Order, Country, CreatedAt, UpdatedAt, Photos (UID + date the photo was added to the album)

### Folder backups
For each folder the following metadata is stored in the yml file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort order, Country, Year, Month, Day, CreatedAt, UpdatedAt

### Month backups
For each month the following metadata is stored in the yml file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, Month, CreatedAt, UpdatedAt

### State backups
For each state the following metadata is stored in the yml file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, CreatedAt, UpdatedAt

### Moment backups
For each moment the following metadata is stored in the yml file:

* UID, Slug, Type, Title, Location, Category, Description, Filter, Sort Order, Country, Year, CreatedAt, UpdatedAt

## Photo Backups
PhotoPrism creates yml backup files for each photo in your `sidecar path`.

The following metadata is stored:

* TakenAt + Source
* UID
* Type
* Title + Source
* Description + Source
* OriginalName
* TimeZone
* PlaceSrc
* Altitude
* Lat
* Lng
* Year
* Month
* Day
* Iso
* Exposure
* FNumber
* FocalLength
* Quality
* Favorite
* Private
* Keywords + Source
* Notes + Source
* Subject + Source
* Artist + Source
* Copyright + Source
* License + Source
* CreatedAt
* UpdatedAt
* EditedAt
* DeletedAt (Archived)