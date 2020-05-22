###Import files from your `import` directory

1. Add files to your `import` folder. 

2. On the main navigation click Library and then Import.

3. Select the folder you want to index.

4. Select your preferred options.

5. Click import.

!!! info
    You can add photos to you import folder via your filesystem, [webdav](webdav.md)  or using PhotoPrisms [upload](upload.md) functionality.

![Screenshot](../img/Import.png)

###What happens during import
* Copy files from `import` folder to `originals` folder. Original files stay in `import` folder.
* To avoid duplicates only unique files are copied. Duplicates and unsupported file types are ignored.
* New files are [indexed](index.md) after creating JPEGs (if needed) and thumbnails.

###Import options

####Move files
In case this option is selected, no copies are created but your original files will be renamed and moved to the `originals` folder.

!!! attention
    Import is not possible in read only mode
    

