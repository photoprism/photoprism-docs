# Video File Support

For maximum browser compatibility, PhotoPrism can transcode video codecs and containers [supported by FFmpeg](https://www.ffmpeg.org/documentation.html) to [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4), as well as extract still images for thumbnail creation:

- if [FFmpeg is disabled](../../getting-started/config-options.md#feature-flags) or not installed, indexing and importing videos is not possible because still images cannot be created
- if [Exiftool is disabled](../../getting-started/config-options.md#feature-flags) or not installed, indexing and importing videos is only partially possible because the video metadata cannot be extracted and thus the duration, resolution, and codec are unknown
- [MPEG-4 AVC](https://en.wikipedia.org/wiki/MPEG-4) videos can be [played natively by most modern browsers](https://caniuse.com/mpeg4) and are not re-encoded, even if they exceed the [configured bitrate limit](../../getting-started/advanced/transcoding.md#bitrate-limiting); to reduce the size of AVC videos, you can manually replace the original files with a smaller version or wait for a future release that offers this functionality
- OGV, VP8, VP9, AV1, WebM, and HEVC videos will be streamed directly if they are supported by your browser and do not exceed the [configured bitrate limit](../../getting-started/advanced/transcoding.md#bitrate-limiting)
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

## Resolutions

The [`PHOTOPRISM_FFMPEG_SIZE`](../../getting-started/config-options.md#file-converters) config option allows to limit the resolution of [transcoded videos](../../getting-started/advanced/transcoding.md). It accepts the following standard sizes, while other values are automatically adjusted to the next supported size:

| Size |       Usage        |
|------|--------------------|
|  720 | SD TV, Mobile      |
| 1280 | HD TV, SXGA        |
| 1920 | Full HD            |
| 2048 | DCI 2K, Tablets    |
| 2560 | Quad HD, Notebooks |
| 3840 | 4K Ultra HD        |
| 4096 | DCI 4K, Retina 4K  |
| 7680 | 8K Ultra HD 2      |

## Technical References and Tutorials

| Title                               | URL                                                                         |
|-------------------------------------|-----------------------------------------------------------------------------|
| Web Video Codec Guide               | https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs     |
| Web Video Content-Type Headers      | https://developer.mozilla.org/en-US/docs/Web/Media/Formats/codecs_parameter |
| Media Container Formats             | https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers       |
| MP4 Signature Format                | https://www.file-recovery.com/mp4-signature-format.htm                      |
| List of file signatures (Wikipedia) | https://en.wikipedia.org/wiki/List_of_file_signatures                       |
| How to use the io.Reader interface  | https://yourbasic.org/golang/io-reader-interface-explained/                 |
| AV1 Codec ISO Media File Format     | https://aomediacodec.github.io/av1-isobmff                                  |

## Hybrid Photo/Video Formats

For more information on hybrid photo/video file formats, e.g. Apple Live Photos and Samsung/Google Motion Photos, see [/developer-guide/media/live/](live.md).

*[HEVC]: High Efficiency Video Coding / H.265