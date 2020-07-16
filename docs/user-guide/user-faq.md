# FAQ #
## What is the easiest way to install PhotoPrism on Mac/Windows? ##

## Should I install PhotoPrism on my laptop or on a server? ##

## What kind of files can I add to PhotoPrism? ##
We aim to support all kinds of photos. You can add jpegs, live photos, pngs and various types of raw files.
In case you have trouble with a special format please let us know.
Metadata files in json/yml or xmp format are supported as well. We extract keywords out of them to organize your photo collection for you.
In addition we support videos with avc1 codec. Other formats are planned.

## Is there a mobile app available? ##
We do not offer a native app via the app stores. 
But our app is fully responsive and you can add it to the homescreen of your phone or tablet. 
This way you can use it like any other app.

**iOS:**

1. Open photoprism in the Safari browser on your phone or tablet
2. Click :material-export-variant:
3. Click add to home screen :material-plus-box-outline:

**Android:**



## How can I find/change my import/originals directories? ##


## Why do some of my photos get the import date as date instead of the date of the image creation? ##
?????


## Why do some of my photos have January 1st 1980 as date? ##
This happens in case there is a failure in your camera's time settings. 
In the [edit dialog](organize/edit.md) you can change the time of your photo.

## I do not find (some) of my photos after indexing, where are they? ##
In case you have our [quality filter](organize/review.md) enabled some of your photos might be located in the Review section.

## When do I need to do a complete rescan? ##
???

## How can I permanently delete photos? ##
Currently you can only [archive](organize/archive.md) photos using PhotoPrism. 

To permanently delete photos you need to delete them on your filesystem and start indexing your originals again.
We plan to implement permanent deletion within PhotoPrism soon.

## Where are my files saved? ##
Your original files stay in the directory you defined as Originals during the set up.

## Can PhotoPrism do backups of my files? ##

## Can I backup images from my phone directly to PhotoPrism? ##

## I removed a label but the related keyword is still existing, why? ##
Keywords come from various sources: labels, file names, folder names, locations etc. 
If a label is removed the keyword is not automatically removed because it might originated from another source.
You can delete the keyword manually on the [edit dialogue](organize/edit.md).

## What are sidecar files and where do I find them? ##
For us it is important that all the information you add to your photos like keywords, titles, labels etc is accessible to you at any time.
That's why we create json files with all those data. 

## What is the advantage of PhotoPrism being OpenSource for me as a user? ##
