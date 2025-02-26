# Checking Image and Video Metadata

We recommend checking the file metadata with [Exiftool](https://exiftool.org/) if some of your pictures are displayed incorrectly (stretched, distorted)[^1], information seems to be missing (e.g. title or caption), or the [wrong time and location](../../user-guide/organize/edit.md) are shown.

To do this, run the following command within a Docker [terminal session](../docker-compose.md#opening-a-terminal) or on your host if you have Exiftool installed (`-n` displays the raw values without changes, `-j` will format the output as JSON, and `-g` optionally groups the output by metadata source):

```bash
exiftool -n -j [filename]
```

If the file specified with `[filename]` contains readable metadata, it will then be displayed to you as JSON-formatted values, for example:

```json
[{
  "SourceFile": "example.jpg",
  "ExifToolVersion": 12.76,
  "FileSize": 200108,
  "FileType": "JPEG",
  "MIMEType": "image/jpeg",
  "Make": "HUAWEI",
  "Model": "ELE-L29",
  "Orientation": 1,
  "ExposureTime": 0.02,
  "FNumber": 1.8,
  "ISO": 100,
  "DateTimeOriginal": "2020:10:17 17:48:24",
  "CreateDate": "2020:10:17 17:48:24",
  "ImageWidth": 500,
  "ImageHeight": 375,
  "Aperture": 1.8,
  "ShutterSpeed": 0.02,
  "SubSecCreateDate": "2020:10:17 17:48:24.950488",
  "SubSecDateTimeOriginal": "2020:10:17 17:48:24.950488",
  "SubSecModifyDate": "2020:10:17 17:48:24.950488",
  "GPSAltitude": 84.47,
  "GPSDateTime": "2020:10:17 15:48:23Z",
  "GPSLatitude": 33.8120962,
  "GPSLongitude": -117.9215491
}]
```

This allows you to check e.g. the values for **Orientation** and **Rotation** if you have problems with the [image orientation](#exif-orientation).

When you post the output on [GitHub](https://github.com/photoprism/photoprism/discussions) or in our [Community Chat](https://link.photoprism.app/chat), please format it as follows for better readability:

    ```json
    [{
      "SourceFile": "example.jpg",
      "ExifToolVersion": 12.76,
      ...
    }]
    ```

Thank you very much!

## Exif Orientation

The numbers used in [Exif metadata](../../developer-guide/metadata/exif/index.md) to specify the [image orientation](../../developer-guide/metadata/orientation.md) are defined as follows: 

1. = 0 degrees: the correct orientation, no adjustment is required.
2. = 0 degrees, mirrored: image has been flipped back-to-front.
3. = 180 degrees: image is upside down.
4. = 180 degrees, mirrored: image has been flipped back-to-front and is upside down.
5. = 90 degrees: image has been flipped back-to-front and is on its side.
6. = 90 degrees, mirrored: image is on its side.
7. = 270 degrees: image has been flipped back-to-front and is on its far side.
8. = 270 degrees, mirrored: image is on its far side.

[Learn more ›](https://sirv.com/help/articles/rotate-photos-to-be-upright/)

## Installing Exiftool

Running the following commands will install Exiftool on Debian or Ubuntu Linux if needed:

```bash
sudo apt update
sudo apt install -y exiftool
```

See the [Exiftool documentation](https://exiftool.org/install.html) for how to install it on other operating systems.

[^1]: If images are displayed in low resolution or slightly distorted, this may also be due to a problem with the [thumbnail cache folder](../docker-compose.md#photoprismstorage) or [your quality settings](../../user-guide/settings/advanced.md#image-quality).