# Videos #

PhotoPrism may use [*ffmpeg*](https://www.ffmpeg.org/documentation.html) to transcode 
common video formats to [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4).
This container / codec combination doesn't require transcoding as it can be played 
natively by most modern browsers, see https://caniuse.com/mpeg4.

OGV, VP8, VP9, AV1, WebM and HEVC videos will be streamed directly in case they are supported by your browser and if they do not exceed the configured [bitrate limit](../../getting-started/config-options.md#file-converters). 
Otherwise those formats will be transcoded as well.


For a list of codecs *ffmpeg* supports, run this command in a terminal:

```
ffmpeg -decoders
```

Please note:

1. Not all [video and audio formats](https://caniuse.com/?search=video%20format) can be [played with every browser](../../getting-started/troubleshooting/browsers.md). For example, [AAC](https://caniuse.com/aac "Advanced Audio Coding") - the default audio codec for [MPEG-4 AVC / H.264](https://caniuse.com/avc "Advanced Video Coding") - is supported natively in Chrome, Safari, and Edge, while it is only optionally supported by the OS in Firefox and Opera.
2. HEVC/H.265 video files can have a `.mp4` file extension too, which is often associated with AVC only. This is because MP4 is a *container* format, meaning that the actual video content may be compressed with H.264, H.265, or something else. The file extension doesn't really tell you anything other than that it's probably a video file.

!!! info
    While the QuickTime `.mov` container format served as the basis for MPEG-4,
    there are differences and the two are not quite interchangeable. They still
    play in most browsers and won't be transcoded automatically for this reason.

## Containers ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers

## Codecs ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs

*[HEVC]: High Efficiency Video Coding / H.265