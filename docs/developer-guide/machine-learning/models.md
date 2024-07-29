# Additional Computer Vision Models

Supplementary machine learning models, e.g. for generating image captions, can be found in our <https://github.com/photoprism/photoprism-vision> repository on GitHub.

!!! example ""
    Note that this has not been officially released yet and that further documentation will be added over time.

## Installing Build Dependencies

Before installing the Python dependencies, please make sure that you have [Git](https://git-scm.com/downloads) and [Python 3.12+ (incl. pip)](https://www.python.org/downloads/) installed on your system, e.g. by running the following command on Ubuntu/Debian Linux:

```
sudo apt-get install -y git python3 python3-pip python3-venv python3-wheel
```

You can then install the required libraries in a virtual environment by either using the Makefiles we provide (i.e. run `make` in the main project directory or a subdirectory) or by manually running the following commands in a service directory, for example:

```bash
cd describe
python3 -m venv ./venv
. ./venv/bin/activate
./venv/bin/pip install --disable-pip-version-check --upgrade pip
./venv/bin/pip install --disable-pip-version-check -r requirements.txt
```

## Contributors

We would like to thank everyone involved, especially [Aatif Dawawala](https://github.com/Aatif-Dawawala) who got things rolling and contributed much of the initial code:

- [Aatif Dawawala](https://github.com/Aatif-Dawawala)
- [Niaz Faridani-Rad](https://github.com/derneuere)

[Learn more ›](https://github.com/photoprism/photoprism-vision/graphs/contributors)
 
## Submitting Pull Requests

Follow our [step-by-step guide](https://docs.photoprism.app/developer-guide/pull-requests) to learn how to submit new features, bug fixes, and documentation enhancements.

[Learn more ›](https://docs.photoprism.app/developer-guide/pull-requests)

## License and Disclaimer

The files in the <https://github.com/photoprism/photoprism-vision> repository are licensed under the [Apache License, Version 2.0](../../license/apache.md) (the “License”).

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

[Learn more ›](../../license/apache.md)