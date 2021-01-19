# Importing files to your library #

1. Add files to the *import* folder if not done already

2. Go to *Library* using the main navigation, and open the *Import* tab

3. Select a sub-folder or keep the default to import all files

4. Select *Move Files* if you want imported files to be removed from the *import* folder

5. Click on *Import*

![Screenshot](img/import.png)

!!! tip
    You may use [WebDAV](webdav.md) for adding files to the *import* folder.
    This is especially helpful if PhotoPrism is running on a remote server.

!!! attention
    Importing is not possible in [read-only mode](../settings/library.md) as it requires
    write permissions for the *originals* folder.
    
#### When should "Move Files" be selected? ####

If selected, files that have been moved to the *originals* folder, or that already exist,
will automatically be deleted from the *import* folder.
This will save storage if you don't want to keep them as backup, or for any other reason.

#### Automatic Import ####
The Importer is triggered automatically 15 Minutes after the import folder has been edited via WebDAV.
15 Minutes is the default value, it can be changed using the respective [config option](../../getting-started/config-options.md).

