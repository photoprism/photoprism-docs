**To index files in `originals` directory:**

1. Add files to your `originals` folder.

2. On the main navigation click Library and then Originals.

3. Select your preferred options.

4. Select the folder you want to index.

5. Click index.

!!! info
    You can add photos via your filesystem or using [webdav](webdav.md).


![Screenshot](../img/Index.png)

####What the index process does:

* Read the metadata from your files to create labels, titles and locations for your photos.
* Render thumbnails for JPEGs.

####What the index process will NOT do:

* Move or rename your files.
* Delete duplicates.
* Change metadata you added manually.

####Index options:
#####Complete rescan
All files are indexed again.
In case this option is not selected only new or changed files will be indexed.

!!! info
    In case you have set read only mode to true (Can be configured in docker-compose.yml), no JPEGs can be created for your RAW files.
    
!!! tip 
    NSFW detection can be enabled (`detect-nsfw`) to flag images that may have offensive content (`nsfw` search filter).
        
    Enable `upload-nsfw` to prevent users from uploading offensive images via Web UI. 
    Note that you'll still be able to manually add such images to the `originals` or `import` folders and index them.

