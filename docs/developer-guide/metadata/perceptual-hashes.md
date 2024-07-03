# Perceptual Image Hashes

Perceptual Image Hashing refers to the use of a fingerprint algorithm to generate a hash that correlates with the *appearance of an image* without depending on other parameters such as file size, type, name, resolution, or other metadata.

## Sorting by Visual Similarity

PhotoPrism currently [generates a perceptual hash](https://github.com/photoprism/photoprism/blob/develop/pkg/media/colors/lightmap.go) while indexing, which can be used to sort search results by visual similarity, e.g.:

- <https://demo.photoprism.app/library/browse?view=cards&order=similar>

Note, though, that it is not yet possible to automatically stack files based on this and that the hash is not 100% precise, so visually different images may have the same hash. This is because it was developed for sorting and not for stacking or finding duplicates.

## Stacking of Similar Files

Developing a user-friendly web interface for semi-automatic stacking of a large number of images based on their appearance is expected to require a significant amount of work.

A simpler solution could be to add one or more additional stacking options on the library settings page and allow them to be applied to existing pictures by pressing a button or running a terminal command, but without being able to see the result in advance or perform manual changes.

See the following issues for related feature requests: 

- [Stacks: Search + manually stack similar images #28](https://github.com/photoprism/photoprism/issues/28)
- [Stacks: Stack compressed and original version of a photo e.g. from Google Photos #1182](https://github.com/photoprism/photoprism/issues/1182)

## Related Resources

### Software Libraries & Examples

- https://github.com/corona10/goimagehash
- https://github.com/Nr90/imgsim
- https://github.com/azr/phash
- https://github.com/ajdnik/imghash
- https://github.com/burntcarrot/hashsearch
- https://github.com/dsoprea/go-perceptualhash
- https://github.com/9elt/fast-dhash
- https://github.com/Estella/ImageDNA
- https://github.com/jenssegers/imagehash

### References, Algorithms & Tutorials

- https://en.wikipedia.org/wiki/Perceptual_hashing
- https://www.microsoft.com/en-us/photodna
- https://news.microsoft.com/en-gb/2013/11/18/tacklingproliferatio/