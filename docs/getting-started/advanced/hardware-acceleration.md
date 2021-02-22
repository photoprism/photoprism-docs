# Hardware Accelerated Video Transcoding

*Note: This is contributed content and may be outdated. Click the edit link
to my perform changes and send a pull request.*

The encoder to be used by FFmpeg when transcoding videos can be configured within `docker-compose.yml`  

In the example below, `h264_v4l2m2m` is set to enable experimental hardware accelerated encoding of h264 video. 
```yaml
PHOTOPRISM_FFMPEG_ENCODER: "h264_v4l2m2m"    # FFmpeg AVC encoder for video transcoding (default: libx264)
```

!!! info 
    Some server configurations, specifically Raspberry Pi's, may run into memory allocation issues when using hardware acceleration. 
    Monitor your server logs carefully and increase available GPU and/or CMA memory allocations if necessary. 
    

Additional advanced configuration options exist:
```yaml
PHOTOPRISM_FFMPEG_BUFFERS: "64"              # FFmpeg capture buffers (default: 32)
```

!!! warning
    Hardware accelerated transcoding within Photoprism is currently experimental.
    It may not work on all server configurations.
    Some users report unexpected hangs in the FFmpeg process when attempting to transcoding large video files. 
