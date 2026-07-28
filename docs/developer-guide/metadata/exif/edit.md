# Editing & Debugging EXIF Data

**Last Updated:** April 21, 2026

This page collects ExifTool and `exif-read-tool` recipes useful when debugging or preparing test fixtures for PhotoPrism's EXIF pipeline. For an overview of how PhotoPrism reads EXIF, see [EXIF](index.md).

## Installing the Tools

- [ExifTool](https://exiftool.org/) — install via your package manager (`apt install exiftool`, `brew install exiftool`) or from the official site.
- [`exif-read-tool`](https://github.com/dsoprea/go-exif/tree/master/v3/command/exif-read-tool) — the reference CLI shipped with the v3 branch of `dsoprea/go-exif`, the same library PhotoPrism uses for its native Stage 1 parser.

## Inspecting EXIF Data

### Dump Every Tag via ExifTool

```bash
exiftool -n photo.jpg            # raw values, human-readable output
exiftool -n -j photo.jpg         # raw values as JSON (same flags PhotoPrism uses)
exiftool -n -g -j photo.jpg      # group tags by source (EXIF / XMP / IPTC / MakerNotes)
```

The `-g` grouping is especially useful for disambiguating tag aliases — for example, telling whether a `Description` came from `EXIF:ImageDescription`, `XMP-dc:description`, or `IPTC:Caption-Abstract`.

### Dump Native-Parser Output

```bash
exif-read-tool -f photo.jpg
```

This matches what PhotoPrism's native parser sees before Stage 2 runs.

### Filter to a Single Tag

```bash
exiftool -n photo.jpg | grep -i orientation
```

## Editing EXIF Data for Testing

### Set a Capture Date

```bash
exiftool -CreateDate="1919:05:04 05:59:26+02:00" photo.jpg
```

### Remove All GPS Tags

```bash
exiftool -GPS:all= photo.jpg
```

### Remove All EXIF Data

```bash
exiftool -all= photo.jpg
```

ExifTool creates a `photo.jpg_original` backup by default. Use `-overwrite_original` to skip the backup, or delete the `_original` file afterward.

### Writing from a Linux Container

When your host does not have ExifTool installed, the quickest sandbox is a Debian container mounting the current directory:

```bash
docker run --rm -v ${PWD}:/test -w /test -ti debian:bookworm bash
apt update && apt install -y exiftool libheif-examples
```

`libheif-examples` is handy alongside ExifTool for converting HEIF/HEIC to JPEG while testing (`heif-convert input.heic output.jpg`).

## Further Reading

More recipes are maintained upstream by Phil Harvey at <https://exiftool.sourceforge.net/examples.html>.
