# FAQ #
## What is the easiest way to install PhotoPrism on Mac/Windows? ##

## Should I install PhotoPrism on my laptop or on a server? ##

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

## Where are my files saved? ##
Your original files stay in the directory you defined as Originals during the set up.

## Can PhotoPrism do backups of my files? ##

## Can I backup images from my phone directly to PhotoPrism? ##

## I removed a label but the related keyword is still existing, why? ##
Keywords come from various sources: labels, file names, folder names, locations etc. 
If a label is removed the keyword is not automatically removed because it might originated from another source.
You can delete the keyword manually on the [edit dialogue](organize/edit.md).

## What are sidecar files and where do I find them? ##
A sidecar is a file which sits along**side** your photos with the same name but different file extension/type. E.g:

 * `IMG_0101.jpg`
 * `IMG_0101.json`
 * `IMG_0101.yaml`

There are 2 types of sidecar files used by Photoprism. 

 * **json** - (Variable: `PHOTOPRISM_SIDECAR_JSON` Parameter: `--sidecar-json, -j`) - This is automatically created from the EXIF data of your photos by `exiftool`. This makes the data easily available for other scripts/apps.
 * **yaml** - (Variable: `PHOTOPRISM_SIDECAR_YAML` Parameter: `--sidecar-yaml, -y`) - This is used to back up any changes made in Photoprism to the metadata of your photos. This preserves the promise that we will not make any changes to originals while also providing any changes you have made in a plaintext format. Useful for and backup/restore and database rebuilds.

## What is the advantage of PhotoPrism being OpenSource for me as a user? ##
