# Face Recognition

PhotoPrism uses a multi-stage AI pipeline to detect, embed, and cluster faces so they can be [easily organized by person](https://docs.photoprism.app/user-guide/organize/people/):

1. **Detection** — a detection model locates faces in each image.
2. **Embedding** — a vector is generated to characterise each face.
3. **Clustering** — similar faces are grouped so they can be assigned to a person.

Detection and embedding use separate models, so each can be chosen and upgraded on its own.

## Face Detection

PhotoPrism ships with **YuNet**, a compact face detection model that runs on the [ONNX Runtime](https://onnxruntime.ai/). It:

- Detects faces that are partially occluded (covered by hands, objects, etc.)
- Works well with off-axis or angled faces
- Handles difficult lighting conditions effectively
- Locates facial landmarks, which are used to align each face before embedding
- Consumes 720 px thumbnails (model input 640 px)
- Schedules work on the meta/vision workers

The detector is selected with `FACE_DETECTOR`. When you leave it unset, it is derived from the face model in use, so a matching combination is the default. The prebuilt runtime targets glibc ≥ 2.27 on `amd64` / `arm64` architectures.

!!! info ""
    `FACE_ENGINE` is **deprecated**: it selected a runtime rather than a model. Only `FACE_ENGINE=none` still has an effect, and `FACE_DETECTOR` overrides it. Existing configurations keep working.

### Small Faces in Group Pictures

`FACE_SIZE` is measured on the 720 px thumbnail used for detection, not on the original picture. In a crowded photo this can push every face below the minimum, so PhotoPrism automatically runs a second pass at a smaller minimum size when a picture would otherwise yield no faces at all. Set `FACE_SIZE_RETRY` to `-1` to switch that off.

## Face Embeddings

After detection, PhotoPrism generates an embedding vector that characterizes each face. These vectors are used to:

1. **Match faces** across different pictures.
2. **Cluster similar faces** using the DBSCAN algorithm.
3. **Assign faces to people** with manual confirmation.

New libraries use **SFace**, which produces 128-dimensional vectors. Libraries created before it was available keep **FaceNet**, which produces 512-dimensional vectors, because switching would make every face already assigned to a person incomparable with newly indexed ones.

Setting `FACE_MODEL` does not change the model of a library that already has one — use `photoprism faces migrate` for that, which re-embeds every face and keeps your person assignments. See the [CLI reference](#cli-reference) below.

All face embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time (after inference)
- Midpoint calculation when merging clusters
- Deserialization when loading from the database

This normalization ensures that Euclidean distance comparisons are equivalent to cosine similarity.

## Config Options

!!! example ""
    We recommend that only advanced users and developers change these parameters.

### Detection Settings

| Environment Variable       | CLI Flag          | Default                 | Description                                                         |
|----------------------------|-------------------|-------------------------|---------------------------------------------------------------------|
| PHOTOPRISM_FACE_DETECTOR   | --face-detector   | *(from the face model)* | Detection model (`auto`, `none`, `yunet`).                          |
| PHOTOPRISM_FACE_MODEL      | --face-model      | *(detected once)*       | Embedding model (`detect`, `none`, `facenet`, `sface`, `auraface`). |
| PHOTOPRISM_FACE_SIZE       | --face-size       | 25                      | Minimum size of faces in `PIXELS` (10-10000).                       |
| PHOTOPRISM_FACE_SIZE_RETRY | --face-size-retry | 10                      | Minimum size in `PIXELS` for the retry pass, `-1` to disable.       |
| PHOTOPRISM_FACE_SCORE      | --face-score      | *(from the detector)*   | Minimum face `QUALITY` score (1-100).                               |
| PHOTOPRISM_FACE_OVERLAP    | --face-overlap    | 42                      | Face area overlap threshold in `PERCENT` (1-100).                   |

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run the "photoprism faces reset" command in a terminal to remove existing clusters and mappings after changing any of the clustering parameters, as otherwise inconsistencies may result in unexpected behavior or errors.

| Environment Variable          | CLI Flag             | Default               | Description                                                          |
|-------------------------------|----------------------|-----------------------|----------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  | 60                    | Minimum size of automatically clustered faces in `PIXELS` (20-10000) |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score | *(from the detector)* | Minimum `QUALITY` score of automatically clustered faces (1-100)     |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  | 4                     | `NUMBER` of faces forming a cluster core (1-100)                     |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | *(from the model)*    | Similarity `DISTANCE` of faces forming a cluster core                |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | *(from the model)*    | Similarity `OFFSET` for matching faces with existing clusters        |

The distance thresholds are calibrated for each embedding model and resolved automatically, because the models do not share a vector space — a distance that separates two people under one model can merge them under another.

### Tuning Tips

- Change a distance threshold **relative to the value your model resolves to**, rather than carrying a number over from another model. A higher value is more aggressive and leads to larger clusters with more false positives.
- To cluster a smaller number of faces, you can reduce the kernel to 3 or 2 similar faces.
- Leave `FACE_DETECTOR` unset unless you have a reason to pin it, so detection stays matched to the embedding model.

## CLI Reference

- `photoprism faces config` — show which options are actually in force, including the ones resolved from the detector or model.
- `photoprism faces stats` — show counts and model info.
- `photoprism faces audit [--subject UID] [--fix]` — check and optionally repair face data.
- `photoprism faces reset [--detector auto|none|yunet] [--force]` — wipe people and markers, then regenerate with the chosen detector.
- `photoprism faces index` — (re)detect faces in originals.
- `photoprism faces update [--force]` — cluster and match detected faces.
- `photoprism faces optimize` — compact clusters after updates.
- `photoprism faces migrate [--to MODEL] [--dry-run]` — re-embed every face with another model. **Stop the server first.**

### Changing the Face Model

`photoprism faces migrate` is how the embedding model is changed. It re-embeds every face, keeps the people you have already identified, and records the new model as the one in use. Run it with `--dry-run` first to see what it would cover:

```bash
photoprism faces migrate --to sface --dry-run
```

!!! danger ""
    Stop the server before migrating. The migration replaces every face cluster in one transaction and cannot account for what a running instance writes to the same rows at the same time.

### Version Upgrade

To benefit from the [facial recognition improvements](https://github.com/photoprism/photoprism/issues/5167), we recommend running `photoprism faces audit --fix` and `photoprism faces index` [in a terminal](https://docs.photoprism.app/getting-started/docker-compose/#opening-a-terminal) to resolve any inconsistencies before detecting and matching additional faces:

```bash
photoprism faces audit --fix # resolve inconsistencies
photoprism faces index       # detect new faces
photoprism faces update      # cluster and match
photoprism faces optimize    # optional tidy-up
```

If you want to re-detect all faces for a clean state, you can do so by executing the commands `photoprism faces reset -f` and then `photoprism faces index`. After that, all detected faces must be reassigned.

!!! note ""
    A [complete rescan](https://docs.photoprism.app/user-guide/library/originals/#when-should-complete-rescan-be-selected) will also detect additional faces, but takes longer since more indexing tasks are performed.
