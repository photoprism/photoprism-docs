## Extraction

PhotoPrism aims to extract as much metadata from your original files as possible.

This is an ongoing task. If you are using certain standard exif or xmp fields that are not supported yet, feel free to open an [issue](https://github.com/photoprism/photoprism/issues) or pull request.

### Supported Exiftool & XMP Tags

PhotoPrism uses [exiftool](https://exiftool.org/) to extract metadata from different file formats like EXIF, XMP, IPTC and more.

We additionally parse XMP.

This table gives an overview what tags from exiftool or XMP are mapped to which fields in PhotoPrism.

!!!tldr ""
    If you update one of those tags using another tool such as Exiftool or Digikam, PhotoPrism will read the changes during the next indexing. Provided the files modifyDate has been updated.

!!!attention ""
    In case a field is populated with data from xmp, the data from xmp is the single source for this field.
    Meaning e.g keywords from xmp overwrite other keywords coming from PhotoPrism such as colors or keywords derived from folder names. 

|    PhotoPrism     |   Type    |                                                                       Exiftool                                                                        |          Adobe XMP           |       DCMI       |
|--------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|------------------|
| Aperture     | decimal   | ApertureValue, Aperture                                                                                                                               |                              |                  |
| FNumber      | decimal   | FNumber                                                                                                                                               |                              |                  |
| FPS          | decimal   | VideoFrameRate, VideoAvgFrameRate                                                                                                                     |                              |                  |
| Duration     | duration  | Duration, MediaDuration, TrackDuration                                                                                                                |                              |                  |
| Flash        | flag      | FlashFired                                                                                                                                            |                              |                  |
| Keywords     | list      | Keywords                                                                                                                                              |                              |                  |
| Altitude     | number    | GlobalAltitude, GPSAltitude                                                                                                                           |                              |                  |
| FocalLength  | number    | FocalLength                                                                                                                                           |                              |                  |
| Frames       | number    | FrameCount                                                                                                                                            |                              |                  |
| Height       | number    | PixelYDimension, ImageHeight, ImageLength, ExifImageHeight, SourceImageHeight                                                                         |                              |                  |
| ImageType    | number    | HDRImageType                                                                                                                                          |                              |                  |
| Iso          | number    | ISO                                                                                                                                                   |                              |                  |
| Rotation     | number    | Rotation                                                                                                                                              |                              |                  |
| Width        | number    | PixelXDimension, ImageWidth, ExifImageWidth, SourceImageWidth                                                                                         |                              |                  |
| Artist       | text      | Artist, Creator, OwnerName, Owner                                                                                                                     | Creator                      |                  |
| CameraMake   | text      | CameraMake, Make                                                                                                                                      | Make                         |                  |
| CameraModel  | text      | CameraModel, Model                                                                                                                                    | Model                        |                  |
| CameraOwner  | text      | OwnerName                                                                                                                                             |                              |                  |
| CameraSerial | text      | SerialNumber                                                                                                                                          |                              |                  |
| Codec        | text      | CompressorID, FileType                                                                                                                                |                              |                  |
| ColorProfile | text      | ICCProfileName, ProfileDescription                                                                                                                    |                              |                  |
| Copyright    | text      | Rights, Copyright, WebStatement                                                                                                                       | Rights, Rights.Alt           |                  |
| Description  | text      | Description                                                                                                                                           | Description, Description.Alt |                  |
| DocumentID   | text      | BurstUUID, MediaGroupUUID, ImageUniqueID, OriginalDocumentID, DocumentID                                                                              |                              |                  |
| Exposure     | text      | ExposureTime, ShutterSpeedValue, ShutterSpeed, TargetExposureTime                                                                                     |                              |                  |
| FileName     | text      | FileName                                                                                                                                              |                              |                  |
| GPSLatitude  | text      | GPSLatitude                                                                                                                                           |                              |                  |
| GPSLongitude | text      | GPSLongitude                                                                                                                                          |                              |                  |
| GPSPosition  | text      | GPSPosition                                                                                                                                           |                              |                  |
| InstanceID   | text      | InstanceID, DocumentID                                                                                                                                |                              |                  |
| LensMake     | text      | LensMake                                                                                                                                              |                              |                  |
| LensModel    | text      | Lens, LensModel                                                                                                                                       | LensModel                    |                  |
| License      | text      | UsageTerms, License                                                                                                                                   |                              |                  |
| Notes        | text      | Comment                                                                                                                                               |                              |                  |
| Projection   | text      | ProjectionType                                                                                                                                        |                              |                  |
| Software     | text      | Software, HistorySoftwareAgent, ProcessingSoftware                                                                                                    |                              |                  |
| Subject      | text      | Subject, PersonInImage, ObjectName, HierarchicalSubject, CatalogSets                                                                                  | Subject                      |                  |
| Title        | text      | Title                                                                                                                                                 | dc:title                     | title, title.Alt |
| TakenAt      | timestamp | DateTimeOriginal, CreationDate, CreateDate, MediaCreateDate, ContentCreateDate, DateTimeDigitized, DateTime, SubSecDateTimeOriginal, SubSecCreateDate | DateCreated                  |                  |
| TakenAtLocal | timestamp | DateTimeOriginal, CreationDate, CreateDate, MediaCreateDate, ContentCreateDate, DateTimeDigitized, DateTime, SubSecDateTimeOriginal, SubSecCreateDate |                              |                  |
| TakenGps     | timestamp | GPSDateTime, GPSDateStamp                                                                                                                             |                              |                  |

### Migrate from other Tools
PhotoPrism also reads metadata from Google Photo's json files or Apple's xmp files.

- [Google Photos](../use-cases/google.md)
- [Apple Photos](../use-cases/apple.md)


## Enrichment
In addition to reading metadata from your original and sidecar files, PhotoPrism enriches the metadata of your photos with additional information:

- dates or keywords from folder or filenames
- keywords derived from image classification, color detection and facial recognition
- GPS information from location estimates 
- keywords derived from location details

## Export
PhotoPrism does not yet write back changes to EXIF or XMP (see [discussion](https://github.com/photoprism/photoprism/discussions/1092)).

We want you to have access to your metadata independent from PhotoPrism or its database,
that's why we create human-readable [YAML files](./export.md) with metadata you add to your files using PhotoPrism.
