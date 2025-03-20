# `settings.yml`

User interface, download, and indexing preferences are stored in a `settings.yml` file, located in the *config path*. If it does not exist yet, it will be created automatically.

Experienced users may edit this file directly to change certain settings, as not all of them can be changed through the user interface.

!!! tldr ""
    Note that changes to the `settings.yml` file require a restart to take effect and that [settings changed through the web interface](../../user-guide/settings/general.md) will also be saved to this file. We therefore recommend that you only edit it manually while your instance is stopped.

### File Format ###

You can use any text editor to [create or modify YAML config files](../../developer-guide/technologies/yaml.md). However, it is important that related values, e.g. [key-value pairs](../../developer-guide/technologies/yaml.md#key-value-pairs), start at the same indentation level and that spaces are used for indentation, for example:

```yaml
Index:
  Path: /
  Convert: true
  Rescan: false
  SkipArchived: false
```

To avoid ambiguity, it is recommended to enclose text strings in `"` (double quotes), especially if they contain spaces, a colon, or other special characters.

### Global Defaults

User settings can optionally be initialized from a `settings.yml` file located in the same folder as the ↪ [`defaults.yml`](defaults.md) file, e.g. `/etc/photoprism`.

## Sections

### UI

The `UI` section allows you to change general user interface settings, such as which theme, language, time zone, and start page to use by default:

```yaml
UI:
  Scrollbar: true
  Zoom: false
  Theme: default
  Language: en
  TimeZone: UTC
  StartPage: default
```

If you set `Scrollbar` to `false`, the browser scrollbar will be hidden regardless of which device you use and which page you are on. This is generally not recommended, but can be useful e.g. when taking screenshots.

Setting `Zoom` to `true` allows you to enlarge the user interface with gestures on mobile devices, making the app feel more like a regular web page. This can be useful for visually impaired users so that they can magnify text and images when needed.

`Theme` and `Language` change the theme and language of the user interface and correspond to the settings dropdowns you find when navigating to [Settings > General](../../user-guide/settings/general.md).

### Search

In the `Search` section, you can turn off the list view and the display of titles and captions in search results:

```yaml
Search:
  BatchSize: -1
  ListView: true
  ShowTitles: true
  ShowCaptions: true
```

The optional `BatchSize` setting allows you to configure how many search results are fetched from the backend with each request. We recommend that you do not change the default.

### Albums

These settings allow you to change the default sort order for newly created albums, as well as configure or disallow downloads of entire albums:

```yaml
Albums:
  Order:
    Album: added
    Folder: added
    Moment: oldest
    State: newest
    Month: oldest
  Download:
    Name: share
    Disabled: false
    Originals: true
    MediaRaw: false
    MediaSidecar: false
```

For details on the download settings, see the section below.

### Downloads

The following settings allow you to configure file downloads through the user interface:

```yaml
Download:
  Name: file
  Disabled: false
  Originals: true
  MediaRaw: false
  MediaSidecar: false
```

The `Name` setting determines which file names are used when downloading pictures from search results or in the photo viewer. Currently, the following options are supported:

- `file` uses the actual file name in the *originals* folder
- `original` uses the original file name if the file was imported
- `share` uses a share-friendly file name based on the title and creation date

Note that your choice will not affect the file names in ZIP archives when you download complete albums, as they always use share-friendly names. However, we may add settings for this in a future release.

In case `Originals` is set to `true`, only the files in the *originals* folder will be downloaded, but not any files that were automatically created in the *sidecar* folder. This is the recommended default.

If you set `MediaRaw` to `true`, RAW image files are downloaded automatically, for example when you click the download button in the photo viewer.

Setting `MediaSidecar` to `true` will also download sidecar files as used for XMP metadata. This is generally not recommended except for some professional workflows.

### Library

These settings affect which files are [stacked](../../user-guide/organize/stacks.md), as well as your preferences when indexing or importing files:

```yaml
Import:
  Path: /
  Move: false
  Dest: 2006/01/20060102_150405_82F63B78.jpg
Index:
  Path: /
  Convert: true
  Rescan: false
  SkipArchived: false
Stack:
  UUID: true
  Meta: true
  Name: false
```

Since you can also change these settings in [Settings > Content](../../user-guide/settings/library.md#stacks) and in the [Library UI](../../user-guide/library/originals.md), it is not necessary to edit them directly in the `settings.yml` configuration file.

!!! note ""
    The date and time placeholders for the **optional** destination file path pattern in `Import` > `Dest` are described in [the *time* package docs](https://pkg.go.dev/time#Layout). Using a different 8 digit hex number such as `12345678` for the [CRC32 checksum](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) and `.ext` instead of `.jpg` for the file extension will work as well. Invalid and empty patterns are ignored and the default is used instead. [Learn more ›](../../user-guide/library/import.md#changing-the-import-file-path)