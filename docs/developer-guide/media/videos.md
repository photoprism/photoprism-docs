# Videos #

For maximum browser compatibility, PhotoPrism can transcode video codecs and containers [supported by FFmpeg](https://www.ffmpeg.org/documentation.html) to [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4), as well as extract still images for thumbnail creation:

- if [FFmpeg is disabled](../../getting-started/config-options.md#feature-flags) or not installed, indexing and importing videos is not possible because still images cannot be created
- if [Exiftool is disabled](../../getting-started/config-options.md#feature-flags) or not installed, indexing and importing videos is only partially possible because the video metadata cannot be extracted and thus the duration, resolution, and codec are unknown
- [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4) doesn't require transcoding as it can be played natively by most modern browsers, see https://caniuse.com/mpeg4
- OGV, VP8, VP9, AV1, WebM, and HEVC videos can be streamed directly if they are supported by your browser and do not exceed the [configured bitrate limit](../../getting-started/config-options.md#file-converters)
- other formats must always be transcoded

You can view a list of codecs that FFmpeg supports by executing this command in a terminal:

```
ffmpeg -decoders
```

Our setup guide for advanced users explains how to [configure hardware video transcoding](../../getting-started/advanced/transcoding.md).

Please note:

1. Not all [video and audio formats](https://caniuse.com/?search=video%20format) can be [played with every browser](../../getting-started/troubleshooting/browsers.md). For example, [AAC](https://caniuse.com/aac "Advanced Audio Coding") - the default audio codec for [MPEG-4 AVC / H.264](https://caniuse.com/avc "Advanced Video Coding") - is supported natively in Chrome, Safari, and Edge, while it is only optionally supported by the OS in Firefox and Opera.
2. HEVC/H.265 video files can have a `.mp4` file extension too, which is often associated with AVC only. This is because MP4 is a *container* format, meaning that the actual video content may be compressed with H.264, H.265, or something else. The file extension doesn't really tell you anything other than that it's probably a video file.

!!! info ""
    Although the QuickTime `.mov` container format served as the basis for MPEG-4, there are differences and the two are not strictly interchangeable. Nevertheless, they can be played in most browsers and are not automatically transcoded for this reason.

!!! tldr ""
    In case [FFmpeg is disabled](../../user-guide/settings/advanced.md#disable-ffmpeg) or not installed, videos cannot be indexed because still images cannot be created.
    You should also have [Exiftool enabled](../../getting-started/config-options.md#feature-flags) to extract metadata such as duration, resolution, and codec.   

## Containers ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers

## Codecs ##

- https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs

*[HEVC]: High Efficiency Video Coding / H.265