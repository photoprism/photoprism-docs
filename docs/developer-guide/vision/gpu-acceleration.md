# GPU Acceleration

**Last Updated:** October 5, 2026

PhotoPrism can run its built-in ONNX models on an NVIDIA GPU through the [ONNX Runtime](https://onnxruntime.ai/) CUDA execution provider. This covers image classification, NSFW detection, and face detection and embeddings. Thumbnail generation, image decoding, metadata extraction, and database work stay on the CPU, so the overall gain is smaller than the speedup of a single model.

## CUDA Images

The CUDA images are amd64-only variants of our Plus and Pro images that include the GPU build of ONNX Runtime together with the CUDA runtime libraries and cuDNN:

| Image                   | Release Tags             | Preview Tag    |
|-------------------------|--------------------------|----------------|
| `photoprism/photoprism` | `cuda`, `YYMMDD-cuda`    | `preview-cuda` |
| `photoprism/pro`        | `cuda`, `1.YYMM.DD-cuda` | `preview-cuda` |

They are about 1.7 GB larger than the regular images and preset `PHOTOPRISM_ONNX_PROVIDER` to `cuda` and `NVIDIA_DRIVER_CAPABILITIES` to `compute,utility,video`, so ONNX inference and [NVENC video transcoding](../../getting-started/advanced/transcoding.md) can both use the GPU once one is assigned to the container.

Do not add `onnxruntime` or `onnxruntime-gpu` to `PHOTOPRISM_INIT` when using these images: the first installs the CPU build of ONNX Runtime, which then takes precedence over the GPU build, and the second reinstalls the libraries the image already contains each time the container is created.

## Requirements

- An NVIDIA GPU with the proprietary driver installed on the host
- The [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- A device reservation for the `photoprism` service in your `compose.yaml`:

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

The image does not set `NVIDIA_VISIBLE_DEVICES`, so the container only gets the GPUs it reserves.

## Regular Images

With the regular images, `PHOTOPRISM_INIT: "onnxruntime-gpu"` installs the GPU build of ONNX Runtime together with the CUDA libraries and cuDNN when the container starts. Set `PHOTOPRISM_ONNX_PROVIDER: "cuda"` as well, since the regular images run inference on the CPU by default. The host requirements are the same.

## Checking That the GPU Is Used

When a model is loaded, PhotoPrism logs a `loading <model> on the <provider>` line naming the execution provider. If the CUDA provider cannot be used, for example because no GPU is assigned to the container or the driver is too old, PhotoPrism logs one warning that the execution provider is unavailable and runs inference on the CPU instead. It does not switch to the GPU later on its own; restart PhotoPrism after fixing the cause.

## Performance

How much a GPU helps depends on the GPU **and** the CPU it is compared with. Measured with a `pro:preview-cuda` build in October 2026, on a library with 2,414 photos and 283 videos:

| Step                           | RTX 4060 | i7-14700 (CPU only) | Speedup |
|--------------------------------|----------|---------------------|---------|
| `photoprism index`             | 658 s    | 1,194 s             | 1.8x    |
| `vision run -m labels --force` | 106 s    | 178 s               | 1.7x    |
| `vision run -m nsfw --force`   | 62 s     | 83 s                | 1.3x    |
| `vision run -m face --force`   | 159 s    | 178 s               | 1.1x    |

The results were identical with and without the GPU. An entry-level NVIDIA T400 gave no measurable gain over an Intel Core i5-13500T in the same test, since image decoding on the CPU dominates there.

## Memory

GPU memory use grows with the number of [index workers](../../getting-started/config-options.md#indexing) running inference at the same time: with 14 workers, PhotoPrism used about 6 GB of VRAM on the RTX 4060, and about 2.3 GB during a single `vision run`. If Ollama shares the GPU, reduce the number of index workers or use a card with more memory.
