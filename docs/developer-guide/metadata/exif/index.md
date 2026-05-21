# EXIF

**Last Updated:** April 21, 2026

EXIF (Exchangeable Image File Format) is a metadata standard for camera and image information — capture date, exposure, GPS coordinates, orientation, camera make/model, and similar fields — embedded directly in the image file. It is supported by virtually every camera manufacturer and image processor, and is by far the most important metadata source for PhotoPrism.

## How PhotoPrism Reads EXIF

Unlike XMP, PhotoPrism reads EXIF through a **two-stage pipeline** that combines a native Go parser with an optional ExifTool overlay. Both stages run against the same media file and write into the same `meta.Data` struct; the second stage only fills fields that the first stage left empty.

### Stage 1: Native EXIF Parser

For every supported container, `internal/meta/exif.go` extracts the raw EXIF block and assigns the values PhotoPrism cares about to `meta.Data`. The parser stack is built on [Dustin Oprea's `go-exif` family](https://github.com/dsoprea/go-exif) (v3):

- [`dsoprea/go-exif/v3`](https://github.com/dsoprea/go-exif/tree/master/v3) — the actual EXIF/IFD parser.
- [`dsoprea/go-jpeg-image-structure/v2`](https://github.com/dsoprea/go-jpeg-image-structure) — locates the EXIF segment inside a JPEG.
- [`dsoprea/go-png-image-structure/v2`](https://github.com/dsoprea/go-png-image-structure) — PNG `eXIf` chunk extractor.
- [`dsoprea/go-heic-exif-extractor/v2`](https://github.com/dsoprea/go-heic-exif-extractor) — HEIC / HEIF / AVIF container parser.
- [`dsoprea/go-tiff-image-structure/v2`](https://github.com/dsoprea/go-tiff-image-structure) — TIFF IFD walker.

When the file format is not one of the above, or when the format-specific parser fails, `internal/meta/exif_parser.go:RawExif()` falls back to a brute-force byte search via `exif.SearchFileAndExtractExif`. The brute-force path is also used when `PHOTOPRISM_EXIF_BRUTE_FORCE` is set (see below).

`ExifSupported()` (in `internal/photoprism/mediafile.go`) reports true for JPEG, RAW, HEIF (HEIC/AVIF), PNG, TIFF, and PSD — the native parser stack either handles these directly or the brute-force fallback kicks in for RAW and PSD.

### Stage 2: ExifTool Overlay (Optional)

When ExifTool support is enabled, `internal/photoprism/mediafile_meta.go:MetaData()` then runs [ExifTool](https://exiftool.org/) via `Convert.ToJson()` and merges its cached JSON output into the same `meta.Data` through `internal/meta/json_exiftool.go:Exiftool()`. This stage:

- Recognises far more tag variants and container formats than the native parser (video metadata, Maker Notes, vendor-specific IPTC/XMP blocks, Google Motion Photo, Samsung `MotionPhoto`, etc.).
- **Does not overwrite non-zero values set by the native parser.** The reflection loop in `json_exiftool.go` checks `!fieldValue.IsZero()` before assigning, so the native parser effectively wins for any field it populated. The overlay fills the gaps.
- Is a precondition for embedded XMP support — see [Adobe XMP](../xmp.md).

A regular `<filename>.json` sidecar (Google Photos export or similar) is read by `meta.Data.JSON()` between the two stages, and is also subject to the non-overwrite rule.

### Configuration

| Variable                      | CLI Flag             | Default      | Effect                                                                                                |
|-------------------------------|----------------------|--------------|-------------------------------------------------------------------------------------------------------|
| `PHOTOPRISM_DISABLE_EXIFTOOL` | `--disable-exiftool` | `false`      | Skips Stage 2. Auto-forced to `true` when the sidecar path is not writable or `ExifToolBin` is empty. |
| `PHOTOPRISM_EXIFTOOL_BIN`     | `--exiftool-bin`     | autodetected | Path to the `exiftool` binary used by Stage 2.                                                        |
| `PHOTOPRISM_EXIF_BRUTE_FORCE` | `--exif-bruteforce`  | `false`      | Forces the brute-force byte-search fallback in Stage 1 even when the format-specific parser succeeds. |

ExifTool JSON output is cached per file under `ExifToolCacheName(hash)` (under the configured cache directory, with the media file's SHA-1 as the cache key) so repeated indexing does not re-run `exiftool` on unchanged files.

## Fields Extracted from EXIF

The table below lists every `meta.Data` field that EXIF and/or ExifTool can populate, along with the specific tag names consulted by each stage. The shape mirrors the [XMP overview table](../xmp.md#fields-extracted-from-xmp) so the two pages can be read side by side.

Column meanings:

- **EXIF Tag(s)** — the tag names the native parser in `internal/meta/exif.go` looks up in `data.exif` (the map populated by `dsoprea/go-exif` from the file's IFD0 / ExifIFD / GPSInfo block). Listed in priority order where the parser tries multiple aliases.
- **ExifTool JSON Key(s)** — the aliases listed in the `meta:"..."` struct tag on that field in [`internal/meta/data.go`](https://github.com/photoprism/photoprism/blob/develop/internal/meta/data.go). Stage 2 iterates this list left-to-right and the first non-empty ExifTool JSON value wins.
- **Native (Stage 1)** — `✓` when the native EXIF parser assigns the field; `—` when it does not. Stage 1 only runs for file formats accepted by `ExifSupported()` (JPEG, RAW, HEIF/HEIC/AVIF, PNG, TIFF, PSD).
- **ExifTool (Stage 2)** — `✓` when the ExifTool overlay can populate the field; `—` when it cannot (the field is not driven by a `meta:"..."` tag). Stage 2 **only fills fields that Stage 1 left empty** — see [How PhotoPrism Reads EXIF](#how-photoprism-reads-exif).

| `Data` Field       | EXIF Tag(s) (IFD0 / ExifIFD / GPSInfo)                                                    | ExifTool JSON Key(s)                                                                                                                                      | Native (Stage 1)              | ExifTool (Stage 2) |
|--------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|--------------------|
| `Artist`           | `Artist`                                                                                  | `Artist`, `Creator`, `By-line`, `OwnerName`, `Owner`                                                                                                      | ✓                             | ✓                  |
| `Copyright`        | `Copyright`                                                                               | `Rights`, `Copyright`, `CopyrightNotice`, `WebStatement`                                                                                                  | ✓                             | ✓                  |
| `Title`            | —                                                                                         | `Title`, `Headline`                                                                                                                                       | —                             | ✓                  |
| `Caption`          | `ImageDescription`                                                                        | `Description`, `ImageDescription`, `Caption`, `Caption-Abstract`                                                                                          | ✓ (also auto-keyword)         | ✓                  |
| `Subject`          | —                                                                                         | `Subject`, `PersonInImage`, `ObjectName`, `HierarchicalSubject`, `CatalogSets`                                                                            | —                             | ✓                  |
| `Keywords`         | —                                                                                         | `Keywords`                                                                                                                                                | —                             | ✓                  |
| `Notes`            | —                                                                                         | `Comment`, `UserComment`                                                                                                                                  | —                             | ✓                  |
| `License`          | —                                                                                         | `UsageTerms`, `License`                                                                                                                                   | —                             | ✓                  |
| `Favorite`         | —                                                                                         | `Favorite`                                                                                                                                                | —                             | ✓                  |
| `Software`         | `Software`                                                                                | `Software`, `Producer`, `CreatorTool`, `Creator`, `CreatorSubTool`, `HistorySoftwareAgent`, `ProcessingSoftware`                                          | ✓                             | ✓                  |
| `CameraMake`       | `CameraMake`, then `Make`                                                                 | `CameraMake`, `Make`                                                                                                                                      | ✓                             | ✓                  |
| `CameraModel`      | `CameraModel`, then `Model`, then `UniqueCameraModel`                                     | `CameraModel`, `Model`, `CameraID`, `UniqueCameraModel`                                                                                                   | ✓                             | ✓                  |
| `CameraOwner`      | `CameraOwnerName`                                                                         | `OwnerName`                                                                                                                                               | ✓                             | ✓                  |
| `CameraSerial`     | `BodySerialNumber`                                                                        | `SerialNumber`                                                                                                                                            | ✓                             | ✓                  |
| `LensMake`         | `LensMake`                                                                                | `LensMake`                                                                                                                                                | ✓                             | ✓                  |
| `LensModel`        | `LensModel`, then `Lens`                                                                  | `LensModel`, `Lens`, `LensID`                                                                                                                             | ✓                             | ✓                  |
| `Exposure`         | `ExposureTime` (`N/M` → `1/⌊M/N⌋`)                                                        | `ExposureTime`, `ShutterSpeedValue`, `ShutterSpeed`, `TargetExposureTime`                                                                                 | ✓                             | ✓                  |
| `FNumber`          | `FNumber` (`N/M` → float)                                                                 | `FNumber`                                                                                                                                                 | ✓                             | ✓                  |
| `Aperture`         | `ApertureValue` (`N/M` → float)                                                           | `ApertureValue`, `Aperture`                                                                                                                               | ✓                             | ✓                  |
| `FocalLength`      | `FocalLengthIn35mmFilm`, else `FocalLength`                                               | `FocalLength`, `FocalLengthIn35mmFormat`                                                                                                                  | ✓                             | ✓                  |
| `FocalDistance`    | —                                                                                         | `HyperfocalDistance`                                                                                                                                      | —                             | ✓                  |
| `Iso`              | `ISOSpeedRatings`                                                                         | `ISO`                                                                                                                                                     | ✓                             | ✓                  |
| `Flash`            | `Flash` (low bit == 1)                                                                    | `FlashFired`                                                                                                                                              | ✓ (also adds `flash` keyword) | ✓                  |
| `Width`            | `PixelXDimension`, else `ImageWidth`                                                      | `ImageWidth`, `PixelXDimension`, `ExifImageWidth`, `SourceImageWidth`                                                                                     | ✓                             | ✓                  |
| `Height`           | `PixelYDimension`, else `ImageLength`                                                     | `ImageHeight`, `ImageLength`, `PixelYDimension`, `ExifImageHeight`, `SourceImageHeight`                                                                   | ✓                             | ✓                  |
| `Orientation`      | `Orientation` (defaults to `1` when missing)                                              | `Orientation` / `Rotation` via `Data.Rotation`                                                                                                            | ✓                             | ✓ (via `Rotation`) |
| `Rotation`         | —                                                                                         | `Rotation`                                                                                                                                                | —                             | ✓                  |
| `Projection`       | `ProjectionType` (also adds `panorama` keyword)                                           | `ProjectionType`                                                                                                                                          | ✓                             | ✓                  |
| `ColorProfile`     | —                                                                                         | `ICCProfileName`, `ProfileDescription`                                                                                                                    | —                             | ✓                  |
| `TakenAt`          | `DateTimeOriginal`, then `DateTimeCreated`, `CreateDate`, `DateTime`, `DateTimeDigitized` | `SubSecDateTimeOriginal`, `SubSecDateTimeCreated`, `DateTimeOriginal`, `CreationTime`, `CreationDate`, `DateTimeCreated`, `DateTime`, `DateTimeDigitized` | ✓                             | ✓                  |
| `TakenAtLocal`     | derived from `TakenAt`                                                                    | `SubSecDateTimeOriginal`, `SubSecDateTimeCreated`, `DateTimeOriginal`, `CreationDate`, `DateTimeCreated`, `DateTime`, `DateTimeDigitized`                 | ✓                             | ✓                  |
| `TakenGps`         | GPS sub-IFD timestamp                                                                     | `GPSDateTime`, `GPSDateStamp`                                                                                                                             | ✓                             | ✓                  |
| `TakenNs`          | `SubSecTimeOriginal`, then `SubSecTime`, `SubSecTimeDigitized`                            | (same sub-sec tags consumed by both stages)                                                                                                               | ✓                             | ✓                  |
| `CreatedAt`        | —                                                                                         | `SubSecCreateDate`, `CreationTime`, `CreationDate`, `CreateDate`, `MediaCreateDate`, `ContentCreateDate`, `TrackCreateDate`                               | —                             | ✓                  |
| `TimeOffset`       | —                                                                                         | `OffsetTime`, `OffsetTimeOriginal`, `OffsetTimeDigitized`                                                                                                 | —                             | ✓                  |
| `TimeZone`         | derived from `Lat`/`Lng` via `tz.Position`                                                | derived from `TakenAtLocal` offset; normalised via `tz.Name`                                                                                              | ✓ (via GPS)                   | ✓                  |
| `Lat` / `Lng`      | GPS sub-IFD → `GpsInfo.Decimal()` → `NormalizeGPS`                                        | `GPSPosition` or `GPSLatitude` + `GPSLongitude` (parsed via `GpsToLatLng` / `GpsToDecimal`)                                                               | ✓                             | ✓                  |
| `GPSPosition`      | —                                                                                         | `GPSPosition`                                                                                                                                             | —                             | ✓                  |
| `GPSLatitude`      | —                                                                                         | `GPSLatitude`                                                                                                                                             | —                             | ✓                  |
| `GPSLongitude`     | —                                                                                         | `GPSLongitude`                                                                                                                                            | —                             | ✓                  |
| `Altitude`         | GPS sub-IFD                                                                               | `GlobalAltitude`, `GPSAltitude`                                                                                                                           | ✓                             | ✓                  |
| `DocumentID`       | `ImageUniqueID` (must pass `rnd.SanitizeUUID`)                                            | `ContentIdentifier`, `MediaGroupUUID`, `BurstUUID`, `OriginalDocumentID`, `DocumentID`, `ImageUniqueID`, `DigitalImageGUID`                               | ✓                             | ✓                  |
| `InstanceID`       | —                                                                                         | `InstanceID`, `DocumentID`                                                                                                                                | —                             | ✓                  |
| `ImageType`        | —                                                                                         | `HDRImageType`                                                                                                                                            | —                             | ✓                  |
| `HasThumbEmbedded` | —                                                                                         | `ThumbnailImage`, `PhotoshopThumbnail`                                                                                                                    | —                             | ✓                  |
| `HasVideoEmbedded` | —                                                                                         | `EmbeddedVideoFile`, `MotionPhoto`, `MotionPhotoVideo`, `MicroVideo`                                                                                      | —                             | ✓                  |
| `Duration`         | —                                                                                         | `Duration`, `MediaDuration`, `TrackDuration`, `PreviewDuration`                                                                                           | —                             | ✓                  |
| `FPS`              | —                                                                                         | `VideoFrameRate`, `VideoAvgFrameRate`                                                                                                                     | —                             | ✓                  |
| `Frames`           | —                                                                                         | `FrameCount`, `AnimationFrames`                                                                                                                           | —                             | ✓                  |
| `Pages`            | —                                                                                         | `PageCount`, `NPages`, `Pages`                                                                                                                            | —                             | ✓                  |
| `Codec`            | —                                                                                         | `CompressorID`, `VideoCodecID`, `CodecID`, `OtherFormat`, `FileType`                                                                                      | —                             | ✓                  |
| `MimeType`         | —                                                                                         | `MIMEType`                                                                                                                                                | —                             | ✓                  |
| `FileName`         | —                                                                                         | `FileName`                                                                                                                                                | —                             | ✓                  |

**Notes**

- **Native-reader tag names are not always identical to ExifTool's.** In particular, `CameraOwnerName` (native) ↔ `OwnerName` (ExifTool), `BodySerialNumber` (native) ↔ `SerialNumber` (ExifTool), and `ISOSpeedRatings` (native) ↔ `ISO` (ExifTool). The native parser follows the EXIF 2.3 specification names; ExifTool uses its own normalised names. This is why the two columns show different strings for what is semantically the same value.
- **Purely numeric `CameraModel` / `CameraMake` / `LensMake` / `LensModel` values are rejected** by the native parser (`txt.IsUInt` check). Broken exporters occasionally write things like `42` as a camera model; these are dropped so Stage 2 can supply a real value instead.
- **`Orientation` falls back to `1`** in Stage 1; the ExifTool path can also populate it via `Rotation` (`xmp:Rotation` or QuickTime `Rotation`), which is mapped back to an orientation value in `json_exiftool.go`.
- **GPS coordinates** flow into `Lat`/`Lng` directly from the native parser (via `exif.GpsInfo`). The `GPSPosition` / `GPSLatitude` / `GPSLongitude` string fields in `Data` are only populated by Stage 2 and then parsed into `Lat`/`Lng` if they are still zero.
- **Sub-second tags** are consulted by both stages but stored in `Data.TakenNs` only once; whichever stage writes first wins.

## Notable Behaviours

These are the EXIF-reader quirks that most commonly surprise developers when debugging indexing issues:

- **IFD0 wins over IFD1.** When the same tag appears in both the primary IFD and the embedded-thumbnail IFD, PhotoPrism keeps the IFD0 value — see issue [#2231](https://github.com/photoprism/photoprism/issues/2231).
- **Numeric model names are discarded.** `CameraModel`, `CameraMake`, `LensMake`, and `LensModel` are skipped when the value parses as an unsigned integer (seen in the wild from broken exporters).
- **Orientation defaults to `1`** when no tag is present; a missing orientation does not block indexing.
- **GPS derives the time zone** in Stage 1; explicit offset tags (`OffsetTime`, `OffsetTimeOriginal`, `OffsetTimeDigitized`) are consumed later by the Stage 2 ExifTool path via `Data.TimeOffset` and may refine it.
- **Sub-second precision** is merged back into `TakenAt` and `TakenAtLocal` after time zone resolution.
- **`ImageUniqueID` becomes `DocumentID`**, which in turn governs file stacking — if a RAW and a JPEG share an `ImageUniqueID`, PhotoPrism stacks them.
- **`Flash` keyword** is only added when the EXIF flash flag's low bit is `1` (flash actually fired), not just when the flag is present.
- **Per-file mutex.** `Data.Exif()` takes a package-level `sync.Mutex`; concurrent calls serialise through it because `dsoprea/go-exif`'s tag index isn't goroutine-safe on write.
- **`ExifSupported()` gate.** `mediafile_meta.go:MetaData()` only runs Stage 1 for JPEG, RAW, HEIF, PNG, TIFF, and PSD; everything else relies entirely on Stage 2 (ExifTool).

## References

- [Official EXIF specification (v2.3)](https://dl.photoprism.app/pdf/specifications/20120101-Exif_v2.3.pdf)
- [`dsoprea/go-exif`](https://github.com/dsoprea/go-exif) — native Go EXIF parser used in Stage 1.
- [ExifTool by Phil Harvey](https://exiftool.org/) — used in Stage 2.
- [Dave Perrett — EXIF Orientation Handling is a Ghetto](https://www.daveperrett.com/articles/2012/07/28/exif-orientation-handling-is-a-ghetto/) — still the clearest practical writeup on what the 8 orientation values actually mean.
- [Editing & Debugging EXIF Data](edit.md) — how to inspect and modify EXIF for testing.

## Using ExifTool Locally

If you want to reproduce PhotoPrism's Stage 2 output on your laptop, install ExifTool via your package manager:

```bash
docker run --rm -v ${PWD}:/test -w /test -ti debian:bookworm bash
apt update && apt install -y exiftool libheif-examples
```

Then inspect a file the same way PhotoPrism does (`-n` disables human-readable formatting, `-j` emits JSON, `-g` groups tags by source — helpful for disambiguating EXIF/XMP/IPTC aliases):

```bash
exiftool -n -j photo.jpg
exiftool -n -g -j photo.jpg | jq '.[0] | keys'
exiftool -n photo.jpg | grep -i orientation
```

For examples of how other applications display EXIF data, and for recipes to edit EXIF tags while testing, see the [Editing & Debugging EXIF Data](edit.md) page.
