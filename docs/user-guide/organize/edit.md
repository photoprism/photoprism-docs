# Viewing and Editing Picture Details

When you click on a title in the cards view or :material-pencil: in the full screen viewer, you can see all the information related to a picture and perform changes to it if you have permission to do so.

=== "Cards View"
     1. Click on the title, date/time, or camera details of a picture

    ![Screenshot](img/edit-open-1-2502.jpg){ class="shadow" }

=== "Full Screen Viewer"
     1. Click on :material-pencil: in the upper right corner

    ![Screenshot](img/edit-open-3-2502.jpg){ class="shadow" }

=== "Context Menu"
     1. Select one or multiple pictures
     2. Click on context menu
     3. Click :material-pencil:

    ![Screenshot](img/edit-open-2-2502.jpg){ class="shadow" }

### Details ###

In the *Details* tab, you can view and edit general metadata such as title, date, location, camera, lens, caption, and copyright:

![Screenshot](img/edit-details-2502.jpg){ class="shadow" }

Much of this information is automatically recognized and updated while indexing. If you edit these fields, the changed values will be preserved and are not overwritten even when you reindex your library.

To quickly set new coordinates, you can paste them into *Latitude* or *Longitude* if they have the format *48.265684, 7.721380*.

Clicking the *Apply* button saves the changes you have made, but does not close the dialog, while the *Close* button closes the dialog without saving additional changes.

!!! note ""
    When performing a search, text in the *Title*, *Caption*, and *Keywords* fields can be found, while *Notes* are private and will be ignored.
    
**Geolocation Plugin**

Our community has [contributed a browser plugin](https://github.com/andyvalerio/photoprism-geolocation) that allows you to easily change the latitude and longitude of a picture by selecting its location on a map:

![Screenshot](https://valerio.nu/maps/geolocation.jpg){ class="shadow" }

This browser plugin can be installed through the [Chrome Web Store](https://chrome.google.com/webstore/detail/geolocation-plugin-for-ph/oggmpodnbdcmfiognbkkeffacpeaifch).
    
### Labels ###

In the *Labels* tab, you can [view, add and edit labels](labels.md) and see whether they have been recognized automatically or added manually.

### People ###

Open the *People* tab to see [whose face has been recognized](people.md#change-people-assignments) in the picture and [assign names to faces](people.md#assign-names-to-faces) that have not yet been recognized.

### Files ###

The *Files* tab shows you all the files that belong to a picture. If it is a RAW image, you might for example also see a JPEG version of it and an XMP sidecar file:

![Screenshot](img/edit-files-1-2502.jpg){ class="shadow" }

Click on :material-chevron-down: to see additional details such as file size, type, and codec: 

![Screenshot](img/edit-files-2-2502.jpg){ class="shadow" }

If there is [more than one JPEG or PNG file](stacks.md), a button in the file details will allow you to change the primary image displayed as a preview in albums and search results. You can also delete non-primary files or [unstack files](stacks.md) by clicking on the action buttons.