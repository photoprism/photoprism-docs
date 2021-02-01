## Edit EXIF metadata for testing
Exiftool --> https://exiftool.org/

Installation possible via brew or from homepage.

## Command line examples

### Set CreateDate

`exiftool -CreateDate="1919:05:04 05:59:26+02:00" dog_toshi_yellow.jpg`

### Remove all GPS data 
`exiftool -GPS:all= file.jpg`

### Remove all exif data
`exiftool -all= foo.jpg`

Further examples can be found here: https://exiftool.org/examples.html