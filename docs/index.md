# PhotoPrism: Browse Your Life in Pictures

PhotoPrism® is a server-based application for browsing, organizing and sharing your personal photo collection.
It makes use of the latest technologies to automatically tag and find pictures without getting in your way.

Say goodbye to solutions that force you to upload your visual memories to the cloud!

![Screenshot](img/preview.jpg)

## What to expect... ##

* clearly structured Web interface for browsing, organizing and sharing your personal photo collection
* import everything without worrying about duplicates or RAW to JPEG conversion
* reverse geocoding, XMP support and automated tagging based on Google TensorFlow
* you're welcome to play with the demo at [demo.photoprism.org](https://demo.photoprism.org)

## Getting Started ##

To simplify running PhotoPrism on a server, we strongly recommend using [Docker Compose](getting-started/docker-compose.md).
It is available for Mac, Linux and Windows.

Next, you'll have to [index](user-guide/library/import-vs-index.md) 
your library. Please be patient, this will take a while depending on the size of your photo collection.

Already indexed photos can be browsed in [Photos](user-guide/organize/browse.md) 
while videos show up in [Videos](user-guide/organize/video.md).
Counts are continuously updated in the navigation.

If files are missing, they might be in [Review](user-guide/organize/review.md) due to low quality or missing metadata.
You can turn this and other features off in [Settings](user-guide/settings/ui.md), depending on
your specific use case.

Note that this is work in progress. We do our best to provide a complete, stable version. 
[Financial support](funding.md) makes a huge difference and enables us to spend more time with this project.
Leave your email to get a [release notification](https://goo.gl/forms/KBPVGl9PCsOKrAv33).