# Video Transcoding

## AVC Encoders

The encoder used by FFmpeg can be configured with [`PHOTOPRISM_FFMPEG_ENCODER`](../config-options.md#file-conversion) in your `compose.yaml` or `docker-compose.yml` config file:

| Encoder                    | Value       |
|----------------------------|-------------|
| Software H.264             | `software`  |
| Apple Video Toolbox        | `apple`     |
| Intel Quick Sync           | `intel`     |
| NVIDIA H.264               | `nvidia`    |
| Raspberry Pi / Video4Linux | `raspberry` |
| Video Acceleration API     | `vaapi`     |
| Vulkan Video Extensions    | `vulkan`    |

It defaults to `software` if no value is set or hardware transcoding fails. Please refer to the [FFmpeg documentation](https://trac.ffmpeg.org/wiki/HWAccelIntro) for a full list of encoders and their implementation status. We welcome contributions to support additional encoders.

!!! tldr ""
    For video transcoding to work, FFmpeg must be enabled and installed. When using our Docker images, it is already pre-installed. In addition, the service must have permission to use the related video devices. This depends on your hardware and operating system, so we can only give you examples that may need to be changed to work for you.

### Size Limit ###

The [`PHOTOPRISM_FFMPEG_SIZE`](../config-options.md#file-conversion) config option allows to limit the resolution of transcoded videos. It accepts the following standard sizes, while other values are automatically adjusted to the next supported size:

| Size | Usage             |
|------|-------------------|
| 720  | SD TV, Mobile     |
| 1280 | HD TV, SXGA       |
| 1920 | Full HD           |
| 2048 | DCI 2K, Tablets   |
| 2560 | Quad HD           |
| 3840 | 4K Ultra HD       |
| 4096 | DCI 4K, Retina 4K |
| 7680 | 8K Ultra HD 2     |

!!! tldr ""
    When transcoding videos, the original aspect ratio is maintained and smaller videos will not be upscaled.
    
!!! tldr ""
    Note that MPEG-4 AVC videos are not re-encoded if they exceed the configured resolution limit.

### Bitrate Limit ###

You can limit the bitrate of the AVC encoder with the config option [`PHOTOPRISM_FFMPEG_BITRATE`](../config-options.md#file-conversion). Keep in mind that this is a "soft limit", so the actual bitrate varies and depends on the encoder used as well as the specific FFmpeg parameters, which in turn depend on the encoder. It may also depend on the operating system and the GPU drivers.

If the bitrate is significantly exceeded in your environment and you want improvements to be implemented, we recommend that you [take a look at the FFmpeg documentation](https://trac.ffmpeg.org/wiki/Limiting%20the%20output%20bitrate) and the [parameters in our source code](https://github.com/photoprism/photoprism/blob/develop/internal/ffmpeg/transcode_cmd.go) so you can tell us which parameters should be changed to make it work for you.

Note that MPEG-4 AVC videos are not re-encoded if they exceed the [configured bitrate limit](../config-options.md#file-conversion). To reduce the size of AVC videos, you can manually replace the original files with a smaller version or wait for a future release that offers this functionality.

!!! tldr ""
    Already transcoded video files are not automatically re-transcoded when the limit is changed. To do this, you must manually remove the `*.avc` files in the `sidecar` [storage folder](../docker-compose.md#photoprismstorage) and run the `photoprism convert` command [in a terminal](../docker-compose.md#opening-a-terminal).

## Software Transcoding ##

Unless you have a lot of high-resolution videos in your library, we recommend keeping the default settings to use the standard software codec for video transcoding. It has a high quality and does not require any special permissions or additional drivers.

Our current [Docker image](https://docs.photoprism.app/release-notes/#march-5-2026) is based on [Ubuntu 25.10](https://packages.ubuntu.com/questing/ffmpeg), which already includes FFmpeg 7.x from the distribution packages. If you want to try a newer upstream static build, you can add `PHOTOPRISM_INIT: "ffmpeg"` to the environment section of your `compose.yaml` or `docker-compose.yml` file:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_INIT: "ffmpeg"
```

Internally, the `ffmpeg` init target installs the current BtbN stable build, equivalent to the `latest` channel in our [`install-ffmpeg.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-ffmpeg.sh) script. At the moment, this updates the preinstalled distro version to FFmpeg 8.0.

You can also install the nightly (master) build instead, which may include newer features and bug fixes that have not yet been included in a stable release:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_INIT: "ffmpeg-master"
```

The `ffmpeg-master` init target maps to the script's `master` channel and installs the latest nightly archive from BtbN.

Note that these static builds cannot be used with hardware transcoding and that they may [support a different set](https://github.com/BtbN/FFmpeg-Builds) of [file formats](https://www.photoprism.app/kb/file-formats).

## GPU Drivers

Depending on your hardware, it may be necessary to install additional packages for FFmpeg to use the AVC encoding device. 

One way to do this automatically is to set `PHOTOPRISM_INIT` to `"gpu tensorflow"` when using our Docker images. Note that this is experimental and not required for most encoders.

See the [related installation script on GitHub](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-gpu.sh) for details. We welcome contributions to support additional devices or update package names if needed.

!!! tldr ""
    Most users can either skip `PHOTOPRISM_INIT` completely or just use `PHOTOPRISM_INIT: "tensorflow"` to install a special version of TensorFlow that improves indexing performance if the server CPU supports AVX, which is independent of video transcoding and the type of GPU.

### Intel Quick Sync

To enable *Intel Quick Sync* hardware video transcoding, add the `intel` target to `PHOTOPRISM_INIT`, choose the `intel` encoder, and share the `/dev/dri` devices with the `photoprism` service:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_FFMPEG_ENCODER: "intel"
      PHOTOPRISM_INIT: "intel"
      ...
    devices:
      - "/dev/dri:/dev/dri"
    volumes:
      - ...
```

In addition, you can choose to run the `photoprism` service as a non-root user by setting either the `user` [service property](https://docs.docker.com/reference/compose-file/services/#user) or the `PHOTOPRISM_UID` and `PHOTOPRISM_GID` [environment variables](../config-options.md#docker-image) in your `compose.yaml` or `docker-compose.yml` file:

| Environment    | Default | Description                                                                                                                                                                                  |
|----------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_UID | 0       | run as a non-root user after initialization (supported: 0, 33, 50-99, 500-600, 900-1250, and 2000-2100)                                                                                      |
| PHOTOPRISM_GID | 0       | run with a specific group id after initialization, can optionally be used together with `PHOTOPRISM_UID` (supported: 0, 33, 44, 50-99, 105, 109, 115, 116, 500-600, 900-1250, and 2000-2100) |

*Which user and group you choose should depend on the owner of the `/dev/dri` video device so that the service has permission to access it.*

Finally, remember to [update the file permissions and/or owner](../troubleshooting/docker.md#file-permissions) with the `chmod` and `chown` commands when you make changes to the UID or GID, and [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

!!! info ""
    Older Intel hardware may not support certain [video codecs and resolutions](https://en.wikipedia.org/wiki/Intel_Quick_Sync_Video#Development). In this case, it is not possible to use hardware transcoding for these videos. We may later add a configuration option that allows you to downscale videos.

### NVIDIA Container Toolkit

For hardware transcoding with an NVIDIA graphics card, the *NVIDIA Container Toolkit* must be installed on the host computer first. Instructions can be found in their [installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

Once the toolkit is installed, choose the `nvidia` encoder and [add a `deploy` section](https://docs.docker.com/compose/how-tos/gpu-support/) to the `photoprism` service:

```yaml
services:
  photoprism:    
    environment:
      PHOTOPRISM_FFMPEG_ENCODER: "nvidia"
      PHOTOPRISM_INIT: "tensorflow-gpu"
      NVIDIA_VISIBLE_DEVICES: "all"
      NVIDIA_DRIVER_CAPABILITIES: "all"
      ...
    volumes:
      - ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: "nvidia"
              capabilities: [gpu]
              count: 1
    ...
```

Now [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

Should PhotoPrism fail to start after this due to *unsupported instructions*, your CPU may not have the capabilities to use the GPU-optimized version of TensorFlow. In this case, you will need to change `PHOTOPRISM_INIT: "tensorflow-gpu"` to `PHOTOPRISM_INIT: "tensorflow"` in your configuration and then recreate the service containers, so that a CPU-only version is installed:

```bash
docker compose stop
docker compose up -d --force-recreate
```

The GPU-optimized version of TensorFlow that [`PHOTOPRISM_INIT`](../config-options.md#docker-image) installs is the same as the one you get at [tensorflow.org/install/lang_c](https://www.tensorflow.org/install/lang_c), so you can refer to their website/documentation for more information, e.g. which GPUs/drivers are supported. Using a GPU-optimized version of TensorFlow is *optional* and has no impact on video transcoding capabilities or performance.

!!! info ""
    We also provide a [ready-to-use `compose.yaml` example](https://dl.photoprism.app/docker/nvidia/compose.yaml) for your convenience.
    Note that older hardware may not support certain [video codecs and resolutions](https://en.wikipedia.org/wiki/Nvidia_NVENC#Versions).

### Raspberry Pi

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

Now [restart the services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

!!! info ""
    Some server configurations, especially Raspberry Pi's, may experience memory allocation issues when using hardware acceleration. Carefully monitor your server's logs and increase the available GPU and/or CMA memory allocations if necessary. Note that the Raspberry Pi hardware currently only supports video resolutions up to 2160p.

### Vulkan

Vulkan-based hardware transcoding works on any GPU that implements the Vulkan video encode extensions. This currently covers recent AMD GPUs (RDNA 2 and later) and Intel GPUs (11th-generation and later) via the open Mesa drivers, as well as NVIDIA Turing-and-later cards through the proprietary driver. The encoder requires FFmpeg 8 or later; this is included in the `:preview` Docker image and will be part of the next stable release. If you are on a stable image with FFmpeg 7, add `PHOTOPRISM_INIT: "ffmpeg"` to install a newer upstream build first.

To enable Vulkan transcoding, choose the `vulkan` encoder and share `/dev/dri` with the `photoprism` service. NVIDIA users should instead follow the [NVIDIA Container Toolkit](#nvidia-container-toolkit) setup and make sure `NVIDIA_DRIVER_CAPABILITIES` includes the `video` capability (the `"all"` value used in our example already does):

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_FFMPEG_ENCODER: "vulkan"
      PHOTOPRISM_INIT: "gpu"
      ...
    devices:
      - "/dev/dri:/dev/dri"
    group_add:
      - "44"  # host "video" group
      - "108" # host "render" group
```

Adjust the IDs in `group_add` to match the owners of `/dev/dri/renderD*` and `/dev/dri/card*` on your host (run `getent group video render` to see the numbers). Now [restart the services](../docker-compose.md#step-2-start-the-server) for the changes to take effect:

```bash
docker compose stop
docker compose up -d
```

If a Vulkan device cannot be opened at runtime — for example on a GPU without the required video extensions — PhotoPrism logs a warning and automatically falls back to the software encoder, so no manual recovery is required.

!!! info ""
    The Vulkan encoder is a preview feature available in the [`:preview`](../updates.md#development-preview) Docker image and will be part of the next stable release. The image already includes the Vulkan loader (`libvulkan1`); vendor-specific Vulkan instance class drivers — [`mesa-vulkan-drivers`](https://packages.ubuntu.com/questing/mesa-vulkan-drivers) for AMD and Intel, or the proprietary NVIDIA Vulkan driver — may need to be added to the container until `PHOTOPRISM_INIT: "gpu"` is updated to provision them automatically.

## Other Hardware

If you want to use other hardware for transcoding, choose the appropriate AVC encoder and share the required devices with the `photoprism` service, as shown in the examples above. Then [restart the services](../docker-compose.md#step-2-start-the-server) for the changes to take effect.

Which devices need to be shared and whether additional drivers are required depends on your specific hardware. For more information, see the [FFmpeg documentation](https://ffmpeg.org/ffmpeg-devices.html).

## Troubleshooting

### Enabling Trace Log Mode

A good way to troubleshoot configuration issues is to increase the log level. To enable [trace log mode](../config-options.md), set `PHOTOPRISM_LOG_LEVEL` to `"trace"` in the `environment:` section of the `photoprism` service (or use the `--trace` flag when running the `photoprism` command directly):


```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_LOG_LEVEL: "trace"
      ...
```

Then [restart all services](../docker-compose.md#step-2-start-the-server) for your changes to take effect:

```bash
docker compose stop
docker compose up -d
```

### Viewing Docker Service Logs

You can run this command to check the server logs for warnings and errors, including the last 100 messages (omit `--tail=100` to see them all, and `-f` to output only the last logs without watching them):

```bash
docker compose logs -f --tail=100 
```

[Learn more ›](../troubleshooting/docker.md#viewing-logs)

!!! tldr ""
    If [FFmpeg is disabled](../config-options.md#feature-flags) or not installed, videos cannot be indexed because still images cannot be created.
    You should also have [ExifTool enabled](../config-options.md#feature-flags) to extract metadata such as duration, resolution, and codec.
    Note that your hardware may not support certain video codecs and resolutions. In this case, the software encoder is used automatically.

!!! tldr ""
    Our examples use the new `docker compose` command by default. If your server does not yet support it, you can still use `docker-compose` or alternatively `podman-compose` on Red Hat-compatible distributions.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.
