# Face Recognition

**Last Updated:** June 28, 2026

To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism uses a multi-stage AI pipeline that detects faces, generates embeddings, and clusters similar faces so they can be easily organized by person.

!!! tldr ""
    The canonical engineering reference for this pipeline is the package README at [`internal/ai/face/README.md`](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md). This page summarizes the developer-facing behavior; consult the README for the latest thresholds, benchmarks, and test recipes.

## How It Works

The face recognition pipeline runs in three stages:

1. **Detection** — the ONNX SCRFD detector locates faces in the 720 px thumbnail of each photo (see [Thumbnails](../media/thumbnails.md) for how thumbnails are generated with libvips).
2. **Embedding** — TensorFlow generates a 512-dimensional vector for each face based on [FaceNet](https://dl.photoprism.app/pdf/publications/20150101-FaceNet.pdf).
3. **Clustering** — similar embeddings are grouped with the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) so clusters can be assigned to people.

## Detection Engine

As of the [April 2026 release](../../release-notes.md), PhotoPrism ships a **single face detector** — the legacy Pigo cascade classifier has been removed from the code base.

**ONNX SCRFD 0.5g** is an [ONNX Runtime](https://onnxruntime.ai/)-backed CNN that delivers higher recall on occluded, off-axis, or poorly-lit faces than the previous Pigo detector. Implementation details:

- Consumes 720 px thumbnails with a 640 px model input.
- Scheduled on the meta/vision workers, in lock-step with the FaceNet embedding step.
- Defaults to half the available CPUs (minimum 1 thread).
- The prebuilt runtime targets glibc ≥ 2.27 on `amd64` / `arm64`.
- When `FACE_ENGINE=auto` the detector is used whenever the bundled SCRFD model is present; otherwise detection is **disabled** rather than falling back to a legacy engine.

For backwards compatibility, legacy `FACE_ENGINE=pigo` values are silently mapped to ONNX in [`internal/ai/face/engine.go:ParseEngine`](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/engine.go) so older configuration files keep working after upgrade. New configurations should use `auto`, `onnx`, or `none`.

### Hardware Acceleration

The ONNX detector currently runs on the **CPU execution provider only**. PhotoPrism configures the inference session with thread counts and full graph optimization but does not append a hardware-accelerated execution provider, so detection throughput scales with `FACE_ENGINE_THREADS` and the host CPU rather than a GPU. The prebuilt runtime is the CPU build of [ONNX Runtime](https://onnxruntime.ai/), installed via [`scripts/dist/install-onnx.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-onnx.sh) from our download server.

Optional hardware acceleration is being tracked for future releases as **opt-in** paths; CPU remains the default so existing installs are unaffected:

- **NVIDIA / CUDA (Linux)** — offloads detection to an NVIDIA GPU through the ONNX Runtime CUDA execution provider. It requires the GPU build of ONNX Runtime, the NVIDIA driver, and — for Docker — the NVIDIA Container Toolkit plus a matching CUDA and cuDNN runtime in the image (these NVIDIA libraries are not part of the ONNX Runtime archive). Tracked in [photoprism/photoprism#5703](https://github.com/photoprism/photoprism/issues/5703).
- **Apple / CoreML (native macOS builds)** — offloads to the Apple Neural Engine and GPU through the CoreML execution provider, which is already compiled into the macOS build of ONNX Runtime. This benefits **natively built** macOS binaries only: the standard Docker image runs inside a Linux VM on macOS with no Apple-accelerator passthrough, so it stays CPU-only regardless. Tracked in [photoprism/photoprism#5704](https://github.com/photoprism/photoprism/issues/5704).

## Configuration

!!! example ""
    We recommend that only advanced users and developers change these parameters. All face-related environment variables and CLI flags are listed in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition); this page only highlights the knobs most relevant to detector behavior.

### Detection Settings

| Environment Variable           | CLI Flag              | Default                 | Description                                                                                 |
|--------------------------------|-----------------------|-------------------------|---------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_ENGINE         | --face-engine         | auto                    | Detection engine (`auto`, `onnx`, `none`). Legacy `pigo` is accepted and aliased to `onnx`. |
| PHOTOPRISM_FACE_ENGINE_THREADS | --face-engine-threads | runtime.NumCPU()/2 (≥1) | Number of ONNX inference threads.                                                           |
| PHOTOPRISM_FACE_SIZE           | --face-size           | 50                      | Minimum face size in `PIXELS` (20-10000).                                                   |
| PHOTOPRISM_FACE_SCORE          | --face-score          | 9.0                     | Base quality threshold before scale-dependent offsets are added.                            |
| PHOTOPRISM_FACE_OVERLAP        | --face-overlap        | 42                      | Maximum allowed IoU when deduplicating markers (preserved from legacy behavior).            |

Run scheduling is configured through the face model entry in `vision.yml`; `FaceEngineRunType()` simply forwards to `vision.Config.RunType(ModelTypeFace)`. There is no separate `FACE_ENGINE_RUN` flag. See the [package README](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md#configuration-summary) for the full run-mode semantics.

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run `photoprism faces reset` in a terminal to remove existing clusters and markers after changing any of the clustering parameters, otherwise inconsistencies may cause unexpected behavior or errors.

| Environment Variable          | CLI Flag             | Default | Description                                                              |
|-------------------------------|----------------------|---------|--------------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  | 80      | Minimum size of automatically clustered faces in `PIXELS` (20-10000).    |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score | 15      | Minimum `QUALITY` score of automatically clustered faces (1-100).        |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  | 4       | `NUMBER` of faces forming a cluster core (1-100).                        |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | 0.64    | Similarity `DISTANCE` of faces forming a cluster core (0.1-1.5).         |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | 0.46    | Similarity `OFFSET` for matching faces with existing clusters (0.1-1.5). |

Additional merge-tuning knobs (`PHOTOPRISM_FACE_MERGE_MAX_RETRY`, `PHOTOPRISM_FACE_CLUSTER_RADIUS`, `PHOTOPRISM_FACE_COLLISION_DIST`, `PHOTOPRISM_FACE_EPSILON_DIST`, `PHOTOPRISM_FACE_SKIP_CHILDREN`, `PHOTOPRISM_FACE_ALLOW_BACKGROUND`) are documented in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition) and in the [package README](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md).

### Tuning Tips

- A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70; a higher value is more aggressive and leads to larger clusters with more false positives.
- To cluster a smaller number of faces, reduce the core to 3 or 2 similar faces.
- Use `FACE_ENGINE=auto` to let PhotoPrism decide whether detection is possible with the bundled model.

## Face Embeddings

After detection, PhotoPrism uses TensorFlow to run [FaceNet](https://dl.photoprism.app/pdf/publications/20150101-FaceNet.pdf) and generate a 512-dimensional embedding for each face. The embeddings are used to:

1. **Match faces** across different photos.
2. **Cluster similar faces** using the DBSCAN algorithm.
3. **Assign faces to people** after manual confirmation.

### Normalization

All embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time, after TensorFlow inference (`NewEmbedding`).
- Midpoint calculation when merging clusters (`EmbeddingsMidpoint`).
- Deserialisation when loading from persisted JSON (`UnmarshalEmbedding` / `UnmarshalEmbeddings`).
- `photoprism faces audit --fix`, which re-normalizes historical embeddings and re-links markers.

With unit vectors Euclidean distance is a rank-equivalent substitute for cosine similarity, so all thresholds on this page are expressed in the Euclidean domain.

### Tensor Memory

FaceNet embeddings are generated through TensorFlow bindings that allocate tensors in C memory; those allocations are only released by Go GC finalisers. To keep memory bounded during extended indexing runs, PhotoPrism periodically forces garbage collection and returns freed C buffers to the OS. Tune with `PHOTOPRISM_TF_GC_EVERY` (default **200**; `0` disables).

## Commands

[Learn more about CLI commands ›](cli.md#face-detection-commands)

## Performance Notes

The October 2025 optimisations (still current) improved the hot paths on the embedding side:

| Benchmark                  | Before                  | After                                  |
|----------------------------|-------------------------|----------------------------------------|
| `Embedding.Dist`           | ~242 ns/op              | ~155 ns/op                             |
| `EmbeddingsMidpoint`       | ~194 µs/op, 528 KB/op   | ~99 µs/op, 4 KB/op                     |
| Face matching (1024 faces) | 1024 distance checks    | ~16 candidates evaluated (≈0.55 ms/op) |
| Cluster materialisation    | ~29.8 µs/op, 384 allocs | ~14.8 µs/op, 64 allocs                 |

Re-run `BenchmarkEmbeddingDist` and `BenchmarkEmbeddingsMidpoint` after any detector or embedding adjustment to catch regressions early.
