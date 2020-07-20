Since we're already linking against [TensorFlow](../technologies/tensorflow.md) and want to keep the number of dependencies small, we should investigate alternative approaches in addition to the obvious solution to use [dlib](http://dlib.net/) (which is the popular/standard way, see [go-face](https://github.com/Kagami/go-face)). [Pigo](https://github.com/esimov/pigo) is a pure Go implementation for *Face Detection*, but it can not do *Face Recognition*.

Lots of useful information provided by [Emmanuel Leroy](https://www.linkedin.com/in/emmanuel-leroy-34b406/) can be found in [[Inbox]].

![](https://www.facefirst.com/wp-content/uploads/2017/01/AdobeStock_123607404-copy.jpeg)

## Links ##
- https://cheppers.com/deploying-distributed-face-recognition-application-kubernetes - Deploying a distributed face-recognition application with Kubernetes
- http://dlib.net/ - Machine learning library, good for face recognition
- https://github.com/Kagami/go-face - implements face recognition for Go using [dlib](http://dlib.net/)
- https://hackernoon.com/face-recognition-with-go-676a555b8a7e - face recognition howto using Kagami/go-face
- https://github.com/esimov/pigo - Pigo is a face detection library implemented in Go
- https://gocv.io/ - GoCV gives access to the [OpenCV](https://opencv.org/) 4 computer vision library
- https://github.com/davidsandberg/facenet - Face Recognition using Tensorflow (Python, not Go)

