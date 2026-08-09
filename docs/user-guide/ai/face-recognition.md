# Face Recognition

PhotoPrism uses a multi-stage AI pipeline to detect, embed, and cluster faces so they can be [easily organized by person](https://docs.photoprism.app/user-guide/organize/people/):

1. **Detection** — the ONNX SCRFD engine locates faces in each image.
2. **Embedding** — 512-dimensional vectors are generated to characterise each face.
3. **Clustering** — similar faces are grouped so they can be assigned to a person.

## Detection Engine

PhotoPrism ships a **single face detector** based on ONNX SCRFD. The legacy Pigo cascade detector was removed in the [April 2026 release](https://docs.photoprism.app/release-notes/); configurations that still set `FACE_ENGINE=pigo` are accepted and silently use ONNX so existing installations keep working after upgrade.

### ONNX SCRFD 0.5g

[ONNX Runtime](https://onnxruntime.ai/)-backed [CNN model](https://dl.photoprism.app/onnx/models/) that delivers **higher recall** on challenging faces. It:

- Detects faces that are partially occluded (covered by hands, objects, etc.)
- Works better with off-axis or angled faces
- Handles difficult lighting conditions more effectively
- Consumes 720 px thumbnails (model input 640 px)
- Schedules work on the meta/vision workers
- Defaults to half the available CPUs (minimum 1 thread)

The detector is automatically enabled when `FACE_ENGINE=auto` and the bundled SCRFD model is present; otherwise face detection is disabled. The prebuilt runtime targets glibc ≥ 2.27 on `amd64` / `arm64` architectures.

## Face Embeddings

### FaceNet

After detection, PhotoPrism uses [TensorFlow](index.md#model-engines) to run [FaceNet](https://en.wikipedia.org/wiki/FaceNet), which generates 512-dimensional embedding vectors that characterize each face. These vectors are then used to:

1. **Match faces** across different pictures.
2. **Cluster similar faces** using the DBSCAN algorithm.
3. **Assign faces to people** with manual confirmation.

All face embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time (after TensorFlow inference)
- Midpoint calculation when merging clusters
- Deserialization when loading from the database

This normalization ensures that Euclidean distance comparisons are equivalent to cosine similarity, aligning with FaceNet research standards.

## Config Options

!!! example ""
    We recommend that only advanced users and developers change these parameters.

### Detection Settings

| Environment Variable           | CLI Flag              | Default                 | Description                                                                                 |
|--------------------------------|-----------------------|-------------------------|---------------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_ENGINE         | --face-engine         | auto                    | Detection engine (`auto`, `onnx`, `none`). Legacy `pigo` is accepted and aliased to `onnx`. |
| PHOTOPRISM_FACE_ENGINE_THREADS | --face-engine-threads | runtime.NumCPU()/2 (≥1) | Number of ONNX inference threads.                                                           |
| PHOTOPRISM_FACE_SIZE           | --face-size           | 50                      | Minimum size of faces in `PIXELS` (20-10000).                                               |
| PHOTOPRISM_FACE_SCORE          | --face-score          | 9.0                     | Minimum face `QUALITY` score (1-100).                                                       |
| PHOTOPRISM_FACE_OVERLAP        | --face-overlap        | 42                      | Face area overlap threshold in `PERCENT` (1-100).                                           |

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run the "photoprism faces reset" command in a terminal to remove existing clusters and mappings after changing any of the clustering parameters, as otherwise inconsistencies may result in unexpected behavior or errors.

| Environment Variable          | CLI Flag             | Default | Description                                                             |
|-------------------------------|----------------------|---------|-------------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  | 80      | Minimum size of automatically clustered faces in `PIXELS` (20-10000)    |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score | 15      | Minimum `QUALITY` score of automatically clustered faces (1-100)        |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  | 4       | `NUMBER` of faces forming a cluster core (1-100)                        |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | 0.64    | Similarity `DISTANCE` of faces forming a cluster core (0.1-1.5)         |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | 0.46    | Similarity `OFFSET` for matching faces with existing clusters (0.1-1.5) |

### Tuning Tips

- A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher value being more aggressive and leading to larger clusters with more false positives.
- To cluster a smaller number of faces, you can reduce the kernel to 3 or 2 similar faces.
- Use `FACE_ENGINE=auto` to let PhotoPrism decide whether detection is possible with the bundled model.

## CLI Reference

- `photoprism faces stats` — show counts and engine info.
- `photoprism faces audit [--subject UID] [--fix]` — check and optionally repair face data.
- `photoprism faces reset [--engine auto|onnx|none] [--force]` — wipe people and markers, then regenerate with the chosen engine.
- `photoprism faces index` — (re)detect faces in originals.
- `photoprism faces update [--force]` — cluster and match detected faces.
- `photoprism faces optimize` — compact clusters after updates.

### Version Upgrade

To benefit from the [facial recognition improvements](https://github.com/photoprism/photoprism/issues/5167), we recommend running `photoprism faces audit --fix` and `photoprism faces index` [in a terminal](https://docs.photoprism.app/getting-started/docker-compose/#opening-a-terminal) to resolve any inconsistencies before detecting and matching additional faces:

```bash
photoprism faces audit --fix # resolve inconsistencies
photoprism faces index       # detect new faces
photoprism faces update      # cluster and match
photoprism faces optimize    # optional tidy-up
```

If you want the new engine to re-detect all faces for a clean state, you can do so by executing the commands `photoprism faces reset -f` and then `photoprism faces index`. After that, all detected faces must be reassigned.

!!! note ""
    A [complete rescan](https://docs.photoprism.app/user-guide/library/originals/#when-should-complete-rescan-be-selected) will also detect additional faces, but takes longer since more indexing tasks are performed.
