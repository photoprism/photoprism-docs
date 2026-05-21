# Adobe XMP

**Last Updated:** April 27, 2026

XMP (Extensible Metadata Platform) is an XML-based metadata container developed by Adobe. It can be embedded in common image and video formats (JPEG, HEIC, TIFF, DNG, MP4, MOV, PSD, …) and is also used as a standalone sidecar format — typically named the same as the original with an `.xmp` extension — to carry Dublin Core, IPTC, EXIF, and vendor-specific fields.

## How PhotoPrism Reads XMP

PhotoPrism has two separate code paths for XMP, and it is important to understand which one handles your files:

### Embedded XMP via ExifTool (Primary Path)

For XMP packets embedded in a media file, PhotoPrism does **not** parse the XML itself. Instead, the indexer runs [ExifTool](https://exiftool.org/) once per file and caches its output as a JSON document. ExifTool flattens EXIF, XMP, IPTC, Maker Notes, QuickTime atoms, and vendor tags into a single object; PhotoPrism then reads the values it recognizes from that JSON.

The relevant code:

- `internal/photoprism/convert_sidecar_json.go` — runs `exiftool -n -m -api LargeFileSupport -j <file>` (adds `-ee` for videos) and writes the result to the cache.
- `internal/photoprism/mediafile_meta.go` — calls `CreateExifToolJson` when the cached JSON is missing and then `ReadExifToolJson` to feed the cache into the metadata.
- `internal/meta/json_exiftool.go` — iterates the fields of `meta.Data` and, for each `meta:"..."` struct tag, assigns the first non-empty value found in the ExifTool JSON.

ExifTool normalizes tag names across groups by default, so an ExifTool JSON key such as `Description` may originate from `XMP-dc:description`, `IPTC:Caption-Abstract`, or `EXIF:ImageDescription` — whichever group ExifTool selected for that file. If you need to see the origin explicitly, pass `-g` to ExifTool (`exiftool -g -j <file>`) when debugging.

This path also covers the XMP that `exiftool` extracts from RAW, HEIC, and video containers — so **all XMP support beyond a handful of sidecar fields depends on ExifTool being enabled**. If `PHOTOPRISM_DISABLE_EXIFTOOL` is set, embedded XMP is not indexed.

### `.xmp` Sidecar Files via the Built-In Reader (Proof of Concept)

When the indexer encounters a standalone `.xmp` file (see `internal/photoprism/index_mediafile.go`, `case m.IsXMP()`), it does **not** invoke ExifTool. It parses the XML directly with the built-in reader in:

- `internal/meta/xmp.go` — entry point `meta.XMP(fileName)`; assigns a fixed set of values to `meta.Data`.
- `internal/meta/xmp_document.go` — hard-coded Go struct with `encoding/xml` tags, plus accessor methods such as `Title()`, `Description()`, and `Keywords()`.

This reader is an **initial, proof-of-concept implementation** that only recognizes a small subset of the fields the ExifTool-backed path covers. It supports only actual `.xmp` sidecar files and does **not** read XMP that is embedded in another media file.

Unlike the ExifTool-driven path — where each `Data` field lists an ordered set of acceptable keys in its `meta:"..."` struct tag and the first non-empty value wins — the direct sidecar reader has **no namespace-priority mechanism**. Each accessor in [`xmp_document.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go) looks up exactly one element (for example, `dc:title` for `Title`, `tiff:Model` for `CameraModel`, `dc:rights` for `Copyright`). The only fallbacks that currently exist are intra-element — specifically, choosing between the XMP `rdf:Alt`/`rdf:li` language-tagged value and a plain chardata value for `dc:title` and `dc:description`. The `xmp:"..."` struct tags on `meta.Data` fields *look* like a namespace-priority list but are currently only consumed by `internal/meta/report.go` for the developer field report — not by the XMP reader itself.

## Fields Extracted from XMP

The table below lists the XMP elements PhotoPrism currently consumes, their primary XMP namespace, and whether each path reads them. ExifTool-JSON keys are the default (un-grouped) names as they appear in the output of `exiftool -n -j`; PhotoPrism looks them up case-sensitively via the `meta:"..."` struct tags on `meta.Data`.

| PhotoPrism `Data` Field | XMP Namespace and Element                                                       | ExifTool JSON Key(s)                                                                  | Embedded (ExifTool) | `.xmp` Sidecar (Direct)                              |
|-------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|------------------------------------------------------|
| `Title`                 | `dc:title` (Dublin Core); also `photoshop:Headline`                             | `Title`, `Headline`                                                                   | ✓                   | ✓ `dc:title` only                                    |
| `Caption`               | `dc:description`                                                                | `Description`, `ImageDescription`, `Caption`, `Caption-Abstract`                      | ✓                   | ✓ `dc:description` only                              |
| `Artist`                | `dc:creator`; also `photoshop:AuthorsPosition`, `photoshop:OwnerName`           | `Artist`, `Creator`, `By-line`, `OwnerName`, `Owner`                                  | ✓                   | ✓ `dc:creator` only                                  |
| `Copyright`             | `dc:rights`; `xmpRights:WebStatement`                                           | `Rights`, `Copyright`, `CopyrightNotice`, `WebStatement`                              | ✓                   | ✓ `dc:rights` only                                   |
| `License`               | `xmpRights:UsageTerms`                                                          | `UsageTerms`, `License`                                                               | ✓                   | —                                                    |
| `Subject`               | `dc:subject`; `lr:hierarchicalSubject` (Lightroom); `Iptc4xmpExt:PersonInImage` | `Subject`, `HierarchicalSubject`, `PersonInImage`, `CatalogSets`, `ObjectName`        | ✓                   | —                                                    |
| `Keywords`              | `dc:subject` (aggregated); `lr:hierarchicalSubject`                             | `Keywords`                                                                            | ✓                   | ✓ `dc:subject` only                                  |
| `TakenAt`               | `xmp:CreateDate`; `photoshop:DateCreated`; `exif:DateTimeOriginal`              | `SubSecDateTimeOriginal`, `DateTimeOriginal`, `CreationDate`, `DateTimeDigitized`     | ✓                   | ✓ `photoshop:DateCreated` only                       |
| `CreatedAt`             | `xmp:CreateDate`; QuickTime `CreateDate`                                        | `SubSecCreateDate`, `CreateDate`, `MediaCreateDate`, `TrackCreateDate`                | ✓                   | —                                                    |
| `Software`              | `xmp:CreatorTool`; `xmpMM:History/softwareAgent`                                | `Software`, `CreatorTool`, `HistorySoftwareAgent`, `ProcessingSoftware`               | ✓                   | —                                                    |
| `CameraMake`            | `tiff:Make`                                                                     | `Make`, `CameraMake`                                                                  | ✓                   | ✓ `tiff:Make` only                                   |
| `CameraModel`           | `tiff:Model`; `aux:UniqueCameraModel`                                           | `Model`, `CameraModel`, `UniqueCameraModel`                                           | ✓                   | ✓ `tiff:Model` only                                  |
| `CameraSerial`          | `aux:SerialNumber`                                                              | `SerialNumber`                                                                        | ✓                   | —                                                    |
| `LensMake`              | `aux:LensMake` / `exifEX:LensMake`                                              | `LensMake`                                                                            | ✓                   | —                                                    |
| `LensModel`             | `aux:Lens` / `exifEX:LensModel`                                                 | `LensModel`, `Lens`, `LensID`                                                         | ✓                   | ✓ `<LensModel>` element (local name; not `aux:Lens`) |
| `FocalLength`           | `exif:FocalLength`, `exifEX:FocalLengthIn35mmFilm`                              | `FocalLength`, `FocalLengthIn35mmFormat`                                              | ✓                   | —                                                    |
| `Exposure`              | `exif:ExposureTime`, `exif:ShutterSpeedValue`                                   | `ExposureTime`, `ShutterSpeedValue`, `ShutterSpeed`                                   | ✓                   | —                                                    |
| `Aperture` / `FNumber`  | `exif:ApertureValue`, `exif:FNumber`                                            | `ApertureValue`, `Aperture`, `FNumber`                                                | ✓                   | —                                                    |
| `Iso`                   | `exif:ISOSpeedRatings`                                                          | `ISO`                                                                                 | ✓                   | —                                                    |
| `Flash`                 | `exif:Flash/Fired`                                                              | `FlashFired`                                                                          | ✓                   | —                                                    |
| `Rotation`              | `xmp:Rotation`; `tiff:Orientation`                                              | `Rotation`, `Orientation`                                                             | ✓                   | —                                                    |
| `Width` / `Height`      | `tiff:ImageWidth` / `ImageLength`; `exif:PixelXDimension` / `PixelYDimension`   | `ImageWidth`, `ExifImageWidth`, `PixelXDimension`, `ImageHeight`, `ExifImageHeight`   | ✓                   | —                                                    |
| `GPSLatitude`           | `exif:GPSLatitude`                                                              | `GPSLatitude`, `GPSPosition`                                                          | ✓                   | —                                                    |
| `GPSLongitude`          | `exif:GPSLongitude`                                                             | `GPSLongitude`, `GPSPosition`                                                         | ✓                   | —                                                    |
| `Altitude`              | `exif:GPSAltitude`                                                              | `GlobalAltitude`, `GPSAltitude`                                                       | ✓                   | —                                                    |
| `TakenGps`              | `exif:GPSTimeStamp` / `GPSDateStamp`                                            | `GPSDateTime`, `GPSDateStamp`                                                         | ✓                   | —                                                    |
| `Projection`            | `GPano:ProjectionType` (Google Photo Sphere)                                    | `ProjectionType`                                                                      | ✓                   | —                                                    |
| `ColorProfile`          | `photoshop:ICCProfile`                                                          | `ICCProfileName`, `ProfileDescription`                                                | ✓                   | —                                                    |
| `DocumentID`            | `xmpMM:OriginalDocumentID` / `DocumentID`; MWG `ImageUniqueID`                  | `ContentIdentifier`, `OriginalDocumentID`, `DocumentID`, `ImageUniqueID`, `BurstUUID` | ✓                   | —                                                    |
| `InstanceID`            | `xmpMM:InstanceID`                                                              | `InstanceID`                                                                          | ✓                   | —                                                    |
| `Favorite`              | Custom `http://www.fstopapp.com/xmp/ favorite` attribute (F-Stop app)           | `Favorite` (when present)                                                             | ✓ (via tag alias)   | ✓ F-Stop `favorite="1"` attr                         |
| `HasThumbEmbedded`      | `photoshop:Thumbnail`                                                           | `ThumbnailImage`, `PhotoshopThumbnail`                                                | ✓                   | —                                                    |
| `HasVideoEmbedded`      | Google Motion Photo (`GCamera:MicroVideo`), Samsung `MotionPhoto`               | `EmbeddedVideoFile`, `MotionPhoto`, `MotionPhotoVideo`, `MicroVideo`                  | ✓                   | —                                                    |

**Notes**

- The XMP element column lists the *primary* namespace mapping. Many fields are aliased across several namespaces (for example, `dc:title` ↔ `photoshop:Headline` ↔ `IPTC:Headline`) and ExifTool merges them, which is why PhotoPrism usually lists multiple ExifTool keys per field.
- The ✓ in the "`.xmp` Sidecar (Direct)" column identifies the *single* XMP element the reader actually consults — it does **not** imply that the other aliases in the middle column are tried as fallbacks. For example, if a sidecar has `photoshop:Headline` but no `dc:title`, the direct reader leaves `Title` empty even though the ExifTool path would pick `Headline` up.
- The direct reader matches XML elements by **local name**, not by XML namespace. Its struct tags in [`xmp_document.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go) are plain local names (`xml:"title"`, `xml:"Make"`, etc.), so the namespaces shown above are the conventional ones from the XMP spec — a sidecar that uses a different prefix for the same element is still read, but an entirely different element (like `photoshop:Headline` for `Title`) is not.
- The authoritative mapping for the ExifTool path lives in the `meta:"..."` struct tags on `meta.Data` in [`internal/meta/data.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/data.go). For the direct sidecar reader, the authoritative mapping is the XML struct in [`internal/meta/xmp_document.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go).
- Standalone `.xmp` sidecar fields that the XML struct parses into memory but that the current reader does not yet assign to `meta.Data` (for example `GPSLatitude`, `GPSLongitude`, `Rating`, `Rotation`, and the full EXIF block) are intentionally left as `—` above. Wiring these up is a natural next step — see "Open Issues" below.

## Sidecar Reader Limitations

The built-in `.xmp` sidecar reader is a proof-of-concept and has several known shortcomings:

- Only the fields marked as supported in the table above are applied; everything else in the sidecar is ignored, even if it is valid XMP.
- **No namespace-priority fallback.** The ExifTool path uses `meta:"A,B,C"` struct tags on `meta.Data` so that the first non-empty alias wins (for example `meta:"Artist,Creator,By-line,OwnerName,Owner"` for `Data.Artist`, or `meta:"Rights,Copyright,CopyrightNotice,WebStatement"` for `Data.Copyright`). The direct sidecar reader's accessors in [`xmp_document.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go) are hard-wired to a single XML element per field, so a sidecar that only carries `photoshop:Headline` (or only `xmpRights:WebStatement`) leaves `Title` / `Copyright` empty even though the ExifTool path would populate them. The `xmp:"..."` struct tags that already exist on `meta.Data` fields *look* like such a priority list but are currently only consumed by `internal/meta/report.go` to render the developer field report.
- It has no generic XMP/RDF parser. The [`XmpDocument` struct](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go) is a hand-written mapping of the elements observed in sample files, so sidecars that nest fields differently (for example, inside additional `rdf:Description` nodes or with non-default namespace prefixes) may not parse as expected.
- GPS coordinates are stored in XMP as strings like `52,27.5814N`. The struct fields exist but are not converted to decimal latitude/longitude — the indexer therefore never sees GPS data from `.xmp` sidecars.
- Go's `encoding/xml` does not natively unmarshal timestamps or rational numbers, so values like EXIF dates, apertures, and focal lengths would have to be parsed manually. Only `photoshop:DateCreated` is currently handled, via `txt.ParseTime`.
- The reader was originally prototyped on `trimmer-io/go-xmp`, but that library did not produce the values we needed for our sample files, so the current implementation uses `encoding/xml` directly.

Pull requests that extend the supported field set (or replace the reader with a generic RDF-aware parser) are welcome.

## RAW Conversion

PhotoPrism currently supports Darktable and RawTherapee as RAW image converters (as well as Sips on macOS). Darktable fully supports XMP sidecar files; RawTherapee only partially. XMP is a container format, so the fields (namespaces) used to describe how an image should be rendered differ between Lightroom/Photoshop, Darktable, and RawTherapee — an application that "supports XMP" in general may still be unable to interpret edits written by another vendor.

From our experience, some basic edits done with Adobe tools — such as cropping — can survive conversion with Darktable, while advanced edits like lens or color corrections usually do not.

[Learn more ›](../media/raw.md)

## Resources

### File Samples

We would be happy to receive more [XMP files for testing](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata). There are two ways to contribute:

- **Pull request** against [`internal/meta/testdata`](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata) — see the [Pull Requests](../pull-requests.md) guide. Use this for files you are clearly licensed to share publicly (files you created yourself, or files from an openly licensed corpus).
- **Email to [samples@photoprism.app](mailto:samples@photoprism.app)** — for files you cannot or would rather not commit directly. Please include the file format and the related [GitHub issue number](https://github.com/photoprism/photoprism/issues) (or other helpful reference) in the subject line, and let us know whether we have permission to upload your files to [dl.photoprism.app/samples](https://dl.photoprism.app/samples/) so other contributors can use them for regression testing.

A short note about the camera or software that produced the sidecar, which fields are relevant, and what PhotoPrism currently gets wrong about the file helps us triage quickly.

### References

- [XMP Part 1: Data and Serialization Model](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Specification_Part_1.pdf)
- [XMP Part 2: Standard Schemas](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Specification_Part_2.pdf)
- [XMP Part 3: Storage in Files](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Specification_Part_3.pdf)
- [Adobe XMP Programmers Guide](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Programmers_Guide.pdf)
- [Adobe XMP Files Plugin SDK](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Files_Plugin_SDK.pdf)
- [Adobe BSD 3-Clause License](https://dl.photoprism.app/pdf/specifications/20120101-Adobe_XMP_Specification_License.txt) and [XMP Toolkit SDK](https://github.com/adobe/XMP-Toolkit-SDK)
- [ExifTool Tag Names: XMP](https://exiftool.org/TagNames/XMP.html) — authoritative list of the XMP tags ExifTool exposes.
- [XMP code in GIMP](https://gitlab.gnome.org/GNOME/gimp/tree/master/plug-ins/metadata) — mostly comments; included here for reference.
- [Camera Raw Schema (exiv2 reference)](http://www.exiv2.org/tags-xmp-crs.html)

### XML/XMP Libraries

The following Go libraries are worth considering as replacements or additions to the existing reader. Their documented maintenance state is as of April 2026.

**XMP-Specific**

- [`evanoberholster/imagemeta`](https://github.com/evanoberholster/imagemeta) — MIT. **Actively maintained** (commits through April 2026). Broader image-metadata library with an `xmp` sub-package for sidecars and embedded XMP; decodes dates and rationals into Go types and handles nested `rdf:Description`. **Read-only**, so only a partial replacement if we also want to write sidecars.

**Generic XML / DOM (for a hand-rolled XMP Parser)**

- [`antchfx/xmlquery`](https://github.com/antchfx/xmlquery) — MIT. Actively maintained (latest commit March 2026, ~490 stars). DOM-style XML parser backed by [`antchfx/xpath`](https://github.com/antchfx/xpath) (MIT, ~740 stars, latest commit February 2026), which implements full XPath 1.0. Namespace-aware queries via `xpath.CompileWithNS(expr, nsMap)`, which is the closest off-the-shelf match for the XMP namespace-priority fallback we need: compile each priority list once (e.g. `//dc:title | //photoshop:Headline`), run it, and take the first non-empty hit. Read-only — writing sidecars back out would still need `encoding/xml` or another library.
- [`beevik/etree`](https://github.com/beevik/etree) — BSD-2-Clause. Actively maintained (latest commit August 2025, ~1.7k stars). DOM-style XML with XPath-like selectors; strong fit for namespace-priority fallback (walk once, cherry-pick `dc:title`, then `photoshop:Headline` via prefix-aware paths) and supports writing. Rational/date coercion still has to be implemented manually.
- [`subchen/go-xmldom`](https://github.com/subchen/go-xmldom) — Apache-2.0. Same niche as `etree` with a smaller community; prefer `etree` unless its XPath dialect is specifically needed.

**RDF Parsers (XMP Is RDF/XML Under the Hood)**

- [`knakk/rdf`](https://github.com/knakk/rdf) — MIT. Actively maintained (commits through March 2026). Turtle / N-Triples / RDF-XML parser that produces triples. Cleanest semantic match for XMP in theory (namespace-agnostic property lookup, `xml:lang` alternatives via language-tagged literals), but we would reconstruct XMP-specific structures ourselves and it does not write RDF/XML back.
- [`deiu/rdf2go`](https://github.com/deiu/rdf2go) — MIT. Graph API with Turtle + JSON-LD I/O; RDF/XML parsing is weaker than `knakk/rdf`.

**ExifTool Wrapper (Alternative Strategy)**

- [`barasher/go-exiftool`](https://github.com/barasher/go-exiftool) — Apache-2.0. Actively maintained (~300 stars, latest commit August 2025). Wraps the Phil Harvey `exiftool` binary. Sidesteps parsing entirely — ExifTool already resolves namespace priority, `xml:lang` alternatives, rationals, and dates. PhotoPrism already shells out to `exiftool` for the embedded-XMP path (see [`convert_sidecar_json.go`](https://github.com/photoprism/photoprism/blob/develop/internal/photoprism/convert_sidecar_json.go)), so adopting this wrapper for `.xmp` sidecars too would unify both paths — at the cost of making ExifTool (and its Perl runtime) a hard dependency for sidecar reading as well.

**Reference Implementation**

- [`sibprogrammer/xq`](https://github.com/sibprogrammer/xq) — MIT, ~1.1k stars, last push April 2026. Command-line XML/HTML beautifier and content extractor written in Go, distributed via Homebrew, MacPorts, and most Linux package managers. Not importable as a library (all logic lives under `internal/`), but its [`internal/utils/utils.go`](https://github.com/sibprogrammer/xq/blob/master/internal/utils/utils.go) is a compact, working example of how to drive `antchfx/xmlquery` + `antchfx/xpath` for XPath and CSS-selector extraction — useful as a starting point when wiring the same libraries into an XMP reader, and handy as a CLI debugging aid alongside `exiftool -g -j <file>`.

**Notes on `encoding/xml` Itself**

Go 1.23 added well-formedness enforcement (with an `AllowIllFormed` escape hatch), but namespace handling and `xml:lang` semantics are **unchanged** from what PhotoPrism originally hit — see [golang/go#14407](https://github.com/golang/go/issues/14407), still open. A materially better `encoding/xml` is unlikely to land in the standard library; any real fix will almost certainly come via a third-party package.

No maintained Go binding for [`libexempi`](https://libopenraw.freedesktop.org/exempi/) (the GNOME XMP Toolkit port) was found; the Go ecosystem has converged on native implementations.

## Open Issues

- [ ] Replace the hand-written struct in `xmp_document.go` with a generic RDF-aware parser so arbitrary namespace prefixes and nested `rdf:Description` blocks parse correctly. See [**XML/XMP Libraries**](#xmlxmp-libraries) above — `evanoberholster/imagemeta`, `antchfx/xmlquery`, `beevik/etree`, and `knakk/rdf` are the main contenders; `barasher/go-exiftool` is an alternative if we're willing to make ExifTool a hard dependency for sidecars too. [`sibprogrammer/xq`](https://github.com/sibprogrammer/xq) is a useful reference implementation for the XPath + namespace pattern.
- [ ] Add a namespace-priority mechanism to the direct sidecar reader, analogous to the ExifTool path's `meta:"A,B,C"` left-to-right fallback. Two natural options:
    1. extend the hand-written accessors in `xmp_document.go` so each falls back across equivalent namespaces (e.g. `Title()` reads `dc:title`, then `photoshop:Headline`; `Copyright()` reads `dc:rights`, then `xmpRights:WebStatement`)
    2. make the existing `xmp:"..."` struct tags on `meta.Data` load-bearing — drive the reader from them via reflection once the parser can resolve namespace-qualified element names. [`antchfx/xmlquery`](https://github.com/antchfx/xmlquery) (XPath-native, namespace-aware via `xpath.CompileWithNS`) and [`beevik/etree`](https://github.com/beevik/etree) are both promising foundations for option (a); option (b) fits better with an RDF-aware parser such as [`knakk/rdf`](https://github.com/knakk/rdf).
- [ ] Extend the built-in `.xmp` sidecar reader to cover GPS (`exif:GPSLatitude` / `exif:GPSLongitude` / `exif:GPSAltitude`), `xmp:Rating`, `xmp:Label`, `xmpMM:DocumentID` / `xmpMM:InstanceID`, `xmp:CreatorTool`, and `xmpRights:UsageTerms`.
- [ ] Experiment with Adobe Lightroom to see how it currently uses sidecar files. Recent versions of Lightroom no longer appear to sync metadata to XMP by default, probably because Adobe focuses on cloud storage. Needs further investigation.
- [ ] Create a matrix showing which fields are used/supported by which application (Photoshop, Lightroom, Darktable, and others — see also [RAW Image Conversion](../media/raw.md)).

### Released Features

- [Store metadata in the filesystem #4](https://github.com/photoprism/photoprism/issues/4)
- [Compare the quality and XMP compatibility of different RAW converters #65](https://github.com/photoprism/photoprism/issues/65)
