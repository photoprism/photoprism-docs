# `settings.yml`

User interface, download and indexing settings are stored in the `settings.yml` file located in the *config* folder. If it does not exist yet, it will be created automatically.

Advanced users can edit the file directly to change certain settings, since not all of them can be modified through the user interface. Note that all changes require a restart to take effect, and that settings changed on the [web interface](../../user-guide/settings/general.md) will be saved in the same file. We therefore recommend that you edit it only while PhotoPrism is not running. 

!!! tldr ""
    When [editing YAML files](../../developer-guide/technologies/yaml.md), it is important that related values start at the same indentation level and that spaces are used, since tabs are not allowed. You can use any text editor for this.

### User Interface

```yaml
UI:
  Scrollbar: true
  Zoom: false
  Theme: default
  Language: en
```

If you set `Scrollbar` to `false`, the scrollbar will be disabled regardless of which browser you use and which page you are on. This is generally not recommended, but can be useful e.g. when taking screenshots.

Setting `Zoom` to `true` allows you to enlarge the user interface with gestures on mobile devices, making the app feel more like a regular web page. This can be useful for visually impaired users so that they can magnify text and images when needed.

`Theme` and `Language` change the theme and language of the user interface and correspond to the settings dropdowns you find when navigating to [Settings > General](../../user-guide/settings/general.md).

### File Downloads

```yaml
Download:
  Name: file
  Disabled: false
  Originals: true
  MediaRaw: false
  MediaSidecar: false
```

The `Name` setting determines which file names to use when downloading files. Currently, the following options are supported:

- `file` uses the actual file name in the *originals* folder
- `original` uses the original file name if the file was imported
- `share` uses a share-friendly file name based on the title and creation date

Note that your choice will not affect the file names in ZIP archives when you download complete albums, as they always use share-friendly names. However, we may add settings for this in a future release.

In case `Originals` is set to `true`, only the files in the *originals* folder will be downloaded, but not any files that were automatically created in the *sidecar* folder. This is the recommended default.

If you set `MediaRaw` to `true`, RAW image files are downloaded automatically, for example when you click the download button in the photo viewer.

Setting `MediaSidecar` to `true` will also download sidecar files as used for XMP metadata. This is generally not recommended except for some professional workflows.

### Media Library

```yaml
Import:
  Path: /
  Move: false
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

These settings affect which files are stacked, as well as your preferences when indexing or importing files.

You can also change these settings by navigating to [Settings > Library](../../user-guide/settings/library.md#stacks) and in the [Library UI](../../user-guide/library/originals.md), so it is generally not necessary to edit them directly in the config file.
