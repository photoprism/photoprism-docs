# Metadata Support

Original media and sidecar files are scanned for Exif and XMP data, as well as proprietary metadata, including Google Photos JSON.
For this, PhotoPrism has a [built-in Exif parser](../../developer-guide/metadata/exif/index.md), a [simple XMP reader](../../developer-guide/metadata/xmp.md) for standalone `.xmp` sidecar files, and can also use [ExifTool](https://exiftool.org/) to extract metadata in various formats such as Exif, XMP, and IPTC from the media files themselves:

[View Supported Tags ›](https://www.photoprism.app/kb/metadata/)

The combined information is then normalized, merged, and [enriched with additional information](#enrichment).

!!! tldr ""
    Feel free to [submit a feature](../../developer-guide/issues.md) [or pull request](../../developer-guide/pull-requests.md) for Exif or XMP metadata that is not  supported yet.

### External Changes

If you update one of these tags with external tools such as [ExifTool](https://exiftool.org/) or Digikam, PhotoPrism reads the changes the next time it indexes the file, provided the file's modification date has been updated.

### XMP Sidecar Files

Many photo editors write their metadata to a standalone `.xmp` file next to the original, rather than into the original itself. PhotoPrism reads these sidecar files while indexing and gives their values priority: when a field is populated from an XMP sidecar, that data is the only source for the field. This means that keywords from XMP override other keywords from PhotoPrism, such as those derived from colors or folder names.

Besides the title, description, copyright, camera, lens, and exposure details, the following are read from sidecar files as well:

#### :material-map-marker: Location

GPS coordinates and altitude are read from a sidecar and take precedence over the position embedded in the image, so geotagging a photo in Darktable, digiKam, or Lightroom updates its location in [*Places*](../organize/places.md) the next time it is indexed. Coordinates written as plain decimals, in degrees/minutes/seconds, or in Adobe's degrees-and-decimal-minutes form are all understood.

#### :material-account-box: Face Regions

Names you have assigned to faces in Adobe Bridge, Lightroom, digiKam, ACDSee, or Windows can be imported as people markers instead of being entered again in PhotoPrism. This works with both standalone sidecar files and XMP embedded in the original, and must be enabled first. [Learn more ›](../organize/people.md#importing-face-regions-from-xmp)

#### :material-tag-multiple: Subject

The terms in the sidecar's `dc:subject` list — the "Keywords" panel in Adobe applications — populate the *Subject* field in the [edit dialog](../organize/edit.md), where multi-word terms are kept as they were written. They remain searchable and are matched against your existing [labels](../organize/labels.md).

For the full list of supported tags, including the associated namespaces and the ExifTool path used for XMP embedded in media files, see [Adobe XMP](../../developer-guide/metadata/xmp.md) in the developer guide.

### Cloud Migration

PhotoPrism also reads metadata from Google Photos JSON and Apple XMP files:

[Migrate from Google Photos ›](../use-cases/google.md)

[Migrate from Apple Photos ›](../use-cases/apple.md)

## Enrichment

In addition to reading metadata from your original and sidecar files, PhotoPrism enriches the metadata of your photos with additional information:

- dates or keywords from folder or filenames
- keywords derived from image classification, color detection and facial recognition
- GPS information from location estimates 
- keywords derived from location details

## Export

We want you to be able to access your metadata independently of PhotoPrism and its database. That's why the indexer additionally creates [human-readable YAML sidecar files](../backups/export.md) that you can open with a text editor or other tools if needed.

!!! note ""
    Except for the [image orientation](../organize/rotate.md), PhotoPrism does not yet offer the ability to write changed metadata back to the original files to avoid possible data loss and conflicts with third-party apps. See [GitHub Discussions](https://github.com/photoprism/photoprism/discussions/1092).
