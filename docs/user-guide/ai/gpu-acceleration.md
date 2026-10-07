# GPU Acceleration

If your server has an NVIDIA graphics card, PhotoPrism can use it to run its built-in AI models for image classification, NSFW detection, and face recognition. This makes indexing faster, while image decoding and thumbnail generation still run on the CPU.

## Setup

Our `cuda` images include everything PhotoPrism needs to use an NVIDIA GPU. They are available for 64-bit Intel and AMD processors only:

| Edition                      | Image                        |
|------------------------------|------------------------------|
| PhotoPrism & PhotoPrism Plus | `photoprism/photoprism:cuda` |
| PhotoPrism Pro               | `photoprism/pro:cuda`        |

In addition, you need:

- an NVIDIA GPU with the proprietary driver installed on your server
- the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

Then change the image of the `photoprism` service in your `compose.yaml` and assign the GPU to it, as shown in the example below:[^1]

```yaml
services:
  photoprism:
    image: photoprism/photoprism:cuda
    deploy:
      resources:
        reservations:
          devices:
            - driver: "nvidia"
              capabilities: [gpu]
              count: 1
```

Finally, run `docker compose pull` and `docker compose up -d` to apply the changes. The `cuda` images are about 1.7 GB larger than our regular images.

!!! info ""
    Do not add `onnxruntime` or `onnxruntime-gpu` to `PHOTOPRISM_INIT` when using a `cuda` image, as the image already includes the required libraries.

## Checking That the GPU Is Used

When PhotoPrism loads a model, it logs a line that names the execution provider it runs on. If the GPU cannot be used, for example because it was not assigned to the container, PhotoPrism logs a warning and uses the CPU instead. Once you have fixed the cause, restart PhotoPrism so that it tries the GPU again.

The `cuda` images also allow [hardware video transcoding](../../getting-started/advanced/transcoding.md) with NVIDIA, which you can enable with `PHOTOPRISM_FFMPEG_ENCODER: "nvidia"`.

## What to Expect

How much faster indexing gets depends on your GPU **and** your CPU. With an NVIDIA GeForce RTX 4060, indexing a library of about 2,400 photos was 1.8 times faster than with an Intel Core i7-14700 alone, with identical results. An entry-level card such as an NVIDIA T400 ran the AI models no faster than a recent CPU.

During indexing, PhotoPrism used up to about 6 GB of GPU memory on the RTX 4060. If you also run [Ollama](using-ollama.md) on the same card, it may not have enough memory left for its model, so consider reducing the number of [index workers](../../getting-started/config-options.md#indexing).

[Learn more ›](../../developer-guide/vision/gpu-acceleration.md)

[^1]: Unrelated configuration details have been omitted for brevity.
