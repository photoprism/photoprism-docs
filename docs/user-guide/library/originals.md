# Indexing Originals #

!!! info
    If you're using PhotoPrism for the first time, make sure your photo and video 
    collection is properly configured as *originals* folder.
    See installation instructions in [Getting Started](../../getting-started/index.md) for details.
    When starting with an empty folder, you need to add or upload files first.


1. Go to *Library* using the main navigation

2. Select a sub-folder or keep the default to index all files

3. Select *Complete Rescan* to re-index all originals, including already indexed and unchanged files

4. Press *Start* to start indexing


![Screenshot](img/index.png)


!!! tip
    You may use [WebDAV](webdav.md) for adding files to the *originals* folder.
    This is especially helpful if PhotoPrism is running on a remote server.

!!! tip 
    A NSFW detector can be enabled to automatically flag pictures as private which 
    may have offensive content. Note that this is only somewhat reliable. 

#### Ignoring Files and Folders ####

Hidden files and folders starting with a `.` or `@` will be ignored automatically. 
Other names to be ignored can be added to a `.ppignore` file in the originals or import folder it should apply.

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

Names will be ignored in the same directory and all subdirectories. You may use `*` as a wildcard.

Note that already indexed files and folders won't be removed from index retroactively. In this case, adding them to a `.ppignore` file will not result in a file or folder to be removed from PhotoPrism.

If you are a new user and files or folders have already been indexed, you generally easiest 
to reset the database and start with a fresh index by running `photoprism reset` in a terminal.

#### When should "Complete Rescan" be selected? ####

If selected, all files in the *originals* folder will be re-indexed, including already indexed and unchanged files. 
This may be necessary after upgrading, especially to new major versions.

#### Automatic Indexing ####
The Indexer is triggered automatically 15 Minutes after the originals folder has been edited via WebDAV.
15 Minutes is the default value, it can be changed using the respective [config option](../../getting-started/config-options.md).
