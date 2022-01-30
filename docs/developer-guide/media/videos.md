# Videos #

PhotoPrism may use [*ffmpeg*](https://www.ffmpeg.org/documentation.html) to transcode 
common video formats to [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4).
This container / codec combination doesn't require transcoding as it can be played 
natively by most modern browsers, see https://caniuse.com/mpeg4.

For a list of codecs *ffmpeg* supports, run this command in a terminal:

```
ffmpeg -decoders
```

Firefox may only play the corresponding AAC audio codec if the operating system supports it, see https://caniuse.com/aac.
All other browsers shouldn't have any issues.

HEVC video files can have a `.mp4` file extension too, which is typically associated with AVC. This is because MP4 is
a *container* format or wrapper - the content could be compressed with H.264, H.265, or something else. The file
extension doesn't really tell you anything other than that it's probably a video file.

!!! info
    While the QuickTime `.mov` container format served as the basis for MPEG-4,
    there are differences and the two are not quite interchangeable. They still
    play in most browsers and won't be transcoded automatically for this reason.

## Containers ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers

## Codecs ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs
