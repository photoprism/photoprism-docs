# Development Environment (Fedora 32)

*Note: This is contributed content intended for advanced users. If you find any errors or want to improve something, click :material-pencil: to make changes and send a pull request.*

Before you start, make sure you have [Git](https://git-scm.com/downloads) and `Development Tools` installed on your system (git, gcc, g++, llvm, cmake, etc...).

Instead of using Docker, you can create your own development environment.
You'll need:

* [Go](https://golang.org/dl/) >= 1.11
* [TensorFlow for C](https://www.tensorflow.org/install/lang_c)
* [Make](http://www.gnu.org/software/make//make.html)
* [NPM](https://nodejs.org/en/download/)
* [MySQL](https://dev.mysql.com/downloads/mysql/) (if you don't want to leverage sqlite)

Without Docker, you won't be able to use our other Dockerfiles (e.g. for TensorFlow).

**Step 1:** Run [Git](https://git-scm.com/downloads) to clone the project's:

```
git clone git@github.com:tensorflow/tensorflow.git
git clone git@github.com:photoprism/photoprism.git
```

**Step 2:** Install required packages:

```
sudo dnf install golang darktable intltool nodejs npm
```

*Note: This setup is for development and testing purposes only.*

**Step 3:** Download Bazel wrapper to build tensorflow:

Consult the [TensorFlow Docs](https://www.tensorflow.org/install/source#configure_the_build) for configuration options.

```
go get github.com/bazelbuild/bazelisk
alias bazel='bazelisk'
cd tensorflow
bazel build --config=v1 //tensorflow/tools/lib_package:libtensorflow
sudo tar -C /usr/local/ -xvf $HOME/.cache/bazel/_bazel_$USER/<SOME_HASH>/execroot/org_tensorflow/bazel-out/k8-opt/bin/tensorflow/tools/lib_package/libtensorflow.tar.gz
```

*Note: Your SOME_HASH value will depend on your build, go find it!*

**Step 4:** Build PhotoPrism:

```
cd photoprism
make
```

**Step 5:** Enjoy an amazing application ;-)

Depending on your system's configuration, you might need to update your ldconfig

*Add a configuration file which persists reboots*

```
sudo echo '/usr/local/lib/' >> /etc/ld.so.conf.d/usrlocallib.conf
sudo ldconfig
```

*Update your shell's environment which will not persist upon reboot*

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
sudo ldconfig
```
