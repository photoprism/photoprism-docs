# Migrate from Google Photos #

It's possible to seamlessly migrate your photos from Google Photos to PhotoPrism.

In order to get your original resolution images and all associated metadata (such as geolocation information),
we have to use [Google Takeout](https://takeout.google.com/).

## Transfer Files ##

1. Go to https://takeout.google.com/
1. Click `Deselect all` then check only `Google Photos`.
1. Trigger the *export* of your Google Photos Data.
1. Depending on the number of photos, it can take a few days for your data to be exported
1. *Download* your data and extract all archives into to your *originals directory*
    - the folder should include the photos themselves, alongside json files for each of the photos
1. Start [*indexing*](../library/originals.md)

## Metadata ##

**Google Takeout exports the following:**

| Data Type | Description | Format |
|:--|:--|:--|
|Photos|Unedited and edited photos contained in each album.|Original format/PNG/JPG/WEBP|
|Videos|Videos contained in each album.|Original format/MP4|
|Album metadata|Data associated with each album, such as title or description.|JSON|
|Photo metadata|Data associated with each photo or video, such as creation time or comments.|JSON|

The format exported from Google Photos depends on the [quality chosen](https://photos.google.com/settings)
when uploaded to Google Photos; 'High' or 'Original'.

**Metadata is read by PhotoPrism from the exported JSON files for each photo.
The following fields are saved:**

- Title
- Description
- Number of Views
- Geolocation Info (lat/long)
- Date/Time Taken
- Date/Time Created
- Date/Time Updated

!!! note ""
    Google Photos albums won't be imported yet as we're trying to find a way to deal with 
    auto-generated albums users may not want to import.
