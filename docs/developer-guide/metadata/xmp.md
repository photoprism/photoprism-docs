# Adobe XMP

**Last Updated:** July 28, 2026

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

This path also covers the XMP that `exiftool` extracts from RAW, HEIC, and video containers. If `PHOTOPRISM_DISABLE_EXIFTOOL` is set, embedded XMP is not indexed.

### `.xmp` Sidecar Files via the Built-In Reader

When the indexer encounters a standalone `.xmp` file (see `internal/photoprism/index_mediafile.go`, `case m.IsXMP()`), it does **not** invoke ExifTool. It parses the XML directly with the built-in reader in:

- `internal/meta/xmp.go` — entry point `meta.XMP(fileName)`; assigns the recognised values to `meta.Data`, then normalises capture time, local time, and time zone through the shared `(*Data).ResolveTimeZone` resolver so the sidecar path produces the same entity state the ExifTool path would for identical metadata.
- `internal/meta/xmp_document.go` — the reader itself: an XPath-based, namespace-aware parser built on [`antchfx/xmlquery`](https://github.com/antchfx/xmlquery) and [`antchfx/xpath`](https://github.com/antchfx/xpath).

The reader was rewritten in [#2260](https://github.com/photoprism/photoprism/issues/2260) and is no longer a proof of concept. It now covers the same descriptive, camera/lens/exposure, GPS, identity, and time fields the ExifTool path covers (the remaining gaps are listed under [Open Issues](#open-issues)), and it reads standalone `.xmp` sidecar files only — it does **not** read XMP embedded in another media file.

Key design points (see [`internal/meta/README.md`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/README.md#xmp-sidecar-reader) for the authoritative description):

- **Namespace-aware queries.** Every XPath expression is compiled once at package init via `xpath.CompileWithNS` against a fixed prefix→URI map. The reader matches by XML namespace, **not** by local name, so a sidecar that uses a non-default prefix for a known namespace still parses, and unrelated elements that merely share a local name do not collide.
- **Namespace-priority fallback.** Each field is backed by a `chainXPath` — an ordered list of expressions evaluated left-to-right; the first non-empty match wins. This is the direct-reader equivalent of the ExifTool path's `meta:"A,B,C"` left-to-right alias fallback. For example `Title` reads `dc:title` (language-tagged `rdf:Alt` → first `rdf:li` → bare text) and then falls back to `photoshop:Headline`; `Copyright` falls back from `dc:rights` to `xmpRights:WebStatement`.
- **Element-or-attribute matching.** RDF/XML allows a scalar property to be written either as a child element or as an attribute on `rdf:Description`. The `elemOrAttr` helper builds a union expression that matches both forms — required because digiKam emits `xmpMM:*` / `exif:*` / `tiff:*` as attributes while Adobe writes them as child elements. Multiple sibling `rdf:Description` blocks (each declaring its own namespace) are also walked correctly.
- **Composition lives in the accessor, not the chain.** Sign handling (`GPSLatitudeRef`/`GPSLongitudeRef`), the sub-second join from `exif:SubSecTimeOriginal`, the APEX → seconds conversion for `exif:ShutterSpeedValue`, and the combined-vs-split `exif:GPSTimeStamp`/`GPSDateStamp` reassembly are all implemented in the relevant accessor rather than in the generic chain engine.
- **Loader security guards.** `Load` rejects sidecars larger than 1 MiB (`ErrXmpFileTooLarge`) and documents nesting deeper than 64 elements (`ErrXmpTooDeep`). XXE and DTD attacks are mitigated by `encoding/xml`'s default behaviour (no external entity resolution); `internal/meta/xmp_security_test.go` is the regression guard. A malformed sidecar does not block indexing of the related image — the indexer logs a warning, records the parse failure in the XMP file row's `file_error`, and continues with the remaining related files.
- **Source priority.** Sidecar values are tagged `SrcXmp` (priority 32), which outranks `SrcMeta` (priority 16) at the entity layer. Re-indexing a photo after a sidecar has been added therefore overwrites the previously embedded-path values without a database wipe — including GPS coordinates, which the sidecar overrides even when the image carries its own embedded EXIF position.

## Fields Extracted from XMP

The table below lists the XMP elements PhotoPrism currently consumes, their primary XMP namespace, and whether each path reads them. ExifTool-JSON keys are the default (un-grouped) names as they appear in the output of `exiftool -n -j`; PhotoPrism looks them up case-sensitively via the `meta:"..."` struct tags on `meta.Data`. The "`.xmp` Sidecar (Direct)" column shows the priority chain the reader evaluates (first non-empty match wins).

| PhotoPrism `Data` Field | XMP Namespace and Element                                                       | ExifTool JSON Key(s)                                                                  | Embedded (ExifTool) | `.xmp` Sidecar (Direct)                                                       |
|-------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------|
| `Title`                 | `dc:title` (Dublin Core); also `photoshop:Headline`                             | `Title`, `Headline`                                                                   | ✓                   | ✓ `dc:title` → `photoshop:Headline`                                          |
| `Caption`               | `dc:description`                                                                | `Description`, `ImageDescription`, `Caption`, `Caption-Abstract`                      | ✓                   | ✓ `dc:description` (lang-alt fallback)                                        |
| `Artist`                | `dc:creator`                                                                    | `Artist`, `Creator`, `By-line`, `OwnerName`, `Owner`                                  | ✓                   | ✓ first `dc:creator/rdf:Seq` entry                                           |
| `Copyright`             | `dc:rights`; `xmpRights:WebStatement`                                           | `Rights`, `Copyright`, `CopyrightNotice`, `WebStatement`                              | ✓                   | ✓ `dc:rights` → `xmpRights:WebStatement`                                     |
| `License`               | `xmpRights:UsageTerms`                                                          | `UsageTerms`, `License`                                                               | ✓                   | ✓ `xmpRights:UsageTerms` (lang-alt fallback)                                 |
| `Subject`               | `dc:subject`; `Iptc4xmpExt:PersonInImage`; `lr:hierarchicalSubject`            | `Subject`, `HierarchicalSubject`, `PersonInImage`, `CatalogSets`, `ObjectName`        | ✓                   | ✓ `dc:subject` (`rdf:Bag` → `rdf:Seq`) → `Iptc4xmpExt:PersonInImage` → `lr:hierarchicalSubject` |
| `Keywords`              | IPTC keyword block (no XMP equivalent)                                          | `Keywords`                                                                            | ✓                   | ✓ auto-derived only (`flash`, `panorama`, `hdr`)                             |
| `Faces`                 | `mwg-rs:RegionList`; `MP:RegionInfo`; `acdsee-rs:RegionList`                    | `RegionName`, `RegionArea*`, `RegionPersonDisplayName`, `RegionRectangle`, `ACDSeeRegion*` | ✓              | ✓ MWG-RS → Microsoft → ACDSee                                                |
| `TakenAt`               | `photoshop:DateCreated`; `exif:DateTimeOriginal`; `xmp:CreateDate`              | `SubSecDateTimeOriginal`, `DateTimeOriginal`, `CreationDate`, `DateTimeDigitized`     | ✓                   | ✓ `photoshop:DateCreated` → `exif:DateTimeOriginal` → `xmp:CreateDate` (+ `exif:SubSecTimeOriginal` join) |
| `CreatedAt`             | `xmp:CreateDate`; `xmpDM:CreationDate`                                          | `SubSecCreateDate`, `CreateDate`, `MediaCreateDate`, `TrackCreateDate`                | ✓                   | ✓ `xmp:CreateDate` → `xmpDM:CreationDate`                                    |
| `TimeOffset`            | `exif:OffsetTimeOriginal` / `OffsetTime` / `OffsetTimeDigitized`               | `OffsetTimeOriginal`, `OffsetTime`                                                    | ✓                   | ✓ `OffsetTimeOriginal` → `OffsetTime` → `OffsetTimeDigitized`               |
| `Software`              | `xmp:CreatorTool`                                                               | `Software`, `CreatorTool`, `HistorySoftwareAgent`, `ProcessingSoftware`               | ✓                   | ✓ `xmp:CreatorTool`                                                          |
| `CameraMake`            | `tiff:Make`                                                                     | `Make`, `CameraMake`                                                                  | ✓                   | ✓ `tiff:Make`                                                                |
| `CameraModel`           | `tiff:Model`                                                                    | `Model`, `CameraModel`, `UniqueCameraModel`                                           | ✓                   | ✓ `tiff:Model`                                                               |
| `CameraSerial`          | `exifEX:SerialNumber`; `aux:SerialNumber`                                       | `SerialNumber`                                                                        | ✓                   | ✓ `exifEX:SerialNumber` → `aux:SerialNumber`                                 |
| `CameraOwner`           | `aux:OwnerName`                                                                 | `OwnerName`, `Owner`                                                                  | ✓                   | ✓ `aux:OwnerName`                                                            |
| `LensMake`              | `exifEX:LensMake`                                                               | `LensMake`                                                                            | ✓                   | ✓ `exifEX:LensMake`                                                          |
| `LensModel`             | `exifEX:LensModel`; `aux:Lens` / `aux:LensID`                                   | `LensModel`, `Lens`, `LensID`                                                         | ✓                   | ✓ `exifEX:LensModel` → `aux:Lens` → `aux:LensID`                            |
| `FocalLength`           | `exif:FocalLength`; `exif:FocalLengthIn35mmFilm`                               | `FocalLength`, `FocalLengthIn35mmFormat`                                              | ✓                   | ✓ `exif:FocalLength` → `exif:FocalLengthIn35mmFilm`                          |
| `Exposure`              | `exif:ExposureTime`; `exif:ShutterSpeedValue`                                   | `ExposureTime`, `ShutterSpeedValue`, `ShutterSpeed`                                   | ✓                   | ✓ `exif:ExposureTime` → `exif:ShutterSpeedValue` (APEX)                      |
| `Aperture` / `FNumber`  | `exif:ApertureValue`; `exif:FNumber`                                            | `ApertureValue`, `Aperture`, `FNumber`                                                | ✓                   | ✓ `exif:ApertureValue` / `exif:FNumber`                                      |
| `Iso`                   | `exifEX:PhotographicSensitivity`; `exif:ISOSpeedRatings`                        | `ISO`                                                                                 | ✓                   | ✓ `exifEX:PhotographicSensitivity` → `exif:ISOSpeedRatings`                  |
| `Flash`                 | `exif:Flash/Fired`                                                              | `FlashFired`                                                                          | ✓                   | ✓ `exif:Flash/Fired` (element / attribute / nested)                          |
| `Notes`                 | `exif:UserComment`                                                              | `UserComment`                                                                         | ✓                   | ✓ `exif:UserComment` (lang-alt fallback)                                     |
| `Rotation`              | `xmp:Rotation`; `tiff:Orientation`                                              | `Rotation`, `Orientation`                                                             | ✓                   | —                                                                            |
| `Width` / `Height`      | `tiff:ImageWidth` / `ImageLength`; `exif:PixelXDimension` / `PixelYDimension`   | `ImageWidth`, `ExifImageWidth`, `PixelXDimension`, `ImageHeight`, `ExifImageHeight`   | ✓                   | —                                                                            |
| `Lat` / `Lng`           | `exif:GPSLatitude` / `GPSLongitude` (+ `GPSLatitudeRef` / `GPSLongitudeRef`)    | `GPSLatitude`, `GPSLongitude`, `GPSPosition`                                          | ✓                   | ✓ decimal, DMS, and 2-component Adobe form                                   |
| `Altitude`              | `exif:GPSAltitude` (+ `GPSAltitudeRef`)                                         | `GlobalAltitude`, `GPSAltitude`                                                       | ✓                   | ✓ rational, ref-sign applied                                                 |
| `TakenGps`              | `exif:GPSTimeStamp` / `GPSDateStamp`                                            | `GPSDateTime`, `GPSDateStamp`                                                         | ✓                   | ✓ combined ISO 8601 → split `GPSDateStamp` + `GPSTimeStamp`                  |
| `Projection`            | `GPano:ProjectionType` (Google Photo Sphere)                                    | `ProjectionType`                                                                      | ✓                   | ✓ `GPano:ProjectionType` (auto-adds the `panorama` keyword)                  |
| `ColorProfile`          | `photoshop:ICCProfile`                                                          | `ICCProfileName`, `ProfileDescription`                                                | ✓                   | ✓ `photoshop:ICCProfile`                                                     |
| `DocumentID`            | `xmpMM:OriginalDocumentID` / `DocumentID`; `dc:identifier`                      | `ContentIdentifier`, `OriginalDocumentID`, `DocumentID`, `ImageUniqueID`, `BurstUUID` | ✓                   | ✓ `OriginalDocumentID` → `DocumentID` → `dc:identifier`                      |
| `InstanceID`            | `xmpMM:InstanceID`                                                              | `InstanceID`                                                                          | ✓                   | ✓ `xmpMM:InstanceID`                                                         |
| `Favorite`              | Custom `http://www.fstopapp.com/xmp/ favorite` attribute (F-Stop app)           | `Favorite` (when present)                                                             | ✓ (via tag alias)   | ✓ F-Stop `favorite="1"` attr                                                 |
| `HasThumbEmbedded`      | `photoshop:Thumbnail`                                                           | `ThumbnailImage`, `PhotoshopThumbnail`                                                | ✓                   | —                                                                            |
| `HasVideoEmbedded`      | Google Motion Photo (`GCamera:MicroVideo`), Samsung `MotionPhoto`               | `EmbeddedVideoFile`, `MotionPhoto`, `MotionPhotoVideo`, `MicroVideo`                  | ✓                   | —                                                                            |

**Notes**

- `dc:subject` populates the descriptive `Subject` field, never the editable Keywords field. `dc:subject` is Adobe's "Keywords" panel, but its entries are human-readable, often multi-word terms that `Subject` preserves verbatim. Subject content stays findable because the indexer tokenizes it into the search index, and it is matched against existing labels. Because XMP has no IPTC keyword block, the only keywords the XMP paths contribute are the ones PhotoPrism derives itself (`flash`, `panorama`, `hdr`).
- The XMP element column lists the *primary* namespace mapping. Many fields are aliased across several namespaces (for example, `dc:title` ↔ `photoshop:Headline` ↔ `IPTC:Headline`) and ExifTool merges them, which is why PhotoPrism usually lists multiple ExifTool keys per field.
- The `.xmp` sidecar column now shows the **full priority chain** the reader evaluates, not a single element. Where a lang-alt fallback is noted, the reader prefers the `xml:lang="x-default"` `rdf:li`, then the first `rdf:li`, then bare element text.
- `Lat`/`Lng`/`Altitude` are decimal floats derived in the reader. The reader does not populate the ExifTool-format string fields `GPSLatitude`/`GPSLongitude` — those keep whatever the embedded path set. GPS decimal parsing now accepts the pure decimal form, the 3-component DMS form (`51 deg 15' 17.47" N`), and the 2-component Adobe XMP form (`52,30.4567N`) that older readers silently dropped.
- The XMP `DocumentID` is adopted as the photo UUID. Real-world document IDs are frequently non-canonical (no dashes, `adobe:docid:` / `xmp.did:` prefixes), so it is stored as-is rather than discarded by a strict UUID check. `InstanceID` and `Software` are mirrored onto the primary file row so the values are visible in the UI (which shows per-file identity metadata for the primary JPEG/HEIC). `ColorProfile` and `Projection` are intentionally **not** mirrored to the primary file — they describe the physical image container, not user-supplied sidecar metadata.
- The authoritative mapping for the ExifTool path lives in the `meta:"..."` struct tags on `meta.Data` in [`internal/meta/data.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/data.go). For the direct sidecar reader, the authoritative mapping is the set of `chainXPath` definitions in [`internal/meta/xmp_document.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/xmp_document.go); the per-fixture provenance lives in the fixture corpus under [`internal/meta/testdata/xmp/`](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata/xmp).
- The `xmp:"..."` / `dc:"..."` struct tags on `meta.Data` are read by `internal/meta/report.go` to render the developer field report (`photoprism show metadata-fields`); they document the namespace mapping but are not the mechanism that drives the reader — the `chainXPath` definitions are.

## Face Regions

Both XMP paths can import named face regions and turn them into people markers, so names assigned in Adobe Bridge, Lightroom, digiKam, ACDSee, or Windows can be reused instead of being re-entered in PhotoPrism.

Import is off by default and enabled with `PHOTOPRISM_XMP_FACES` (CLI `--xmp-faces`), or with the *Import Faces from XMP* switch in [*Settings > Advanced*](../../user-guide/settings/advanced.md#import-faces-from-xmp). The bundled `compose.yaml` and setup examples set it to `"true"`, so new installations have it enabled while existing libraries do not start creating people on their next re-index.

### Supported Region Dialects

| Dialect                              | Region Container       | Name Element                                                       |
|--------------------------------------|------------------------|--------------------------------------------------------------------|
| MWG-RS (Adobe, Lightroom, digiKam)   | `mwg-rs:RegionList`    | `mwg-rs:Name`, falling back to `mwg-rs:Title` and `PersonInImage`  |
| Microsoft (Windows, Photo Gallery)   | `MP:RegionInfo`        | `MPReg:PersonDisplayName`                                          |
| ACDSee                               | `acdsee-rs:RegionList` | `acdsee-rs:Name`                                                   |

- **Shapes.** Center-based rectangles and circles are supported, in normalized or pixel units. `mwg-rs:Rotation` is applied as the axis-aligned bounds of the rotated rectangle. A region that extends past the frame is clipped; a region whose center falls outside the frame is rejected. When `AppliedToDimensions` is missing, pixel and circular regions are resolved against the source image's real dimensions.
- **Orientation.** Coordinates are mapped into the EXIF-displayed frame, covering all eight orientations including the mirrored and transposed cases, so imported regions line up with markers detected on the orientation-corrected preview.
- **Region type.** `mwg-rs:Type` and `acdsee-rs:Type` are optional in their specifications, so a region without one is imported. Only an explicitly declared non-face type, such as `BarCode`, `Pet`, or `Focus`, is skipped.

### Sources and Precedence

- Regions are read from the **logical still image** — for HEIC and RAW originals that is the source file or its sidecar, not the generated JPEG preview that is indexed as the primary file. The resulting markers are attached to the primary file. Videos, PDFs, and animated images are excluded.
- Sidecars are searched in the originals folder, the configured sidecar folder, and `.photoprism`, matching both the `photo.xmp` and the `photo.ext.xmp` naming scheme. Candidates are tried newest first.
- A **sidecar overrides the embedded packet only when it declares a region container.** Rating-only and develop-only sidecars are ordinary editor output — PhotoPrism itself hands an existing `.xmp` to `darktable-cli` — so their lack of regions is not treated as "this image has no faces".
- Import is best-effort: a malformed sidecar is logged and skipped without failing the index or discarding faces that were detected automatically.

### Markers and People

- A region that overlaps a marker found by [face detection](../vision/face-recognition.md) keeps the detected rectangle and only contributes the name. A region with no overlap creates a new marker from the XMP rectangle.
- Names are resolved to people by exact name, so an imported name links to an existing person if one exists and creates a new one otherwise. Imported names override automatically assigned names but never a name a user or admin set manually.
- Named regions are ready to use; **unnamed** regions are flagged for review so you can name them in [*People*](../../user-guide/organize/people.md).
- Markers you rejected are never recreated or resurrected by an import.
- Imported names do not drive face clustering: markers created from XMP carry no face embedding, and an imported name is not promoted onto the shared face cluster of a detected marker.

### Re-Indexing and Removal

Re-import is idempotent. Updated or newly added sidecars are re-read on incremental indexing passes, so name changes are picked up without a full rescan, and geometry stays stable.

Deleting a region is only honored when the file states unambiguously that it has none left:

| Region Container    | Regions Resolved | Markers Deleted |
|---------------------|------------------|-----------------|
| Absent              | —                | No              |
| Present, incomplete | Partially        | No              |
| Present, complete   | Fully            | Yes             |

A suppressed sweep still updates and names every region it matched; it only declines to delete or clear the markers it did not match. This is what keeps a rating-only sidecar, a writer that omits optional region members, or an unreadable RAW sibling from wiping markers that are still valid.

Two gaps follow from this and are worth knowing before you rely on deletion:

- Removing **every** region from an *embedded* packet leaves its markers in place. ExifTool flattens the region containers away, so the embedded path cannot tell "the user removed the last face" from "this file never tracked regions". The sidecar path has a narrower version of the same gap: it recognizes an emptied `RegionList`, but a writer that deletes the whole `mwg-rs:Regions` struct instead leaves nothing to declare.
- Deleting a sidecar file is not detected on an incremental pass. Its metadata is cleared on a forced rescan.

## Sidecar Reader Limitations

The built-in `.xmp` sidecar reader now covers the high-value descriptive, camera, GPS, identity, and time fields, but it is still a focused reader rather than a general-purpose XMP toolkit:

- Only the fields marked as supported in the table above are applied; everything else in the sidecar is ignored, even if it is valid XMP. Notably `xmp:Rating`, `xmp:Label`, image dimensions, and embedded-media flags are not read from sidecars (they remain ExifTool-only). `tiff:Orientation` is read, but only to place face regions — it does not set the photo's orientation.
- The reader is read-only. It does not write `.xmp` sidecars back out; round-tripping or generating sidecars is out of scope.
- It is not a generic RDF/XMP processor. Each supported field is wired explicitly through a `chainXPath`; a brand-new namespace or property is not picked up until an accessor and chain are added for it. Adding one is intentionally small — declare a `chainXPath` at package init, document the priority order, add the accessor that calls `firstNonEmpty` (scalars) or `queryAll` (`rdf:Bag`/`rdf:Seq`), and wire the field into `xmp.go` with the existing "set only when non-empty" pattern.
- `encoding/xml`'s namespace and `xml:lang` handling remains the long-standing Go limitation ([golang/go#14407](https://github.com/golang/go/issues/14407)); the reader works around it with XPath-level namespace binding rather than relying on the standard unmarshaller.

Pull requests that extend the supported field set are welcome.

## RAW Conversion

PhotoPrism currently supports Darktable and RawTherapee as RAW image converters (as well as Sips on macOS). Darktable fully supports XMP sidecar files; RawTherapee only partially. XMP is a container format, so the fields (namespaces) used to describe how an image should be rendered differ between Lightroom/Photoshop, Darktable, and RawTherapee — an application that "supports XMP" in general may still be unable to interpret edits written by another vendor.

From our experience, some basic edits done with Adobe tools — such as cropping — can survive conversion with Darktable, while advanced edits like lens or color corrections usually do not.

[Learn more ›](../media/raw.md)

## Resources

### File Samples

We would be happy to receive more [XMP files for testing](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata). There are two ways to contribute:

- **Pull request** against [`internal/meta/testdata`](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata) — see the [Pull Requests](../pull-requests.md) guide. Use this for files you are clearly licensed to share publicly (files you created yourself, or files from an openly licensed corpus). New fixtures should follow the corpus layout under [`internal/meta/testdata/xmp/`](https://github.com/photoprism/photoprism/tree/develop/internal/meta/testdata/xmp) (`adobe/`, `darktable/`, `digikam/`, `synthetic/`) and ship the paired `*.exiftool.txt` reference.
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

### Implementation & Library Notes

The `.xmp` sidecar reader is built on [`antchfx/xmlquery`](https://github.com/antchfx/xmlquery) (MIT) and [`antchfx/xpath`](https://github.com/antchfx/xpath) (MIT), which provide a DOM-style parser and full XPath 1.0 with namespace-aware compilation via `xpath.CompileWithNS(expr, nsMap)`. This is what makes the namespace-priority chains (`//dc:title | //photoshop:Headline`, compiled once and reused for every sidecar in an indexer run) possible. Both libraries are read-only, so writing sidecars back out would still require `encoding/xml` or another library.

Alternatives considered during the rewrite, and still relevant if the scope expands to writing sidecars or to a fully RDF-aware model:

- [`evanoberholster/imagemeta`](https://github.com/evanoberholster/imagemeta) — MIT, actively maintained. Broader image-metadata library with an `xmp` sub-package; decodes dates and rationals into Go types and handles nested `rdf:Description`. Read-only.
- [`beevik/etree`](https://github.com/beevik/etree) — BSD-2-Clause, actively maintained. DOM-style XML with XPath-like selectors and **write** support; rational/date coercion still manual.
- [`knakk/rdf`](https://github.com/knakk/rdf) — MIT, actively maintained. Turtle / N-Triples / RDF-XML triple parser; cleanest semantic match for XMP-as-RDF but does not write RDF/XML back.
- [`barasher/go-exiftool`](https://github.com/barasher/go-exiftool) — Apache-2.0. Wraps the `exiftool` binary; would unify both XMP paths at the cost of making ExifTool a hard dependency for sidecar reading as well.
- [`sibprogrammer/xq`](https://github.com/sibprogrammer/xq) — MIT. CLI XML extractor; not importable, but a compact working example of driving `antchfx/xmlquery` + `antchfx/xpath`, and a handy debugging aid alongside `exiftool -g -j <file>`.

No maintained Go binding for [`libexempi`](https://libopenraw.freedesktop.org/exempi/) was found; the Go ecosystem has converged on native implementations.

## Open Issues

- [x] Replace the hand-written struct in `xmp_document.go` with a namespace-aware parser so arbitrary namespace prefixes and nested `rdf:Description` blocks parse correctly. *(Done in [#2260](https://github.com/photoprism/photoprism/issues/2260) — XPath-based reader on `antchfx/xmlquery`.)*
- [x] Add a namespace-priority mechanism to the direct sidecar reader, analogous to the ExifTool path's left-to-right fallback. *(Done — `chainXPath` priority lists per field.)*
- [x] Extend the built-in `.xmp` sidecar reader to cover GPS (`exif:GPSLatitude` / `GPSLongitude` / `GPSAltitude`), `xmpMM:DocumentID` / `xmpMM:InstanceID`, `xmp:CreatorTool`, and `xmpRights:UsageTerms`. *(Done — see the field table above.)*
- [x] Import face regions from XMP as people markers, from both the sidecar and the embedded path. *(Done in [#5712](https://github.com/photoprism/photoprism/issues/5712) and [#5751](https://github.com/photoprism/photoprism/issues/5751) — see [Face Regions](#face-regions).)*
- [x] Map `dc:subject` to the descriptive Subject field instead of the keyword list. *(Done in [#2075](https://github.com/photoprism/photoprism/issues/2075).)*
- [ ] Parse hierarchical keyword tags (`lr:hierarchicalSubject`, `digiKam:TagsList`, `MicrosoftPhoto:LastKeywordXMP`) into labels, preserving the `Parent|Child` hierarchy. See [#5710](https://github.com/photoprism/photoprism/issues/5710).
- [ ] Extend the reader to the remaining ExifTool-only fields: `xmp:Rating`, `xmp:Label`, `Rotation`/`Orientation`, image dimensions, and the embedded-media flags.
- [ ] Add sidecar **write** support (or a generic RDF model) so PhotoPrism can persist edits back to `.xmp`. The current reader is read-only.
- [ ] Experiment with Adobe Lightroom to see how it currently uses sidecar files. Recent versions of Lightroom no longer appear to sync metadata to XMP by default, probably because Adobe focuses on cloud storage. Needs further investigation.
- [ ] Create a matrix showing which fields are used/supported by which application (Photoshop, Lightroom, Darktable, and others — see also [RAW Image Conversion](../media/raw.md)).

### Released Features

- [Store metadata in the filesystem #4](https://github.com/photoprism/photoprism/issues/4)
- [Compare the quality and XMP compatibility of different RAW converters #65](https://github.com/photoprism/photoprism/issues/65)
- [Rewrite the `.xmp` sidecar reader as a namespace-aware XPath parser #2260](https://github.com/photoprism/photoprism/issues/2260)
