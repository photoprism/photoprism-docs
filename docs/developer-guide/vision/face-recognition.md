# Face Recognition

**Last Updated:** August 25, 2026

To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism uses a multi-stage AI pipeline that detects faces, generates embeddings, and clusters similar faces so they can be easily organized by person.

!!! tldr ""
    The canonical engineering reference for this pipeline is the package README at [`internal/ai/face/README.md`](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md). This page summarizes the developer-facing behavior; consult the README for the latest thresholds, benchmarks, and test recipes.

## How It Works

The face recognition pipeline runs in three stages:

1. **Detection** — a detection model locates faces in the 720 px thumbnail of each photo (see [Thumbnails](../media/thumbnails.md) for how thumbnails are generated with libvips).
2. **Embedding** — an embedding model turns each detected face into a vector that can be compared with others.
3. **Clustering** — similar embeddings are grouped with the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) so clusters can be assigned to people.

Detection and embedding are configured independently, so the model that finds a face and the model that describes it can be chosen and upgraded separately.

## Detection Models

**YuNet** is the bundled detector. It is a compact, anchor-free CNN published in the [OpenCV Zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet) under the MIT license, and it emits a bounding box plus five facial landmarks, which the embedding stage needs to align crops. Implementation details:

- Consumes 720 px thumbnails with a 640 px model input.
- Runs on the [ONNX Runtime](https://onnxruntime.ai/); the prebuilt runtime targets glibc ≥ 2.27 on `amd64` / `arm64`.
- Scheduled on the meta/vision workers, with one detection session per indexing worker.
- Scores detections on a 0–100 confidence scale, with a calibrated cutoff below which a detection is discarded.

Every score threshold in this pipeline is on that same 0–100 scale, including the ones the detector itself enforces inside the inference session — the engine converts to the 0–1 scale its decoder reports. The cutoffs registered for YuNet are **65** for detection, **70** for admitting a marker to automatic clustering, and **50** for re-detection during a migration. They are separate numbers because they answer different questions: what to record, what to trust enough to cluster, and what to accept rather than discard a marker that already exists.

`FACE_DETECTOR` selects the model by name. When it is unset, the detector is derived from the configured embedding model rather than chosen independently, so a supported combination is the default rather than something you have to assemble. Setting it to `none` disables detection.

!!! info ""
    `FACE_ENGINE` is **deprecated** and selected a runtime rather than a model. Only `FACE_ENGINE=none` still has an effect, and `FACE_DETECTOR` overrides it. Configurations that set it keep working; new configurations should use `FACE_DETECTOR`.

### Small Faces and the Retry Pass

`FACE_SIZE` sets the minimum face size in detection-thumbnail pixels. Because that measurement is taken on the 720 px thumbnail rather than the original, a crowd photograph can push every face below the threshold and be indexed as containing none.

`FACE_SIZE_RETRY` guards against that: when a picture yields no faces at all, detection runs a second pass at a smaller minimum size. Set it to `-1` to disable the retry.

The smallest value `FACE_SIZE` accepts is 10 px, which is where the detector stops being trained rather than a policy choice — a smaller setting asks for faces no bundled model can find.

### Hardware Acceleration

Detection currently runs on the **CPU execution provider only**. PhotoPrism configures the inference session with thread counts and full graph optimization but does not append a hardware-accelerated execution provider, so throughput scales with `FACE_DETECTOR_THREADS` and the host CPU rather than a GPU. The prebuilt runtime is the CPU build of [ONNX Runtime](https://onnxruntime.ai/), installed via [`scripts/dist/install-onnx.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-onnx.sh).

Optional hardware acceleration is being tracked for future releases as **opt-in** paths; CPU remains the default so existing installs are unaffected:

- **NVIDIA / CUDA (Linux)** — offloads inference to an NVIDIA GPU through the ONNX Runtime CUDA execution provider. It requires the GPU build of ONNX Runtime, the NVIDIA driver, and — for Docker — the NVIDIA Container Toolkit plus a matching CUDA and cuDNN runtime in the image (these NVIDIA libraries are not part of the ONNX Runtime archive). Tracked in [photoprism/photoprism#5703](https://github.com/photoprism/photoprism/issues/5703).
- **Apple / CoreML (native macOS builds)** — offloads to the Apple Neural Engine and GPU through the CoreML execution provider, which is already compiled into the macOS build of ONNX Runtime. This benefits **natively built** macOS binaries only: the standard Docker image runs inside a Linux VM on macOS with no Apple-accelerator passthrough, so it stays CPU-only regardless. Tracked in [photoprism/photoprism#5704](https://github.com/photoprism/photoprism/issues/5704).

## Embedding Models

`FACE_MODEL` selects the model that turns a detected face into a vector. Each supported model needs code that knows its preprocessing contract, so the set is a registry rather than an arbitrary file path.

| Model      | Runtime    | Dimensions | Crop Alignment | Availability                         |
|------------|------------|------------|----------------|--------------------------------------|
| `sface`    | ONNX       | 128        | Landmark       | Bundled; preferred for new libraries |
| `facenet`  | TensorFlow | 512        | Bounding box   | Bundled; kept by existing libraries  |
| `auraface` | ONNX       | 512        | Landmark       | Optional download                    |

`--help` offers `auto`, `sface`, and `none`, because the help text reads as an offer and `sface` is the model this release supports. The others in the table remain selectable by name and are documented here for that reason.

When `FACE_MODEL` is unset, PhotoPrism works the model out once and writes the name to `options.yml`:

- **A library that already holds face vectors keeps the model that produced them.** Resolving away from it would leave every stored cluster incomparable with anything indexed afterwards, so the existing space wins even when a preferred model is installed.
- **A library with no face vectors takes the first installed model in preference order**, which is `sface`.

`auraface` is redistributable but too large to ship in the images, so it is an explicit download rather than a bundled model. It measures in the same quality band as `sface` at roughly eight times the size, which is why `sface` is the one that ships.

### Crop Alignment

Models marked **Landmark** above are trained on faces warped onto a standard template, so PhotoPrism fits a similarity transform from the five detected landmarks onto a 112×112 template before inference. When a face has no complete landmark set, it falls back to an unaligned bounding box crop. `facenet` is trained on unaligned crops and takes the bounding box directly.

This is why the detector has to emit landmarks, and why detection and embedding are not freely interchangeable — `FACE_DETECTOR` derives from `FACE_MODEL` for exactly this reason.

### Changing the Model

An environment variable does not change the model of a library that already has one. Use the migration command, which re-embeds every marker and records the target as the configured model:

```bash
docker compose exec photoprism photoprism faces migrate
```

It defaults to the supported model, so an ordinary migration needs no `--to`. `photoprism faces reset` clears the recorded pin, because a reset leaves no vectors for it to keep comparable.

Stop the server first, and see [Migrate Face Embeddings](cli.md#migrate-face-embeddings) for the dry run, the report it prints, what re-detection can lose, and what happens to person assignments.

!!! info ""
    If the configured model cannot read a library's stored vectors, embedding work **pauses** rather than silently filtering the mismatch: generation, clustering, and matching stop after one warning until a migration reconciles them. Detection keeps running, so faces stay recorded and their vectors are filled in afterwards.

## Configuration

!!! example ""
    We recommend that only advanced users and developers change these parameters. All face-related environment variables and CLI flags are listed in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition); this page only highlights the knobs most relevant to detector and model behavior.

### Run Scheduling

`FACE_RUN` decides when face detection and clustering run. It is the only control: unlike the label and caption models, faces are **not** scheduled through `vision.yml`.

| Value           | Effect                                                                                               |
|-----------------|------------------------------------------------------------------------------------------------------|
| `auto`          | Detects inline while indexing on a host fast enough, otherwise on the pass over newly indexed files. |
| `always`        | Detects while indexing **and** sweeps the library on the scheduled vision pass.                      |
| `on-index`      | Detects while indexing, and on an explicit run.                                                      |
| `newly-indexed` | Covers newly indexed pictures, on-demand work, and explicit runs.                                    |
| `on-schedule`   | Sweeps the whole library on the scheduled vision pass.                                               |
| `on-demand`     | Covers manual and newly indexed work, without re-examining pictures an earlier pass already saw.     |
| `manual`        | Runs only when a command asks for it.                                                                |
| `never`         | Disables the worker.                                                                                 |

**Only `on-schedule` and `always` sweep the library.** Every other value, `auto` and `on-demand` included, stays out of the scheduled pass: re-examining pictures an earlier pass already saw costs a full decode per file and finds nothing while the detector is unchanged. What makes another pass worthwhile is a change of detector, and that is a migration or an explicit run.

Detection and embedding always run together, so one schedule covers both.

### Detection Settings

| Environment Variable             | CLI Flag                | Default                       | Description                                                                                                    |
|----------------------------------|-------------------------|-------------------------------|----------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_DETECTOR         | --face-detector         | *(from the face model)*       | Detection model (`auto`, `none`, `yunet`).                                                                     |
| PHOTOPRISM_FACE_DETECTOR_THREADS | --face-detector-threads | `NumCPU()`/index workers (≥1) | ONNX threads per detection session; one session runs per indexing worker.                                      |
| PHOTOPRISM_FACE_SIZE             | --face-size             | 25                            | Minimum face size in `PIXELS` (10-10000), measured on the detection thumbnail.                                 |
| PHOTOPRISM_FACE_SIZE_RETRY       | --face-size-retry       | 10                            | Minimum face size in `PIXELS` for the second pass, used only when a picture would have none.                   |
| PHOTOPRISM_FACE_SCORE            | --face-score            | *(from the detector)*         | Minimum face `QUALITY` score (1-100), **replacing** the detector's calibrated cutoff; `-1` disables the check. |
| PHOTOPRISM_FACE_OVERLAP          | --face-overlap          | 42                            | Maximum allowed IoU when deduplicating markers.                                                                |

`FACE_SCORE` replaces the calibrated cutoff rather than being applied after it, so it can loosen detection as well as tighten it. The cutoff lives in the inference session, so a lower value genuinely admits detections the detector would otherwise never emit. It exists for calibration work; leave it unset unless you are measuring something.

### Migration Settings

Re-detection during `photoprism faces migrate` runs at its own floors, because keeping an existing marker and creating a new one are different trades — see [Migrate Face Embeddings](cli.md#migrate-face-embeddings).

| Environment Variable          | CLI Flag             | Default               | Description                                                                                 |
|-------------------------------|----------------------|-----------------------|---------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_MIGRATE_SIZE  | --face-migrate-size  | 10                    | Minimum face size in `PIXELS` while a migration re-detects.                                 |
| PHOTOPRISM_FACE_MIGRATE_SCORE | --face-migrate-score | *(from the detector)* | Minimum face `QUALITY` score (1-100) while a migration re-detects; `-1` disables the check. |

The size floor is lower than `FACE_SIZE` on purpose: a marker's size is recorded in pixels of the thumbnail it was detected in, and an earlier detector may have fallen back to a larger thumbnail, so a marker carried over from one can sit well below the ordinary floor — which no score recovers.

### Embedding Settings

| Environment Variable          | CLI Flag             | Default           | Description                                                                            |
|-------------------------------|----------------------|-------------------|----------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_MODEL         | --face-model         | *(detected once)* | Embedding model (`auto`, `none`, `sface`; `facenet` and `auraface` are also accepted). |
| PHOTOPRISM_FACE_MODEL_THREADS | --face-model-threads | `NumCPU()`/2 (≥1) | ONNX threads for embedding, which runs one session in total behind the model lock.     |

!!! info ""
    `FACE_ENGINE_THREADS` is **deprecated** and set both thread counts at once. They derive different defaults because detection runs one session per indexing worker while embedding runs a single shared session, so a value that suits one does not suit the other.

`detect` is no longer accepted as a spelling of `auto` for either `FACE_MODEL` or `FACE_DETECTOR`. A configuration that still sets it is reported once and then applied as a request to derive the value; for `FACE_MODEL` it additionally stops the detected name being recorded, so correct it in `options.yml` to avoid re-detecting on every start.

Face **scheduling** is configured through `FACE_RUN` alone — see [Run Scheduling](#run-scheduling) above. Unlike the label and caption models, faces are not scheduled through `vision.yml`, and a **custom face model configured in `vision.yml` is deprecated** in favor of `FACE_MODEL`; it still loads while no embedding model is active and logs a warning.

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run `photoprism faces reset` in a terminal to remove existing clusters and markers after changing any of the clustering parameters, otherwise inconsistencies may cause unexpected behavior or errors.

| Environment Variable           | CLI Flag              | Default               | Description                                                                        |
|--------------------------------|-----------------------|-----------------------|------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE   | --face-cluster-size   | 60                    | Minimum size of automatically clustered faces in `PIXELS` (20-10000).              |
| PHOTOPRISM_FACE_CLUSTER_SCORE  | --face-cluster-score  | *(from the detector)* | Minimum `QUALITY` score of automatically clustered faces (1-100).                  |
| PHOTOPRISM_FACE_CLUSTER_CORE   | --face-cluster-core   | 4                     | `NUMBER` of faces forming a cluster core (1-100), and half the clustering trigger. |
| PHOTOPRISM_FACE_CLUSTER_DIST   | --face-cluster-dist   | *(from the model)*    | Similarity `DISTANCE` of faces forming a cluster core.                             |
| PHOTOPRISM_FACE_CLUSTER_RADIUS | --face-cluster-radius | *(from the model)*    | Maximum cluster `RADIUS` accepted for automatic matches.                           |
| PHOTOPRISM_FACE_MATCH_DIST     | --face-match-dist     | *(from the model)*    | Similarity `OFFSET` for matching faces with existing clusters.                     |

Distance thresholds are **calibrated per embedding model** and resolved from the model in use when left unset, because the models do not share a vector space — a distance that separates two people under one model merges them under another. The values below are what each model resolves to:

| Model      | Cluster Distance | Cluster Radius | Match Distance | Collision Distance | Epsilon |
|------------|------------------|----------------|----------------|--------------------|---------|
| `facenet`  | 0.64             | 0.42           | 0.40           | 0.050              | 0.010   |
| `sface`    | 0.85             | 0.60           | 0.35           | 0.061              | 0.010   |
| `auraface` | 0.98             | 0.76           | 0.35           | 0.077              | 0.010   |

Cluster radius plus match distance may not exceed 1.25, and a configured value above that ceiling is refused rather than clipped, so the reported configuration always matches the one in force.

**Epsilon is the one distance that does not scale with the model.** The others are calibrated separations; epsilon is the *gap* a resolved collision leaves behind — a void where nothing matches — so a wider one strands embeddings rather than telling two people apart. It is registered per model only so it can be overridden, and `FACE_EPSILON_DIST` accepts at most `0.01`; a larger value resolves to the model default with a warning. Twice epsilon is the distance below which two embeddings of different subjects are flagged ambiguous instead of being separated, because below that the backoff would exceed the separation it preserves.

The clustering score bar is taken from **the detector that scored each marker**, not from the detector currently configured. Detector scores are not comparable across models, and nothing recomputes a stored score, so judging an old marker by a new detector's bar would exclude it permanently for a calibration it was never scored against. Markers indexed before detector provenance was recorded fall back to a shared default of 20.

`PHOTOPRISM_FACE_COLLISION_DIST` and `PHOTOPRISM_FACE_EPSILON_DIST` are listed in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition). `PHOTOPRISM_FACE_MERGE_MAX_RETRY` limits how often the optimizer retries stubborn manual clusters (`0` for unlimited); it is read from the environment only and has no CLI flag, so it does not appear in that table. All three are described in the [package README](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md).

### Tuning Tips

- Prefer adjusting a threshold **relative to the calibrated value for your model** rather than carrying a number over from another model; a higher cluster distance is more aggressive and leads to larger clusters with more false positives.
- To cluster a smaller number of faces, reduce the core to 3 or 2 similar faces.
- Raising `FACE_CLUSTER_SCORE` is a weak control on its own, because detector confidence saturates above the detector's own cutoff. `FACE_CLUSTER_SIZE` is what keeps an interpolated, upscaled crop out of a cluster — and on real libraries it is by some margin the bar that excludes the most markers.
- Leave `FACE_DETECTOR` unset unless you have a reason to pin it, so detection stays matched to the embedding model.
- `FACE_SCORE` and `FACE_MIGRATE_SCORE` exist for calibration work. They change what is recorded and what is kept, so a value carried over from a measurement run is not a setting to leave in place.

### When No Clusters Appear

Detected faces that never reach **People › New** usually mean clustering has not run, rather than that it ran and rejected them. Start with the report rather than with the thresholds:

```bash
docker compose exec photoprism photoprism faces status
```

It names which of the two situations applies. If markers exist but none is newer than the newest cluster, an automatic pass will not restart on its own, and `photoprism faces update --force` is what reconsiders the whole library. If instead there are simply not enough markers clearing the bars yet, the report says how many clear each one — and the gap between "clears the size bar" and "clears the score bar" tells you which threshold to look at first.

## Face Embeddings

Embeddings are used to:

1. **Match faces** across different photos.
2. **Cluster similar faces** using the DBSCAN algorithm.
3. **Assign faces to people** after manual confirmation.

### Normalization

All embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time, after inference (`NewEmbedding`).
- Midpoint calculation when merging clusters (`EmbeddingsMidpoint`).
- Deserialisation when loading from persisted JSON (`UnmarshalEmbedding` / `UnmarshalEmbeddings`).
- `photoprism faces audit --fix`, which re-normalizes historical embeddings and re-links markers.

With unit vectors Euclidean distance is a rank-equivalent substitute for cosine similarity, so all thresholds on this page are expressed in the Euclidean domain.

A vector is only comparable with another produced by the same model, so each marker records the model that generated it. Vectors of differing width are rejected rather than compared.

### Tensor Memory

This applies to `facenet` only, which is the one model that runs on TensorFlow. Its embeddings are generated through bindings that allocate tensors in C memory, and those allocations are only released by Go GC finalisers. To keep memory bounded during extended indexing runs, PhotoPrism periodically forces garbage collection and returns freed C buffers to the OS. Tune with `PHOTOPRISM_TF_GC_EVERY` (default **200**; `0` disables). Lower values reduce peak RSS but increase GC overhead.

## Commands

[Learn more about CLI commands ›](cli.md#face-detection-commands)

## Performance Notes

| Benchmark                     | Current            |
|-------------------------------|--------------------|
| `BenchmarkEmbeddingDist`      | ~155 ns/op         |
| `BenchmarkEmbeddingsMidpoint` | ~99 µs/op, 4 KB/op |

Re-run `BenchmarkEmbeddingDist` and `BenchmarkEmbeddingsMidpoint` after any detector or embedding adjustment to catch regressions early.
