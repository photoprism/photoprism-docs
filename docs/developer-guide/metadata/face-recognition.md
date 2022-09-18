# Face Recognition

To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism first extracts crops from your images using the [Pigo face detection library](https://github.com/esimov/pigo). It is based on [pixel intensity comparisons](https://dl.photoprism.app/pdf/20140820-Pixel_Intensity_Comparisons.pdf).

These are then fed into TensorFlow to [compute 512-dimensional vectors for characterization](https://dl.photoprism.app/pdf/20150101-FaceNet.pdf).

In the final step, the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) attempts to cluster these so-called face embeddings so that they can be assigned to people with a few clicks.

## Configuration

!!! example ""
    We recommend that only advanced users and developers change these parameters.

|          Environment          |       CLI Flag       | Default  |                                       Description                                       |
|-------------------------------|----------------------|----------|-----------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_SIZE          | --face-size          |       50 | minimum size of faces in `PIXELS` (20-10000)                                            |
| PHOTOPRISM_FACE_SCORE         | --face-score         | 9.000000 | minimum face `QUALITY` score (1-100)                                                    |
| PHOTOPRISM_FACE_OVERLAP       | --face-overlap       |       42 | face area overlap threshold in `PERCENT` (1-100)                                        |
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  |       80 | minimum size of automatically clustered faces in `PIXELS` (20-10000) *sponsors only*    |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score |       15 | minimum `QUALITY` score of automatically clustered faces (1-100) *sponsors only*        |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  |        4 | `NUMBER` of faces forming a cluster core (1-100) *sponsors only*                        |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | 0.640000 | similarity `DISTANCE` of faces forming a cluster core (0.1-1.5) *sponsors only*         |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | 0.460000 | similarity `OFFSET` for matching faces with existing clusters (0.1-1.5) *sponsors only* |

- A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher value being more aggressive and leading to larger clusters with more false positives.
- To cluster a smaller number of faces, you can reduce the kernel to 3 or 2 similar faces.

## External Resources ##

- https://cheppers.com/deploying-distributed-face-recognition-application-kubernetes - Deploying a distributed face-recognition application with Kubernetes
- http://dlib.net/ - Machine learning library, good for face recognition
- https://github.com/Kagami/go-face - implements face recognition for Go using [dlib](http://dlib.net/)
- https://hackernoon.com/face-recognition-with-go-676a555b8a7e - face recognition howto using Kagami/go-face
- https://github.com/esimov/pigo - Pigo is a face detection library implemented in Go
- https://gocv.io/ - GoCV gives access to the [OpenCV](https://opencv.org/) 4 computer vision library
- https://github.com/davidsandberg/facenet - Face Recognition using Tensorflow (Python, not Go)

