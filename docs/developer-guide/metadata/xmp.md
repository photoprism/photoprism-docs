# Adobe XMP

XMP (Extensible Metadata Platform) is the standard sidecar file format supported by Adobe Lightroom. While [YAML](../technologies/yaml.md) files might be easier to understand, read and edit for humans, using the XML-based XMP format simplifies importing metadata from Lightroom and we can leverage a documented standard. Ideally, data can be kept in sync continuously between PhotoPrism and other photo management applications.

A proof-of-concept for reading `Title`, `Copyright`, `Artist` and `Description` is implemented but full support is a lot more work, contributions welcome. One issue is proper XML parsing in Go as basic types like date and time are not supported by `xml.Unmarshaler`. GPS coordinates are not stored as float but as a string like `52,27.5814N`.

The original plan to build upon `go-xmp` didn't work out as we couldn't read many fields, so we're using pure Go for now until we find a way to get the data we need with `go-xmp`. It might be a bug and/or it's an issue with our specific XMP files.

## RAW Conversion

PhotoPrism currently supports Darktable and RawTherapee as RAW image converters (as well as Sips on macOS). Darktable fully supports XMP sidecar files, RawTherapee might only partially. However, XMP is only a "container" format, so the fields (namespaces) used there to indicate how an image should be converted (as well as other metadata) differ between Lightroom/Photoshop, Darktable, and RawTherapee.
    
In other words, just because an application generally supports XMP that doesn't mean it can use metadata created with another application or by another vendor like Adobe. If you think that's confusing, well, that's because it is. You have an open format, but you still suffer from vendor lock-in - probably not entirely unintentional on Adobe's part.

From our experience, some basic edits done with Adobe tools - such as cropping - might be preserved when you convert the same RAW image with other software like Darktable. Advanced edits, such as lens or color corrections, will likely not be applied.

[Learn more ›](../media/raw.md)

## File Samples

We would be happy to receive more [XMP files for testing](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata), either via [pull request](../pull-requests.md) or [email](https://www.photoprism.app/contact).

## Specification

- [Part 1: Data and Serialization Model](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Specification_Part_1.pdf)
- [Part 2: Standard Schemas](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Specification_Part_2.pdf)
- [Part 3: Storage in Files](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Specification_Part_3.pdf) 
- [Adobe XMP Programmers Guide](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Programmers_Guide.pdf)
- [Adobe XMP Files Plugin SDK](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Files_Plugin_SDK.pdf)
- [Adobe BSD 3-Clause License](https://dl.photoprism.app/pdf/20120101-Adobe_XMP_Specification_License.txt) and [XMP Toolkit SDK](https://github.com/adobe/XMP-Toolkit-SDK)

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
