PhotoPrism aims to extract as much metadata from your original files as possible.

This is an ongoing task. If you are using certain standard exif or xmp fields that are not supported yet, feel free to open an issue or pull request.

PhotoPrism does not yet write back changes to EXIF or XMP (see [discussion](https://github.com/photoprism/photoprism/discussions/1092)). 

We want you to have access to your metadata independent from PhotoPrism or its database,
that's why we create human-readable [yml backups](./backups.md) with all the metadata you add to your files using PhotoPrism.

##Supported Metadata Tags

This table gives an overview on which fields in PhotoPrism are populated with what metadata tags.

PhotoPrism | [Exiftool](https://exiftool.org/) Tag | XMP Tag
:--------------|----------- |:--------
Altitude      | GlobalAltitude                        |
Aperture      | ApertureValue                         |
Artist        | Artist / OwnerName / Creator          | RDF.Description.Creator.Seq.Li 
CameraMake    | Make / CameraMake                     | RDF.Description.Make
CameraModel   | Model / CameraModel                   | RDF.Description.Model
CameraOwner   | CameraOwnerName / OwnerName           | 
CameraSerial  | BodySerialNumber / SerialNumber       |
Codec         | CompressorID / Compression / FileType |
Copyright     | Copyright / Rights                    | RDF.Description.Rights.Alt.Li.Text
Description   | ImageDescription / Description        | RDF.Description.Description.Alt.Li.Text
DocumentID    | ImageUniqueID / OriginalDocumentID / DocumentID|
Duration      | duration / MediaDuration / TrackDuration |
Exposure      | ExposureTime                          |
Flash         | Flash                                  |
FNumber       | FNumber                               |
FocalLength   | FocalLengthIn35mmFilm / FocalLength   |
Height        | PixelYDimension / ImageLength / ImageHeight / ExifImageHeight / SourceImageHeight         |
Iso           | ISOSpeedRatings / ISO                 |
Keywords      | Keywords |
Latitude / Longitude | GPSPosition / GPSLatitude / GPSLongitude |
LensMake      | LensMake                              | 
LensModel     | LensModel / Lens                      | RDF.Description.LensModel  
Orientation   | Orientation                            |
Projection    | ProjectionType                        |
Rotation      | Rotation |
Subject       | Subject / PersonInImage / ObjectName / HierarchicalSubject / CatalogSets |
TakenAt       | DateTimeOriginal / DateTimeDigitized / CreateDate / DateTime / CreationDate / MediaCreateDate / ContentCreateDate / |
Title         |                                       | RDF.Description.Title.Alt.Li.Text
Width         | PixelXDimension / ImageWidth / ExifImageWidth / SourceImageWidth        | 

