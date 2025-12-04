# Face Recognition

To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism uses a multi-stage AI pipeline that detects faces, generates embeddings, and clusters similar faces so they can be easily organized by person.

!!! tldr ""
    PhotoPrism supports **two interchangeable detection engines** that you can switch between depending on your hardware and accuracy requirements. The ONNX-based engine provides significantly improved detection of faces that are occluded, at angles, or in challenging lighting conditions.

## How It Works

The face recognition pipeline consists of three stages:

1. **Detection** - Locate faces in photos using Pigo or ONNX SCRFD engines
2. **Embedding** - Generate 512-dimensional vectors to characterize each face using TensorFlow based on [FaceNet](https://dl.photoprism.app/pdf/publications/20150101-FaceNet.pdf)
3. **Clustering** - Group similar faces using the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) so they can be assigned to people

## Detection Engines

PhotoPrism offers two face detection engines with different characteristics:

### Pigo

[Pigo](https://github.com/esimov/pigo) is a fast, CPU-only cascade classifier based on [pixel intensity comparisons](https://dl.photoprism.app/pdf/publications/20140820-Pixel_Intensity_Comparisons.pdf). It provides good performance for straightforward face detection scenarios and maintains PhotoPrism's historical detection behavior.

**Best for:**

- Quick processing of well-lit, front-facing portraits
- Lower resource consumption

### ONNX SCRFD 0.5g

ONNX Runtime-backed CNN model that delivers **higher recall** on challenging faces. This engine:

- Detects faces that are partially occluded (covered by hands, objects, etc.)
- Works better with off-axis or angled faces
- Handles difficult lighting conditions more effectively
- Consumes 720px thumbnails (model input 640px)
- Schedules work on the meta/vision workers
- Defaults to half the available CPUs (minimum 1 thread)

The ONNX engine is automatically enabled when `FACE_ENGINE=auto` and the bundled SCRFD model is present. The prebuilt runtime targets glibc ≥ 2.27 on x86_64/arm64 architectures.

**Best for:**

- Maximum face detection accuracy
- Photos with challenging angles or lighting
- Group photos with partially obscured faces

## Configuration

!!! example ""
    We recommend that only advanced users and developers change these parameters.

### Detection Settings

| Environment Variable           | CLI Flag              | Default                 | Description                                                                |
|--------------------------------|-----------------------|-------------------------|----------------------------------------------------------------------------|
| PHOTOPRISM_FACE_ENGINE         | --face-engine         | auto                    | Detection engine (`auto`, `pigo`, `onnx`). `auto` uses ONNX when available |
| PHOTOPRISM_FACE_ENGINE_THREADS | --face-engine-threads | runtime.NumCPU()/2 (≥1) | Number of ONNX inference threads; ignored by Pigo                          |
| PHOTOPRISM_FACE_ANGLE          | --face-angle          | -0.3,0,0.3              | Detection angles in radians for Pigo multi-angle scanning                  |
| PHOTOPRISM_FACE_SIZE           | --face-size           | 50                      | Minimum size of faces in `PIXELS` (20-10000)                               |
| PHOTOPRISM_FACE_SCORE          | --face-score          | 9.0                     | Minimum face `QUALITY` score (1-100)                                       |
| PHOTOPRISM_FACE_OVERLAP        | --face-overlap        | 42                      | Face area overlap threshold in `PERCENT` (1-100)                           |

### Clustering Settings

!!! danger ""
    It is strongly recommended that you run the "photoprism faces reset" command in a terminal to remove existing clusters and mappings after changing any of the clustering parameters, as otherwise inconsistencies may result in unexpected behavior or errors.

| Environment Variable           | CLI Flag               | Default  | Description                                                                            |
|--------------------------------|------------------------|----------|----------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_CLUSTER_SIZE   | --face-cluster-size    | 80       | Minimum size of automatically clustered faces in `PIXELS` (20-10000)                   |
| PHOTOPRISM_FACE_CLUSTER_SCORE  | --face-cluster-score   | 15       | Minimum `QUALITY` score of automatically clustered faces (1-100)                       |
| PHOTOPRISM_FACE_CLUSTER_CORE   | --face-cluster-core    | 4        | `NUMBER` of faces forming a cluster core (1-100)                                       |
| PHOTOPRISM_FACE_CLUSTER_DIST   | --face-cluster-dist    | 0.64     | Similarity `DISTANCE` of faces forming a cluster core (0.1-1.5)                        |
| PHOTOPRISM_FACE_MATCH_DIST     | --face-match-dist      | 0.46     | Similarity `OFFSET` for matching faces with existing clusters (0.1-1.5)                |


### Tuning Tips

- A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher value being more aggressive and leading to larger clusters with more false positives.
- To cluster a smaller number of faces, you can reduce the kernel to 3 or 2 similar faces.
- The ONNX engine typically provides better results on challenging photos (angles, occlusions, lighting) compared to Pigo.
- Use `FACE_ENGINE=auto` to automatically select the best available engine.

## Face Embeddings

After detection, PhotoPrism generates 512-dimensional embedding vectors using TensorFlow to characterize each face. These embeddings are used to:

1. **Match faces** across different photos
2. **Cluster similar faces** using the DBSCAN algorithm
3. **Assign faces to people** with manual confirmation

### Normalization

All face embeddings are L2-normalized to unit length (‖x‖₂ = 1) at:

- Creation time (after TensorFlow inference)
- Midpoint calculation when merging clusters
- Deserialization when loading from the database

This normalization ensures that Euclidean distance comparisons are equivalent to cosine similarity, aligning with FaceNet research standards.

## Commands

[Learn more about CLI commands ›](cli.md#face-detection-commands)

## Performance Improvements

Recent optimizations have significantly improved face detection and clustering:

| Benchmark                   | Before              | After               | Improvement     |
|-----------------------------|---------------------|---------------------|-----------------|
| Embedding Distance          | ~242 ns/op          | ~155 ns/op          | 36% faster      |
| Embeddings Midpoint         | ~194 µs/op, 528 KB  | ~99 µs/op, 4 KB     | 49% faster, 99% less memory |
| Face Matching (1024 faces)  | 1024 comparisons    | ~16 comparisons     | 98% fewer evaluations |
| Cluster Materialization     | ~29.8 µs/op, 384 allocs | ~14.8 µs/op, 64 allocs | 50% faster, 83% fewer allocations |

These improvements mean:

- **Faster indexing** of large photo collections
- **Lower memory usage** during face clustering
- **Quicker face matching** when organizing people
- **More efficient** distance calculations

<!-- ## Troubleshooting

### Manual Cluster Merging Warnings

When optimizing face clusters, you may see warnings like:

```
faces: retained manual clusters after merge: kept 4 candidate cluster(s) [...] 
for subject <uid> because markers still reference them
```

This informational message indicates that some manually created face clusters couldn't be merged because their embeddings are too far apart. This can happen when:

- The same person has very different appearances (age, lighting, angles)
- Some faces were incorrectly assigned to the person
- Detection engine differences created inconsistent embeddings

**To resolve:**

1. **Re-index with consistent engine:**
   ```bash
   docker compose exec photoprism photoprism faces reset --engine=onnx
   ```

!!! danger ""
    The `faces reset` command will delete all existing face markers and clusters. Make sure you have backups if needed, as this operation cannot be undone.


2. **Review manual clusters** in the UI and remove outliers

3. **Retry optimization:**
   ```bash
   docker compose exec photoprism photoprism faces optimize --retry
   ```

4. **Audit specific subjects:**
   ```bash
   docker compose exec photoprism photoprism faces audit --subject=<uid>
   ```

The optimizer has safeguards to prevent infinite retries:

- Each manual cluster has a retry counter (default max: 1)
- Warnings only appear when the counter increments
- Set `PHOTOPRISM_FACE_MERGE_MAX_RETRY=0` for unlimited retries
- Use `--retry` flag to clear counters after manual cleanup
-->

