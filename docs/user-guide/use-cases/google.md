# Migrate from Google Photos #

## Transfer Files ##

1. Go to [Google Takeout](https://takeout.google.com/)
2. Click `Deselect all` then check only `Google Photos`.
3. Trigger the *export* of your Google Photos Data.
4. Depending on the number of photos, it can take a few days for your data to be exported
5. *Download* your data and extract all archives into to your *originals* or *import* folder
    - the folder should include the photos themselves, alongside json files for each of the photos
6. Start [*indexing*](../library/originals.md) or [*importing*](../library/import.md)

## Metadata ##

**The following metadata is read by PhotoPrism from each photo's JSON file**

- Title
- Caption
- Geolocation Info (lat/long)
- Date/Time Taken
- Date/Time Created
- Date/Time Updated

## Transfer Albums ##

!!! note ""
    Google Photos albums won't be automatically imported yet as we're trying to find a way to deal with 
    auto-generated albums users may not want to import.

The community has created a bash script to import albums from a Google Takeout.
For more information and support, see the project page on Github:

https://github.com/inthreedee/photoprism-transfer-album

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
