# Adobe XMP

XMP (Extensible Metadata Platform) is the standard sidecar file format supported by Adobe Lightroom. While [YAML](../technologies/yaml.md) files might be easier to understand, read and edit for humans, using the XML-based XMP format simplifies importing metadata from Lightroom and we can leverage a documented standard. Ideally, data can be kept in sync continuously between PhotoPrism and other photo management applications.

A proof-of-concept for reading `Title`, `Copyright`, `Artist` and `Description` is implemented but full support is a lot more work, contributions welcome. One issue is proper XML parsing in Go as basic types like date and time are not supported by `xml.Unmarshaler`. GPS coordinates are not stored as float but as a string like `52,27.5814N`.

The original plan to build upon `go-xmp` didn't work out as we couldn't read many fields, so we're using pure Go for now until we find a way to get the data we need with `go-xmp`. It might be a bug and/or it's an issue with our specific XMP files.

Please send more XMP files for testing ([pull request](../pull-requests.md)):

see https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata

## Specification

- [Part 1: Data and Serialization Model](https://dl.photoprism.app/pdf/20080101-Adobe_XMP_Specification_Part_1.pdf)
- [Part 2: Standard Schemas](https://dl.photoprism.app/pdf/20080101-Adobe_XMP_Specification_Part_2.pdf)
- [Part 3: Storage in Files](https://dl.photoprism.app/pdf/20080101-Adobe_XMP_Specification_Part_3.pdf) 

## Open Issues

- Experiment with Adobe Lightroom to see how it uses sidecar files. The new version doesn't seem to use XMP to automatically sync metadata anymore, probably because Adobe focuses on cloud storage. Needs further investigation.
- Create a matrix showing what fields are used/supported by which application/tool (Photoshop, Lightroom, Darktable and others, [see](../media/raw.md)
- Read http://www.exiv2.org/tags-xmp-crs.html (Camera Raw Schema)

## Released Features

- [Store metadata in the filesystem #4](https://github.com/photoprism/photoprism/issues/4)
- [Compare the quality and XMP compatibility of different RAW converters #65](https://github.com/photoprism/photoprism/issues/65)

## External Resources

- https://github.com/trimmer-io/go-xmp - A native Go SDK for the Extensible Metadata Platform (XMP)
- [XMP code in GIMP](https://gitlab.gnome.org/GNOME/gimp/tree/master/plug-ins/metadata) - Nothing beyond some comments. It was a code drop, we needed the feature, but unfortunately the original contributor left.
