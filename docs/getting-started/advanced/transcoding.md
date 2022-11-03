# Video Transcoding

*Note: This is contributed content intended for advanced users. You can contribute by clicking :material-pencil: to send a pull request with your changes.*

The encoder used by FFmpeg can be configured within your `docker-compose.yml` config file.  

Experimental hardware accelerated transcoding on a Raspberry Pi (and compatible devices)
may be enabled using the `h264_v4l2m2m` encoder:

```yaml
PHOTOPRISM_FFMPEG_ENCODER: "h264_v4l2m2m"
```

It defaults to `libx264` if no value is set or transcoding with `h264_v4l2m2m` fails.

Please refer to the [official documentation](https://trac.ffmpeg.org/wiki/HWAccelIntro)
for a full list of encoders and their implementation status.

!!! info 
    Some server configurations, specifically Raspberry Pi's, may run into memory 
    allocation issues when using hardware acceleration. 
    Monitor your server logs carefully and increase available GPU and/or CMA memory 
    allocations if necessary. 

The Docker container will also need access to one or more video devices.
For the `h264_v4l2m2m` encoder on a Raspberry Pi, also add:
```yaml
devices:
 - "/dev/video11:/dev/video11"
```

Additional advanced configuration options:

```yaml
PHOTOPRISM_FFMPEG_BUFFERS: "64" # FFmpeg capture buffers (default: 32)
```

!!! warning
    Hardware accelerated transcoding within Photoprism is currently experimental.
    It may not work on all server configurations.
    Some users report unexpected hangs in the FFmpeg process when attempting to 
    transcode large video files. 

## Using the Nvidia Container Toolkit

This involves installing a toolkit on the host machine. For instructions for your chosen distro please refer to [Nvidia Container Toolkit Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

### Docker Compose file setup for Nvidia Container Toolkit

On the same level as volumes, place the `deploy` section and re-create your containers.

```yaml
# --- cut out for brevity ---
volumes:
  # "/host/folder:/photoprism/folder"                # Example
  - "/photoprism/originals/:/photoprism/originals"   # Original media files (DO NOT REMOVE)
  # - "/example/family:/photoprism/originals/family" # *Additional* media folders can be mounted like this
  - "/photoprism/import:/photoprism/import"          # *Optional* base folder from which files can be imported to originals
  - "/photoprism/data:/photoprism/storage"           # *Writable* storage folder for cache, database, and sidecar files (DO NOT REMOVE)
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
# --- cut out for brevity ---    
```

