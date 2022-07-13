# Indexing Your Library

Most users with an existing library will want to [index their originals](originals.md) directly without using the optional import feature, leaving the file and folder names unchanged.

When [importing](import.md), files are first transferred from a temporary folder to the *originals* folder. In the process, duplicates are automatically skipped, and the imported files are given a unique file name and will be sorted by year and month.

Importing is also an efficient way to add files, since PhotoPrism does not need to search your *originals* folder to find new files.

!!! info ""
    Hidden files and folders that start with a `.` or `@` are automatically ignored. Other names to be
    ignored can be added to a `.ppignore` file in the *originals* or *import* folder it should affect.
    You can put it either in the main folder or in a subfolder to limit the scope.

## Indexing Originals

Use *index* if you want to index your photos and videos directly in the *originals* folder, leaving the file and folder names unchanged.

Your folder structure in *originals* might look like this:

   ![Screenshot](img/originals-before-after.png){ class="shadow" }
     
**During indexing:**

* Files are not renamed or moved
* Your existing folder structure remains. You might decide to have your folders displayed as albums in PhotoPrism
* Metadata from your files is read to create labels, titles and locations for your photos
* Thumbnails are rendered for JPEGs
* Optionally json and or yml files containing metadata are created

After indexing your originals folder has not been touched:

![Screenshot](img/originals-before-after.png){ class="shadow" }

### Advantages

* You keep your existing folder structure
* You can display your existing folder structure in PhotoPrism
* You can move photos between the various folders within your Originals folder.  PhotoPrism will recognize this move and update appropriately during the next index.

## Importing Files

*Importing* is more efficient when adding files as you don't need to re-index all originals to find new photos and videos.
[*Uploads*](upload.md) will also be treated as import, you can't directly upload to originals (yet).

Your initial folder structure in *import* might look like this:

   ![Screenshot](img/before-import.png){ class="shadow" }
   
**During import:**
 
* Files are moved or copied from import directory to originals directory
* In the originals directory files are renamed and get a new folder structure. The original name is saved as property of the file
* All imported files are indexed

After import using "copy" (this is the default) your folders could look like this:

   ![Screenshot](img/copy-import.png){ class="shadow" }

After import using "move" your folders might look like this:

   ![Screenshot](img/move-import.png){ class="shadow" }

### Advantages
* Unsupported files stay untouched in the import directory
* No duplicates in your originals directory


!!! info ""
    Original file and folder names are used to create keywords. 
    In case you import and index or only index a directory with the path "Vacation/Africa". All files from this folder get the keywords "vacation" and "africa".


## Conclusion
In case you have no organization in your existing photo collection and you assume you have many duplicates on various hard drives.
*Import* is the way to go. It will organize all your photos and videos due to time taken and it will avoid duplicates.

In case you have your photo collection organized nicely in folders and you prefer to keep this organization displayed in the filesystem. *Index* will be the right option for you.
