# Importing Files to Originals #

!!! tldr ""
    Most users with an existing library will want to [index their originals](originals.md) directly without using the optional import feature, leaving the file and folder names unchanged. Importing first copies or moves from their source directory to the *originals* folder, which is optional.

## Manual Import

1. Add files to the *import* folder if not done already

2. Go to *Library* using the main navigation, and open the *Import* tab

3. Select a sub-folder or keep the default to import all files

4. Select *Move Files* if you want imported files to be removed from the *import* folder

5. Click on *Import*

![Screenshot](img/import-light.jpg){ class="shadow" }

!!! tip ""
    You may use [WebDAV](webdav.md) for adding files to the *import* folder.
    This is especially helpful if PhotoPrism is running on a remote server.

!!! danger ""
    Import is not possible in [read-only mode](../settings/library.md) because it requires [write permissions](../../getting-started/troubleshooting/docker.md#file-permissions) to the folder of *originals*.

### When should "Move Files" be selected?

If you select this option, files that have been moved to the *originals* folder, or that already exist, will be automatically deleted from the *import* folder.
This way you save disk space if you don't want to keep them as backup or for other reasons.

## Automatic Import

Automatic imports are disabled by default, as a wrong configuration or unsupported usage can cause files or sets of files to be imported incompletely, e.g. if you are using a slow or unreliable Internet connection, which is of particular concern with [large video or RAW files](https://github.com/photoprism/photoprism/issues/4310).

If you enable automatic imports by setting the config option [`PHOTOPRISM_AUTO_IMPORT`](../../getting-started/config-options.md#indexing) to a positive number indicating the safety delay in seconds, an import is automatically triggered after the safety delay when files are added to the *import* folder [via WebDAV](../sync/webdav.md).

[Learn more ›](../../getting-started/config-options.md#indexing)

## Changing the Import File Path

Starting with [Release 250223-b79d21907](../../release-notes.md#february-23-2025), advanced users can customize the destination file path pattern used by the import feature through the [`settings.yml`](../../getting-started/config-files/settings.md#media-library) config file, as shown in this example:

```yaml
Import:
  Dest: 2006/01/20060102_150405_82F63B78.jpg
```

The date and time placeholders for the import destination file path pattern are described in [the *time* package docs](https://pkg.go.dev/time#Layout). Using a different 8 digit hex number such as `12345678` for the [CRC32 checksum](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) and `.ext` instead of `.jpg` for the file extension will work as well. Invalid and empty patterns are ignored and the default is used instead.

[Learn more ›](../../getting-started/config-files/settings.md#media-library)

!!! note ""
    Setting a custom import file path **will not rename any files** that have already been imported, since this might cause conflicts with other tools or instances that may be accessing your files. Renaming existing files may also result in storage and/or transfer overhead with backup tools that do not recognize that files have been moved, i.e. they may create and/or transfer a new backup copy. We will consider [adding an integrated file renaming feature](../../getting-started/faq.md#can-i-use-photoprism-to-sort-files-into-a-configurable-folder-structure) once we have had time to test possible implementations for usability, performance, and security.

## Frequently Asked Questions

### Can I use PhotoPrism to sort files into a configurable folder structure?

You have complete freedom in how you name your files and folders. So if you don't like the unique names and folders used by the import feature, you can instead use external tools like [ExifTool](https://ninedegreesbelow.com/photography/exiftool-commands.html#rename), [PhockUp](https://github.com/ivandokov/phockup), or [Photo Organizer](https://www.systweak.com/photo-organizer) to reorganize your files based on their metadata.

[Learn more ›](../../getting-started/faq.md#can-i-use-photoprism-to-sort-files-into-a-configurable-folder-structure)