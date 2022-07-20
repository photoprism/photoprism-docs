# Picture Metadata

Original media and sidecar files are scanned for Exif and XMP data, as well as proprietary metadata, including Google Photos JSON. The combined information is then normalized, merged, and [enriched with additional information](#enrichment).

## Compatibility

PhotoPrism has a [built-in Exif parser](../../developer-guide/metadata/exif/index.md), a [simple XMP reader](../../developer-guide/metadata/xmp.md) and can also use [Exiftool](https://exiftool.org/) to extract metadata in various formats such as Exif, XMP and IPTC:

↪  [Supported Exif, XMP, IPTC and DCMI Tags](https://photoprism.app/kb/metadata)

!!! tldr ""
    Feel free to [submit a feature](../../developer-guide/issues.md) [or pull request](../../developer-guide/pull-requests.md) for Exif or XMP metadata that is not  supported yet.

### Metadata Updates

If you update one of these tags with another tool such as Exiftool or Digikam, PhotoPrism will read the changes the next time you index the file, provided the file's modification date has been updated.

### XMP Sidecar Files

When a field is populated with data from an XMP sidecar file, that data is the only source for the field. This means that keywords from XMP override other keywords from PhotoPrism, such as those derived from colors or folder names.

### Cloud Migration

PhotoPrism also reads metadata from Google Photos JSON and Apple XMP files:

↪ [Google Photos](../use-cases/google.md)

↪ [Apple Photos](../use-cases/apple.md)

## Enrichment

In addition to reading metadata from your original and sidecar files, PhotoPrism enriches the metadata of your photos with additional information:

- dates or keywords from folder or filenames
- keywords derived from image classification, color detection and facial recognition
- GPS information from location estimates 
- keywords derived from location details

## Export

We want you to be able to access your metadata independently of PhotoPrism and its database. That's why the indexer additionally creates [human-readable YAML sidecar files](export.md) that you can open with a text editor or other tools if needed.

!!! note ""
    PhotoPrism does not yet offer the ability to write changed metadata back to the original files to avoid eventual data loss and conflicts with third-party apps. See [GitHub Discussions](https://github.com/photoprism/photoprism/discussions/1092).
