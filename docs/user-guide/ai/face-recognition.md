# Face Recognition

PhotoPrism uses a multi-stage AI pipeline to detect, embed, and cluster faces so they can be [easily organized by person](https://docs.photoprism.app/user-guide/organize/people/):

1. **Detection** — a detection model locates faces in each image.
2. **Embedding** — a vector is generated to characterize each face.
3. **Clustering** — similar faces are grouped so they can be assigned to a person.

Detection and embedding use separate models, so each can be chosen and upgraded on its own.

## Upgrading an Existing Library

Libraries indexed before the current [embedding model](#face-embeddings) became available keep the model they already use, because vectors produced by different models cannot be compared: switching automatically would make every face you have already assigned to a person incomparable with newly indexed ones. Setting `FACE_MODEL` does not change it either.

`photoprism faces migrate` is what changes it. It re-embeds every face, keeps the people you have already identified, and records the new model as the one in use. It defaults to the model this release supports, so an ordinary upgrade needs no target — run it [in a terminal](https://docs.photoprism.app/getting-started/docker-compose/#opening-a-terminal) with `--dry-run` first to see what it would cover:

```bash
photoprism faces migrate --dry-run # report the scope, change nothing
photoprism faces migrate           # re-embed every face
```

Expect it to take a while on a large library. Name a different target with `--to` only if you are migrating somewhere other than the model this release supports — or if this instance has `FACE_MODEL` set to `none`, which is kept rather than overridden, so the target has to be named.

!!! info ""
    **Restart your instance once the migration has finished.** It records the new model in `options.yml`, which a running instance does not reload, so face embedding work stays paused until it starts again. You do not need to stop the instance beforehand: a migration takes a lock the instance reads, so indexing and vision wait for it and edits to people are refused while it runs. Start it when no indexing or import is already under way, though — that lock is checked when such a run begins, not while one is in progress.

Afterwards, let the detector find the faces it previously missed and settle the clusters:

```bash
photoprism faces audit --fix    # resolve inconsistencies
photoprism faces index          # detect additional faces
photoprism faces update --force # re-match and cluster faces
photoprism faces optimize       # optional tidy-up
```

`--force` is what matters there: a plain `photoprism faces update` runs only once enough faces have been added since the last pass, which a freshly migrated library has not. With `--force` the pass runs regardless, every face is matched against the clusters again, and the ones left unassigned are clustered at the current settings. Faces that already belong to a cluster keep it. Reach for it whenever faces have been detected but *People* shows no cluster for them.

To check the result, `photoprism faces status` reports which model is in use and why clustering is waiting if no clusters are forming.

If you would rather start from a clean state, run `photoprism faces reset -f` followed by `photoprism faces index`. All detected faces must then be reassigned.

!!! note ""
    A [complete rescan](https://docs.photoprism.app/user-guide/library/originals/#when-should-complete-rescan-be-selected) will also detect additional faces, but takes longer since more indexing tasks are performed.

## Face Detection

PhotoPrism ships with **YuNet**, a compact face detection model that runs on the [ONNX Runtime](https://onnxruntime.ai/). It:

- Detects faces that are partially occluded (covered by hands, objects, etc.)
- Works well with off-axis or angled faces
- Handles difficult lighting conditions effectively
- Locates facial landmarks, which are used to align each face before embedding
- Consumes 720 px thumbnails (model input 640 px)
- Schedules work on the meta/vision workers

The detector is selected with `FACE_DETECTOR`. When you leave it unset, it is derived from the face model in use, so a matching combination is the default. The prebuilt runtime targets glibc ≥ 2.28 on `amd64` / `arm64` architectures.

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

Setting `FACE_MODEL` does not change the model of a library that already has one — use `photoprism faces migrate` for that, which re-embeds every face and keeps your person assignments. See [Upgrading an Existing Library](#upgrading-an-existing-library) above.

All face embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time (after inference)
- Midpoint calculation when merging clusters
- Deserialization when loading from the database

This normalization ensures that Euclidean distance comparisons are equivalent to cosine similarity.

## Config Options

!!! example ""
    We recommend that only advanced users and developers change these parameters.

### Detection Settings

| Environment Variable       | CLI Flag          | Default                 | Description                                                                        |
|----------------------------|-------------------|-------------------------|------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_DETECTOR   | --face-detector   | *(from the face model)* | Detection model (`auto`, `none`, `yunet`).                                         |
| PHOTOPRISM_FACE_MODEL      | --face-model      | sface                   | Embedding model (`auto`, `sface`, `none`), detected from the library unless named. |
| PHOTOPRISM_FACE_SIZE       | --face-size       | 25                      | Minimum size of faces in `PIXELS` (10-10000).                                      |
| PHOTOPRISM_FACE_SIZE_RETRY | --face-size-retry | 10                      | Minimum size in `PIXELS` for the retry pass, `-1` to disable.                      |
| PHOTOPRISM_FACE_SCORE      | --face-score      | *(from the detector)*   | Minimum face `QUALITY` score (1-100).                                              |
| PHOTOPRISM_FACE_OVERLAP    | --face-overlap    | 42                      | Face area overlap threshold in `PERCENT` (1-100).                                  |

### Clustering Settings

!!! info ""
    After changing any of the clustering parameters, run `photoprism faces update --force` in a terminal so that a pass runs at the new values instead of waiting for enough new faces. It applies them to the faces that are not yet in a cluster and matches every face against the clusters again; faces that already belong to one keep it, so run `photoprism faces reset` if you want the library regrouped from scratch. Changing the embedding model is a different operation and requires `photoprism faces migrate`.

| Environment Variable          | CLI Flag             | Default               | Description                                                          |
|-------------------------------|----------------------|-----------------------|----------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  | 112                   | Minimum size of automatically clustered faces in `PIXELS` (20-10000) |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score | *(from the detector)* | Minimum `QUALITY` score of automatically clustered faces (1-100)     |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  | 5                     | `NUMBER` of faces forming a cluster core (2-100)                     |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | *(from the model)*    | Similarity `DISTANCE` of faces forming a cluster core                |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | *(from the model)*    | Similarity `OFFSET` for matching faces with existing clusters        |

The distance thresholds are calibrated for each embedding model and resolved automatically, because the models do not share a vector space — a distance that separates two people under one model can merge them under another.

### Tuning Tips

- Change a distance threshold **relative to the value your model resolves to**, rather than carrying a number over from another model. A higher value is more aggressive and leads to larger clusters with more false positives.
- To cluster a smaller number of faces, you can reduce the kernel to 3 or 2 similar faces.
- Leave `FACE_DETECTOR` unset unless you have a reason to pin it, so detection stays matched to the embedding model.

## CLI Reference

- `photoprism faces status` — show which options are actually in force, including the ones resolved from the detector or model, and why clustering is waiting if no clusters are forming. `faces config` is an alias.
- `photoprism faces stats` — measure how far face embeddings sit from one another. Compares every sample with every other, so use it on a test library.
- `photoprism faces subjects [name|uid]` — list people with the clusters, files, and photos their markers support.
- `photoprism faces ls [name|uid]` — list face clusters with their samples, radius, and current markers. `faces clusters` is an alias.
- `photoprism faces markers [name|uid] [--face ID] [--unassigned] [--dangling]` — list face markers and what they are assigned to.
- `photoprism faces conflicts [name|uid]` — list face clusters that hold the same face but are assigned to different people.
- `photoprism faces audit [--subject UID] [--fix]` — check and optionally repair face data.
- `photoprism faces reset [--detector auto|none|yunet] [--all] [--force]` — remove automatic clusters and matches; `--all` also removes names while keeping the markers, `--force` removes the markers too so faces must be detected again.
- `photoprism faces index` — (re)detect faces in originals.
- `photoprism faces update [--force]` — cluster and match detected faces.
- `photoprism faces optimize` — compact clusters after updates.
- `photoprism faces migrate [--to MODEL] [--dry-run]` — re-embed every face with another model, then restart the instance. See [Upgrading an Existing Library](#upgrading-an-existing-library).
