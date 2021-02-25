PhotoPrism aims to extract as much metadata from your original files as possible.

This is an ongoing task. If you are using certain standard exif or xmp fields that are not supported yet, feel free to open an issue or pull request.

PhotoPrism does not yet write back changes to EXIF or XMP (see [discussion](https://github.com/photoprism/photoprism/discussions/1092)). 

We want you to have access to your metadata independent from PhotoPrism or its database,
that's why we create human-readable [yml backups](./backups.md) with all the metadata.

## Supported EXIF tags

EXIF Tag                       | PhotoPrism DB | PhotoPrism UI | PhotoPrism YML 
:------------------------------ |:-------------------------- |:-------- |:-------
Artist                                                          | Artist        | Artist|               
Copyright                                                       | Copyright     | Copyright|           
Model / CameraModel                                             | CameraModel   | Camera|        
CameraownerName                                                 | CameraOwner   | Artist?|   
BodySerialNumber                                                | CameraSerial  |   |
LensMake                                                        | LensMake      | Lens|
LensModel                                                       | LensModel     | Lens|
ExposureTime                                                    | Exposure      | Exposure|
FNumber                                                         | FNumber       | F Number|
ApertureValue                                                   | Aperture      ||
FocalLengthIn35mmFilm / FocalLength                             | FocalLength   | Focal Lenght|
ISOSpeedRatings                                                 | Iso           | Iso|
ImageUniqueID                                                   | DocumentID    ||
PixelXDimension / ImageWidth                                    | Width         ||
PixelYDimension / ImageLength                                   | Height        ||
Orientation                                                     | Orientation   ||
DateTimeOriginal / DateTimeDigitized / CreateDate / DateTime    | TakenAt       | Local Time, UTC Time, Timezone|
Flash                                                           | Flash         ||
ImageDescription                                                | Description   | Description|
ProjectionType                                                  | Projection    ||

## Supported XMP fields

XMP Tag                       | PhotoPrism DB | PhotoPrism UI | PhotoPrism YML
:------------------------------ |:-------------------------- |:-------- |:-------
RDF.Description.Title.Alt.Li.Text       | Title         | Title |
RDF.Description.Creator.Seq.Li          | Artist        | Artist       |
RDF.Description.Description.Alt.Li.Text | Description   | Description |
RDF.Description.Rights.Alt.Li.Text      | Copyright     | Copyright |
RDF.Description.Make                    | CameraMake    | Camera|
RDF.Description.Model                   | CameraModel   | Camera |
RDF.Description.LensModel               | LensModel     | Lens |
