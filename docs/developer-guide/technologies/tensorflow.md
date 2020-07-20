## Using TensorFlow with Go ##

<img align="right" width="100" height="100" src="https://photoprism.org/images/tensorgologo.png" alt="created by Takuya Ueda (@tenntenn)">

For an introduction please read [Understanding Tensorflow using Go](https://pgaleone.eu/tensorflow/go/2017/05/29/understanding-tensorflow-using-go/).

The TensorFlow API for Go is well suited to loading existing models and executing them within a Go application. It requires the [TensorFlow C library](https://www.tensorflow.org/install/lang_c) to be installed. A full TensorFlow installation is not needed.

It is not possible to statically link against the C library, but the [issue is known](https://github.com/tensorflow/tensorflow/issues/15563) and there might be a [fix later this year](https://github.com/bazelbuild/bazel/issues/1920). 

## Vision ##

Our long-term goal is to become an open platform for machine learning research based on real-world photo collections.

## Links ##
- https://tfhub.dev/ - TensorFlow Hub is a library for reusable machine learning modules
- https://www.tensorflow.org/install/lang_c - TensorFlow for C
- http://www.asimovinstitute.org/neural-network-zoo/ - types of neural networks explained
- http://playground.tensorflow.org/ - Experiment with neural networks in your browser
- http://jupyter.org/ - open-source web application for creating and sharing documents that contain live code
- https://developers.google.com/machine-learning/crash-course/ - Machine Learning Crash Course with TensorFlow APIs
- https://medium.com/implodinggradients/tensorflow-or-keras-which-one-should-i-learn-5dd7fa3f9ca0
- https://medium.com/analytics-vidhya/deploy-your-first-deep-learning-model-on-kubernetes-with-python-keras-flask-and-docker-575dc07d9e76 - Deploy Your First Deep Learning Model On Kubernetes With Python, Keras, Flask, and Docker
- https://medium.com/mlreview/getting-inception-architectures-to-work-with-style-transfer-767d53475bf8 - Getting Inception Architectures to Work with Style Transfer
- https://github.com/jdeng/goface - Face Detector based on MTCNN, tensorflow and golang
- https://www.tensorflow.org/tutorials/representation/word2vec - Vector Representations of Words (for searching/tagging)
- https://github.com/chtorr/go-tensorflow-realtime-object-detection - Real-time object detection with Go, Tensorflow, and OpenCV
- https://ai.googleblog.com/2018/07/accelerated-training-and-inference-with.html - Accelerated Training and Inference with the Tensorflow Object Detection API
- https://github.com/NanoNets/object-detection-sample-golang - NanoNets Object Detection API Example for Golang
- https://hub.packtpub.com/object-detection-go-tensorflow/ - Implementing Object detection with Go using TensorFlow
- https://github.com/tensorflow/tensorflow/tree/master/tensorflow/contrib/makefile - Build TensorFlow C lib statically