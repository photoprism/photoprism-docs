# Indexing Your Originals #

!!! info ""
    If you're using PhotoPrism for the first time, make sure your photo and video 
    collection is properly configured as *originals* folder.
    See installation instructions in [Getting Started](../../getting-started/index.md) for details.
    When starting with an empty folder, you need to add or upload files first.

1. Go to *Library* using the main navigation

2. Select a sub-folder or keep the default to index all files

3. Select *Complete Rescan* to re-index all originals, including already indexed and unchanged files

4. Press *Start* to start indexing

![Screenshot](img/index-dark.jpg){ class="shadow" }

!!! info ""
    You can use [WebDAV](webdav.md)-compatible apps, including Microsoft's Windows Explorer and Apple's Finder, 
    to add files to your *originals* folders from a remote computer or mobile device.

!!! tip "NSFW"
    An NSFW detector can be enabled to automatically mark images with potentially objectionable content as 
    private. Note that this feature is only partially reliable.

#### Ignoring Files and Folders ####

Hidden files and folders that start with a `.`, `@`, `_.`, or `__` like `__MACOSX` are automatically ignored. Other names to be 
ignored can be added to a `.ppignore` file in the *originals* or *import* folder it should affect.
You can put it either in the main folder or in a subfolder to limit the scope.

Example:

```
# ignore a directory by its name
foo
# ignore all files
*.*
# ignore all files with gif extension
*.gif
# ignore videos which name start with MVI
MVI_*.MOV
# or
MVI_*.*
```

Names in the same directory and in all subdirectories are ignored. You can use `*` as a wildcard.

Files and folders that have already been indexed cannot be retroactively removed from the index
using a `.ppignore` file. Adding their name won't remove them from PhotoPrism.

!!! tldr ""
    If you are a new user and files or folders have already been indexed, it is generally easiest to reset the database and start with a new index by running `photoprism reset` in a [terminal](../../getting-started/docker-compose.md#command-line-interface).

#### When should "Complete Rescan" be selected? ####

If you select this option, all files in the *originals* folder will be re-indexed, including already indexed and unchanged files.

We recommend performing a complete rescan after major updates to take advantage of new search filters and sorting options. Be sure to [read the notes for each release](../../release-notes.md) to see what changes have been made and if they might affect your library, for example, because of the file types you have or because new search features have been added. If you encounter problems that you cannot solve otherwise (i.e. before reporting a bug), please also try a rescan and see if it solves the problem.

!!! tldr ""
    Manually entered information such as labels, people, titles or descriptions will not be modified when indexing, even if you perform a "complete rescan".

#### Automatic Indexing ####

Indexing is triggered automatically when files are [synced with the *originals* folder via WebDAV](../sync/webdav.md).

The default safety delay for automatic indexing is 5 minutes. You can change it through the [PHOTOPRISM_AUTO_INDEX](../../getting-started/config-options.md#index-workers) config option.