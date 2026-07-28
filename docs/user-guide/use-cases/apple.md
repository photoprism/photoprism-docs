# Migrate from Apple Photos #

## Transfer Files ##

1. Select the files or albums you want to export
2. Click *File > Export > Export Unmodified Original For Photos*
3. Select *Export IPTC as XMP*
4. Click *Export*
5. Move the exported files/folders to your *originals* or *import* directory and start indexing or importing

## Metadata ##

**Apple saves the following information in its XMP files:**

- Title
- Caption
- TakenAt Date
- Keywords (include people)
- GPS information

**The following metadata is read by PhotoPrism from the exported XMP files for each photo during indexing:**

- Title
- Caption
- TakenAt Date
- Keywords
- GPS information

Coordinates from an XMP file take precedence over the position embedded in the picture itself, so
exported photos appear in the right location in [*Places*](../organize/places.md) after indexing.
[Learn more ›](../library/metadata.md#xmp-sidecar-files)

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
