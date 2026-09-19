# Face Recognition

**Last Updated:** September 19, 2026

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
- Runs on the [ONNX Runtime](https://onnxruntime.ai/); the prebuilt runtime targets glibc ≥ 2.28 on `amd64` / `arm64`. The installation packages carry a higher floor, set by the bundled TensorFlow build rather than by this runtime.
- Scheduled on the meta/vision workers, with one detection session per indexing worker.
- Scores detections on a 0–100 confidence scale, with a calibrated cutoff below which a detection is discarded.

Every score threshold in this pipeline is on that same 0–100 scale, including the ones the detector itself enforces inside the inference session — the engine converts to the 0–1 scale its decoder reports. The cutoffs registered for YuNet are **65** for detection, **85** for admitting a marker to automatic clustering, and **50** for re-detection during a migration. They are separate numbers because they answer different questions: what to record, what to trust enough to cluster, and what to accept rather than discard a marker that already exists.

[`PHOTOPRISM_FACE_DETECTOR`](#detection-settings) selects the model by name. When it is unset, the detector is derived from the configured embedding model rather than chosen independently, so a supported combination is the default rather than something you have to assemble. Setting it to `none` disables detection.

!!! info ""
    `PHOTOPRISM_FACE_ENGINE` is **deprecated** and selected a runtime rather than a model. Only `PHOTOPRISM_FACE_ENGINE=none` still has an effect, and `PHOTOPRISM_FACE_DETECTOR` overrides it. Configurations that set it keep working; new configurations should use `PHOTOPRISM_FACE_DETECTOR`.

### Small Faces and the Retry Pass

[`PHOTOPRISM_FACE_SIZE`](#detection-settings) sets the minimum face size in detection-thumbnail pixels. Because that measurement is taken on the 720 px thumbnail rather than the original, a crowd photograph can push every face below the threshold and be indexed as containing none.

[`PHOTOPRISM_FACE_SIZE_RETRY`](#detection-settings) guards against that: when a picture yields no faces at all, detection runs a second pass at a smaller minimum size. Set it to `-1` to disable the retry.

**Its default is derived from the thumbnail settings rather than fixed**, because a face crop is taken from a pre-generated rendition: where the cache offers none wider than the detection thumbnail, the smallest faces would be detected only to stay unrecognizable, reaching neither the model's template nor the clustering bar. Unset, it resolves to **10** where a crop can reach further than 1920 px or [`PHOTOPRISM_THUMB_SIZE_FACE`](../../getting-started/config-options.md#preview-images) allows the source to be rendered on demand, **20** where it cannot reach past 1920, and **off** at a thumbnail limit of 720. An explicit value stands in either direction.

The smallest value `PHOTOPRISM_FACE_SIZE` accepts is 10 px, which is where the detector stops being trained rather than a policy choice — a smaller setting asks for faces no bundled model can find.

### Hardware Acceleration

Detection currently runs on the **CPU execution provider only**. PhotoPrism configures the inference session with thread counts and full graph optimization but does not append a hardware-accelerated execution provider, so throughput scales with [`PHOTOPRISM_FACE_DETECTOR_THREADS`](#detection-settings) and the host CPU rather than a GPU. The prebuilt runtime is the CPU build of [ONNX Runtime](https://onnxruntime.ai/), installed via [`scripts/dist/install-onnx.sh`](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/install-onnx.sh).

Optional hardware acceleration is being tracked for future releases as **opt-in** paths; CPU remains the default so existing installs are unaffected:

- **NVIDIA / CUDA (Linux)** — offloads inference to an NVIDIA GPU through the ONNX Runtime CUDA execution provider. It requires the GPU build of ONNX Runtime, the NVIDIA driver, and — for Docker — the NVIDIA Container Toolkit plus a matching CUDA and cuDNN runtime in the image (these NVIDIA libraries are not part of the ONNX Runtime archive). Tracked in [photoprism/photoprism#5703](https://github.com/photoprism/photoprism/issues/5703).
- **Apple / CoreML (native macOS builds)** — offloads to the Apple Neural Engine and GPU through the CoreML execution provider, which is already compiled into the macOS build of ONNX Runtime. This benefits **natively built** macOS binaries only: the standard Docker image runs inside a Linux VM on macOS with no Apple-accelerator passthrough, so it stays CPU-only regardless. Tracked in [photoprism/photoprism#5704](https://github.com/photoprism/photoprism/issues/5704).

## Embedding Models

[`PHOTOPRISM_FACE_MODEL`](#embedding-settings) selects the model that turns a detected face into a vector. Each supported model needs code that knows its preprocessing contract, so the set is a registry rather than an arbitrary file path.

| Model      | Runtime    | Dimensions | Crop Alignment | Availability                         |
|------------|------------|------------|----------------|--------------------------------------|
| `sface`    | ONNX       | 128        | Landmark       | Bundled; preferred for new libraries |
| `facenet`  | TensorFlow | 512        | Bounding box   | Bundled; kept by existing libraries  |
| `auraface` | ONNX       | 512        | Landmark       | Optional download                    |

`--help` offers `auto`, `sface`, and `none`, because the help text reads as an offer and `sface` is the model this release supports. The others in the table remain selectable by name and are documented here for that reason.

When `PHOTOPRISM_FACE_MODEL` is unset, PhotoPrism works the model out once and writes the name to `options.yml`:

- **A library that already holds face vectors keeps the model that produced them.** Resolving away from it would leave every stored cluster incomparable with anything indexed afterwards, so the existing space wins even when a preferred model is installed.
- **A library with no face vectors takes the first installed model in preference order**, which is `sface`.

`auraface` is redistributable but too large to ship in the images, so it is an explicit download rather than a bundled model. It measures in the same quality band as `sface` at roughly eight times the size, which is why `sface` is the one that ships.

### Crop Alignment

Models marked **Landmark** above are trained on faces warped onto a standard template, so PhotoPrism fits a similarity transform from the five detected landmarks onto a 112×112 template before inference. When a face has no complete landmark set, it falls back to an unaligned bounding box crop. `facenet` is trained on unaligned crops and takes the bounding box directly.

This is why the detector has to emit landmarks, and why detection and embedding are not freely interchangeable — `PHOTOPRISM_FACE_DETECTOR` derives from `PHOTOPRISM_FACE_MODEL` for exactly this reason.

### Changing the Model

An environment variable does not change the model of a library that already has one. Use the migration command, which re-embeds every marker and records the target as the configured model:

```bash
docker compose exec photoprism photoprism faces migrate
```

It defaults to the supported model, so an ordinary migration needs no `--to`. `photoprism faces reset` clears the recorded pin, because a reset leaves no vectors for it to keep comparable.

Restart the instance once it has finished, and see [Migrate Face Embeddings](cli.md#migrate-face-embeddings) for the dry run, the report it prints, what re-detection can lose, and what happens to person assignments.

!!! info ""
    If the configured model cannot read a library's stored vectors, embedding work **pauses** rather than silently filtering the mismatch: generation, clustering, and matching stop after one warning until a migration reconciles them. Detection keeps running, so faces stay recorded and their vectors are filled in afterwards.

## Configuration

!!! example ""
    We recommend that only advanced users and developers change these parameters. All face-related environment variables and CLI flags are listed in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition); this page only highlights the knobs most relevant to detector and model behavior.

### Run Scheduling

[`PHOTOPRISM_FACE_RUN`](#run-scheduling) decides when face detection and clustering run. It is the only control: unlike the label and caption models, faces are **not** scheduled through `vision.yml`.

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

| Environment Variable             | CLI Flag                | Default                                                         | Description                                                                                                 |
|----------------------------------|-------------------------|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_DETECTOR         | --face-detector         | yunet                                                           | face detection model `NAME` (auto, yunet, none), derived from the face model unless named                   |
| PHOTOPRISM_FACE_DETECTOR_THREADS | --face-detector-threads | auto                                                            | face detection thread `COUNT` per indexing worker, derived from the CPU cores when unset                    |
| PHOTOPRISM_FACE_SIZE             | --face-size             | 25                                                              | minimum size of faces in `PIXELS` (10-10000)                                                                |
| PHOTOPRISM_FACE_SIZE_RETRY       | --face-size-retry       | 10 (20 where a crop can reach no further than 1920, off at 720) | minimum size of faces in `PIXELS` when a picture would otherwise have none, -1 to disable                   |
| PHOTOPRISM_FACE_SCORE            | --face-score            | 65                                                              | minimum face `QUALITY` score (1-100), replacing the detector's own calibrated cutoff, -1 disables the check |
| PHOTOPRISM_FACE_OVERLAP          | --face-overlap          | 42                                                              | face area overlap threshold in `PERCENT` (1-100)                                                            |

[`PHOTOPRISM_FACE_SCORE`](#detection-settings) replaces the calibrated cutoff rather than being applied after it, so it can loosen detection as well as tighten it. The cutoff lives in the inference session, so a lower value genuinely admits detections the detector would otherwise never emit. It exists for calibration work; leave it unset unless you are measuring something.

### Migration Settings

Re-detection during `photoprism faces migrate` runs at its own floors, because keeping an existing marker and creating a new one are different trades — see [Migrate Face Embeddings](cli.md#migrate-face-embeddings).

| Environment Variable          | CLI Flag             | Default | Description                                                                                                                              |
|-------------------------------|----------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_MIGRATE_SIZE  | --face-migrate-size  | 10      | minimum size of faces in `PIXELS` while a migration re-detects them, which is where a marker an earlier detector placed is found or lost |
| PHOTOPRISM_FACE_MIGRATE_SCORE | --face-migrate-score | 50      | minimum face `QUALITY` score (1-100) while a migration re-detects them, -1 disables the check                                            |

The size floor is lower than `PHOTOPRISM_FACE_SIZE` on purpose: a marker's size is recorded in pixels of the thumbnail it was detected in, and an earlier detector may have fallen back to a larger thumbnail, so a marker carried over from one can sit well below the ordinary floor — which no score recovers.

### Embedding Settings

| Environment Variable          | CLI Flag             | Default | Description                                                                                                                        |
|-------------------------------|----------------------|---------|------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_MODEL         | --face-model         | sface   | face embedding model `NAME` (auto, sface, none), detected from the library unless named, and changed with photoprism faces migrate |
| PHOTOPRISM_FACE_MODEL_THREADS | --face-model-threads | auto    | face embedding thread `COUNT`, derived from the CPU cores when unset                                                               |

!!! info ""
    `PHOTOPRISM_FACE_ENGINE_THREADS` is **deprecated** and set both thread counts at once. They derive different defaults because detection runs one session per indexing worker while embedding runs a single shared session, so a value that suits one does not suit the other.

`detect` is no longer accepted as a spelling of `auto` for either `PHOTOPRISM_FACE_MODEL` or `PHOTOPRISM_FACE_DETECTOR`. A configuration that still sets it is reported once and then applied as a request to derive the value; for `PHOTOPRISM_FACE_MODEL` it additionally stops the detected name being recorded, so correct it in `options.yml` to avoid re-detecting on every start.

Face **scheduling** is configured through `PHOTOPRISM_FACE_RUN` alone — see [Run Scheduling](#run-scheduling) above. Unlike the label and caption models, faces are not scheduled through `vision.yml`, and a **custom face model configured in `vision.yml` is deprecated** in favor of `PHOTOPRISM_FACE_MODEL`; it still loads while no embedding model is active and logs a warning.

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run `photoprism faces reset` in a terminal to remove existing clusters and markers after changing any of the clustering parameters, otherwise inconsistencies may cause unexpected behavior or errors.

| Environment Variable               | CLI Flag                  | Default                                    | Description                                                                                                                                                                           |
|------------------------------------|---------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE       | --face-cluster-size       | 112                                        | minimum size of automatically clustered faces in `PIXELS` of the image their embedding was sampled from (20-10000), calibrated per face model when unset                              |
| PHOTOPRISM_FACE_CLUSTER_SCORE      | --face-cluster-score      | 85                                         | minimum `QUALITY` score of automatically clustered faces (1-100), overriding the bar calibrated per detector, -1 disables the check                                                   |
| PHOTOPRISM_FACE_CLUSTER_CORE       | --face-cluster-core       | 5                                          | `NUMBER` of faces forming a cluster core (2-100)                                                                                                                                      |
| PHOTOPRISM_FACE_CLUSTER_CORE_RETRY | --face-cluster-core-retry | 4 (off where face-cluster-core is below 5) | `NUMBER` of faces forming a cluster core in a second pass over what matching left unclustered, -1 to disable                                                                          |
| PHOTOPRISM_FACE_CLUSTER_DIST       | --face-cluster-dist       | 0.72                                       | similarity `DISTANCE` of faces forming a cluster core (collision distance to 1.25), calibrated per face model when unset                                                              |
| PHOTOPRISM_FACE_CLUSTER_RADIUS     | --face-cluster-radius     | 0.7                                        | maximum cluster `RADIUS` accepted for automatic matches, calibrated per face model when unset; radius plus match distance may not exceed 1.25                                         |
| PHOTOPRISM_FACE_CLUSTER_PERCENTILE | --face-cluster-percentile | 95                                         | `PERCENTILE` of the member distances a cluster's radius is derived from (1-100), where 100 uses the maximum and lets one loose face decide how far the cluster reaches                |
| PHOTOPRISM_FACE_MATCH_DIST         | --face-match-dist         | 0.25                                       | similarity `OFFSET` for matching faces with existing clusters, calibrated per face model when unset; radius plus match distance may not exceed 1.25                                   |
| PHOTOPRISM_FACE_MATCH_MARGIN       | --face-match-margin       | 0.01                                       | minimum `DISTANCE` by which the nearest cluster must beat the runner-up, leaving a face between two people unassigned instead of guessing, 0 reads as unset and -1 disables the check |
| PHOTOPRISM_FACE_COLLISION_DIST     | --face-collision-dist     | 0.05                                       | minimum collision discrimination `DISTANCE` (greater than 0, up to 1), the same for every face model                                                                                  |
| PHOTOPRISM_FACE_EPSILON_DIST       | --face-epsilon-dist       | 0.001                                      | collision tolerance `DELTA` appended to max match distances (up to 0.01), the same for every face model; twice it is the distance at which a colliding cluster is retired for good    |

Distance thresholds are **calibrated per embedding model** and resolved from the model in use when left unset, because the models do not share a vector space — a distance that separates two people under one model merges them under another. The values below are what each model resolves to:

| Model         | Cluster Distance | Cluster Radius | Match Distance | Collision Distance | Epsilon |
|---------------|------------------|----------------|----------------|--------------------|---------|
| `facenet`     | 0.64             | 0.42           | 0.40           | 0.05               | 0.001   |
| `sface`       | 0.72             | 0.70           | 0.25           | 0.05               | 0.001   |
| `auraface`    | 0.98             | 0.76           | 0.35           | 0.05               | 0.001   |
| `arcface_r50` | 1.07             | 0.67           | 0.55           | 0.05               | 0.001   |
| `arcface_mbf` | 1.03             | 0.64           | 0.49           | 0.05               | 0.001   |

**Collision distance and epsilon are the same for every model**, unlike the three above them: they describe the gap a resolved collision leaves rather than a separation the vector space defines.

[`PHOTOPRISM_FACE_CLUSTER_SIZE`](#clustering-settings) is likewise resolved from the model when unset — it is the embedder's own input size, so **112 px for `sface` and 160 px for `facenet`**. It is measured in pixels of the image the embedding was sampled from, not of the detection thumbnail.

Cluster radius plus match distance may not exceed 1.4, and a configured value above that ceiling is refused rather than clipped, so the reported configuration always matches the one in force.

**Epsilon is the one distance that does not scale with the model.** The others are calibrated separations; epsilon is the *gap* a resolved collision leaves behind — a void where nothing matches — so a wider one strands embeddings rather than telling two people apart. It is registered per model only so it can be overridden, and [`PHOTOPRISM_FACE_EPSILON_DIST`](#clustering-settings) accepts at most `0.01`; a larger value resolves to the model default with a warning. Twice epsilon is the distance below which two embeddings of different subjects are flagged ambiguous instead of being separated, because below that the backoff would exceed the separation it preserves.

The clustering score bar is taken from **the detector that scored each marker**, not from the detector currently configured. Detector scores are not comparable across models, and nothing recomputes a stored score, so judging an old marker by a new detector's bar would exclude it permanently for a calibration it was never scored against. Markers indexed before detector provenance was recorded fall back to a shared default of 20.

`PHOTOPRISM_FACE_MERGE_MAX_RETRY` limits how often the optimizer retries stubborn manual clusters (`0` for unlimited); it is read from the environment only and has no CLI flag, so it appears neither in the table above nor in [Config Options › Face Recognition](../../getting-started/config-options.md#face-recognition). It is described alongside the distance thresholds in the [package README](https://github.com/photoprism/photoprism/blob/develop/internal/ai/face/README.md).

### The Second Clustering Pass

Clustering runs twice. The first pass forms cores at [`PHOTOPRISM_FACE_CLUSTER_CORE`](#clustering-settings); matching then attaches
what it can to existing clusters; and a second pass runs at [`PHOTOPRISM_FACE_CLUSTER_CORE_RETRY`](#clustering-settings) over whatever
is **still unclustered**. It needs no separate selection rule — clustering only ever considers
markers that carry no cluster, so once matching has finished the residue is exactly what remains.

The retry core is derived: **4 where `PHOTOPRISM_FACE_CLUSTER_CORE` is 5 or higher, and disabled below that**.
It is deliberately a fixed 4 rather than one below whatever the core is set to, because 5 → 4 is the
combination that was measured. A value at or above `PHOTOPRISM_FACE_CLUSTER_CORE` is meaningless — it can form
nothing the first pass did not — and resolves to `-1`.

The point is to reach people with few pictures without fragmenting people who have many. Lowering
`PHOTOPRISM_FACE_CLUSTER_CORE` itself does the opposite: it applies the weaker density requirement to everyone,
which splits well-photographed people across more clusters and loses recall overall.

### Embedding Detail

Every embedding records what share of the crop the embedder asked for its source could supply, as
`markers.embed_detail` — 100 where the source supplied all of it, less where the crop had to be
enlarged. **Embeddings below 100 are not clustered**, whatever `PHOTOPRISM_FACE_CLUSTER_SIZE` is set to, so a
vector resting on interpolated pixels cannot join a cluster even when the size bar is lowered.

Markers that no sampling has measured are unaffected: the value is unset for every marker indexed
before it existed, and those cluster exactly as before. Only re-embedding — indexing, or
`photoprism faces migrate` — records it.

### Tuning Tips

- Prefer adjusting a threshold **relative to the calibrated value for your model** rather than carrying a number over from another model; a higher cluster distance is more aggressive and leads to larger clusters with more false positives.
- To reach people with only a few pictures, prefer `PHOTOPRISM_FACE_CLUSTER_CORE_RETRY` over lowering `PHOTOPRISM_FACE_CLUSTER_CORE`. The retry applies the weaker requirement **only to what is left unclustered**; lowering the core applies it to everyone, which fragments well-photographed people and loses more than it gains.
- Raising [`PHOTOPRISM_FACE_CLUSTER_SCORE`](#clustering-settings) is a weak control on its own, because detector confidence saturates above the detector's own cutoff. `PHOTOPRISM_FACE_CLUSTER_SIZE` is what keeps an interpolated, upscaled crop out of a cluster — and on real libraries it is by some margin the bar that excludes the most markers. It is not the only guard: `embed_detail` keeps upscaled crops out regardless of how the size bar is set.
- If face crops are being enlarged, the fix is more source pixels rather than a lower bar. `PHOTOPRISM_THUMB_SIZE_FACE` caps the source rendered on demand so a face crop is not taken from a rendition narrower than it needs; it defaults to 4096 px, and `0` disables the rendering.
- Leave `PHOTOPRISM_FACE_DETECTOR` unset unless you have a reason to pin it, so detection stays matched to the embedding model.
- `PHOTOPRISM_FACE_SCORE` and [`PHOTOPRISM_FACE_MIGRATE_SCORE`](#migration-settings) exist for calibration work. They change what is recorded and what is kept, so a value carried over from a measurement run is not a setting to leave in place.

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
