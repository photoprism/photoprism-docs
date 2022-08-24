As PhotoPrism is a complete photo management solution, it is not only possible to index existing images, but also to add / upload new files to a photo collection or delete existing photos to save storage.

There has been a debate on whether PhotoPrism should be responsible for file naming, see [Support Photos In Place on Hard Drive #41](https://github.com/photoprism/photoprism/issues/41). As soon as you want the software to create new files or merge photo libraries from different devices, there is no other way. Therefore we're going to implement a read-only mode for those who want to use it as a gallery with reduced functionality, see [Read-only mode #56](https://github.com/photoprism/photoprism/issues/56).

## Post Processing / Keyboard Shortcuts ##

After importing new images, it would be amazing to be able to quickly sort / review them. This way the library stays clean and well organized, even without applying filters to hide bad shots. Apparently this is common among users of [Adobe Bridge](https://www.adobe.com/products/bridge.html), a tool used by many professionals. They go through complete asset collections and sort photos using keyboard shortcuts, where keys toggle pre-defined tags or flags like "favorite".

## Upload ##
Idea: We can use Webassembly for performance enhancements / faster upload.
