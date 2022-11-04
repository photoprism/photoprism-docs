# Video Transcoding

*Note: This content is intended for advanced users only. You can contribute by clicking :material-pencil: to send a pull request with your changes.*

## AVC Encoders

The encoder used by FFmpeg can be configured with `PHOTOPRISM_FFMPEG_ENCODER` in your `docker-compose.yml` config file:

| Encoder                    | Value       |
|----------------------------|-------------|
| Software H.264             | `software`  | 
| Apple Video Toolbox        | `apple`     | 
| Intel Quick Sync           | `intel`     | 
| NVIDIA H.264               | `nvidia`    | 
| Raspberry Pi / Video4Linux | `raspberry` | 
| Video Acceleration API     | `vaapi`     | 

It defaults to `software` if no value is set or hardware transcoding fails. Please refer to the [FFmpeg documentation](https://trac.ffmpeg.org/wiki/HWAccelIntro) for a full list of encoders and their implementation status. We welcome contributions to support additional encoders.

!!! tldr ""
    For transcoding to work, FFmpeg must be enabled and installed. When using our Docker images, it is already pre-installed. In addition, the service must have permission to use the related video devices. This depends on your hardware and operating system, so we can only give you examples that may need to be changed to work for you.

## GPU Drivers

Depending on your hardware, it may be necessary to install additional packages for FFmpeg to use the AVC encoding device. One way to do this is to set `PHOTOPRISM_INIT` to `"gpu tensorflow"` when using our Docker images. Note this is experimental and currently only required for *Intel HD Graphics i915* hardware. For example, if you use the *NVIDIA Container Toolkit*, as described below, you don't need to set the `gpu` target. See the [related installation script on GitHub](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-gpu.sh) for details. We welcome contributions to support additional devices or update package names if needed.

!!! tldr ""
    Most users can either skip `PHOTOPRISM_INIT` completely or just use `PHOTOPRISM_INIT: "tensorflow"` to install a special version of TensorFlow that improves indexing performance if your server CPU supports AVX, a technology unrelated to video transcoding.

## NVIDIA Container Toolkit

For hardware transcoding with an NVIDIA graphics card, the NVIDIA Container Toolkit must be installed on the host computer first. Instructions can be found in their [installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

### Docker Compose

At the same level as the volumes, add the `deploy` section and then restart all services for the changes to take effect:

```yaml
services:
  photoprism:
    # --- cut out for brevity ---
    environment:
      PHOTOPRISM_FFMPEG_ENCODER: "nvidia"
      PHOTOPRISM_INIT: "tensorflow"
      NVIDIA_VISIBLE_DEVICES: "all"
      NVIDIA_DRIVER_CAPABILITIES: "compute,video,utility"
    # --- cut out for brevity ---
    volumes:
      - ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: "nvidia"
              count: 1
              capabilities: [gpu]
    # --- cut out for brevity ---    
```

## Raspberry Pi

Experimental hardware-accelerated transcoding on a Raspberry Pi (and compatible devices) can be enabled by choosing the `raspberry` encoder:

```yaml
PHOTOPRISM_FFMPEG_ENCODER: "raspberry"
```

The Docker container must also have access to one or more video devices.  For the `raspberry` encoder, for example, you add:

```yaml
devices:
 - "/dev/video11:/dev/video11"
```

Additional advanced configuration options are available to improve stability if needed:

```yaml
PHOTOPRISM_FFMPEG_BUFFERS: "64" # FFmpeg capture buffers (default: 32)
```

!!! info ""
    Some server configurations, especially Raspberry Pi's, may experience memory allocation issues when using hardware acceleration. Carefully monitor your server's logs and increase the available GPU and/or CMA memory allocations if necessary.
