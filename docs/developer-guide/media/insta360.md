# Insta360 360° Photos and Videos

Insta360 cameras record through two fisheye lenses. Depending on the model and resolution, a capture is saved either as a single file or as several related files, which PhotoPrism groups by their original filenames. Keep the names assigned by the camera: renamed files cannot be matched to the rest of their capture.

## Photos

Insta360 photos use the `.insp` extension. An `.insp` file is a JPEG that contains the images from both lenses in one 2:1 frame, so each file is a complete photo and is indexed on its own:

```
IMG_20220701_170732_00_018.insp
IMG_20220701_170732_00_018.dng
```

A RAW `.dng` file saved alongside it shares its base name and is stacked with it, just like any other RAW/JPEG pair.

PhotoPrism does not pair `.insp` files, because photos are never split across lens files. [Insta360's MediaSDK](https://github.com/Insta360Develop/Insta360-Developer_Docs/blob/master/docs/en/sdk/x-ace-go/desktop/media.md) accepts one source file for a regular 360° photo or three or more for an HDR bracket, but never exactly two. The files of an HDR bracket share the timestamp in their names and each have their own sequence number. PhotoPrism does not merge them into one HDR image.

## Videos

Insta360 videos use the `.insv` extension, an MP4 container with additional camera metadata. How a capture is stored depends on the camera:

| Layout                       | Cameras and Modes                       | Files                                                                 |
|------------------------------|-----------------------------------------|-----------------------------------------------------------------------|
| One file per lens            | Models before the X4, at 5.7K and above | `VID_…_00_….insv` and `VID_…_10_….insv`, optionally `LRV_…_11_….insv` |
| Both lenses in one frame     | Models before the X4, below 5.7K        | one `VID_…_00_….insv`, optionally `LRV_…_11_….insv`                   |
| Two video tracks in one file | X4, X4 Air, X5, X6                      | one `VID_…_00_….insv`, optionally a `.lrv` proxy                      |

### Lens Pairs

When a camera stores one file per lens, the filenames differ only in the lens code:

| File                              | Lens Code | Role                                   |
|-----------------------------------|-----------|----------------------------------------|
| `VID_20231218_150323_00_022.insv` | `00`      | first lens, the main file of the stack |
| `VID_20231218_150323_10_022.insv` | `10`      | second lens                            |
| `LRV_20231218_150323_11_022.insv` | `11`      | low-resolution proxy (optional)        |

Files in the same folder whose names match in date, time, and sequence number belong to the same capture, and PhotoPrism stacks them under the name of the `_00` file. The two lenses are combined into a single equirectangular video, which can be viewed in the [360° viewer](../../user-guide/organize/panoramas.md), if both lens files are present and match:

- Both have square frames of identical resolution.
- Their frame rates differ by no more than 0.1 fps.
- Their durations differ by no more than one second.

The combined preview is the cover of the capture, regardless of the order in which its files were indexed, and no separate preview is created for the second lens or the proxy. If your sidecar folder is inside the originals folder, the preview created first remains the cover until you choose another one.

If the lens files have been indexed as separate items, a complete rescan combines them. The combined item keeps the archive state of the item that was indexed first, so archiving one of the other items does not archive the capture. Since both lenses are needed to view the video, the lens and proxy files of a capture stay together, and *Unstack* is not available for them.

### Single-File Videos

Videos that store both lenses side by side in one 2:1 frame are converted directly. For cameras that store the two lenses as separate video tracks in a single file, converting both tracks into one 360° video [is not supported yet](https://github.com/photoprism/photoprism/issues/5843), and neither is indexing their `.lrv` proxy files.

## References

| Title                                                      | URL                                                                                                          |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Insta360: How to Edit and Reframe 360 Videos (File Naming) | https://www.insta360.com/blog/tips/how-to-edit-and-reframe-360.html                                          |
| Insta360 MediaSDK: Stitching Input Files                   | https://github.com/Insta360Develop/Insta360-Developer_Docs/blob/master/docs/en/sdk/x-ace-go/desktop/media.md |
| Insta360 Desktop MediaSDK for C++                          | https://github.com/Insta360Develop/Desktop-MediaSDK-Cpp                                                      |

## Related GitHub Issues

- [Media: Render original-format 360° files (Insta360 .insv/.insp, fisheye DNG) via FFmpeg #5711](https://github.com/photoprism/photoprism/issues/5711)
- [Index: Stack Insta360 capture files that arrive after the capture was indexed #5839](https://github.com/photoprism/photoprism/issues/5839)
- [Media: Improve Insta360 photo and video support #5843](https://github.com/photoprism/photoprism/issues/5843)
