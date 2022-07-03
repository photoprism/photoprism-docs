Exiftool --> https://exiftool.org/

Installation possible via brew or from homepage.

Exif-Read-Tool: https://github.com/dsoprea/go-exif

## Show exif data for debugging

### Show exif data read from exiftool

`exiftool -j photo.jpg`

### Show exif data read from exif-read-tool

`exif-read-tool -f photo.jpg`


## Edit EXIF data for testing

### Set CreateDate

`exiftool -CreateDate="1919:05:04 05:59:26+02:00" dog_toshi_yellow.jpg`

### Remove all GPS data 
`exiftool -GPS:all= file.jpg`

### Remove all exif data
`exiftool -all= foo.jpg`

Further examples can be found here: https://exiftool.org/examples.html