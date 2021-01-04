# Release Notes

!!! tip "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of
    `photoprism/photoprism:latest` for testing our development preview.
    The preview image for ARM64 is `photoprism/photoprism-arm64:preview`.

### Development Preview ###

- Config: Added [auto index & import](https://github.com/photoprism/photoprism/issues/281) defaults to [Dockerfiles](https://github.com/photoprism/photoprism/commit/1d9ade4c22bba01e03182b04d5b819e0ee6211a5)
- Import: [Extract metadata with ExifTool before moving](https://github.com/photoprism/photoprism/issues/810)
- Import: Automatically create folder albums
- Help: Updated WebSocket page
- UX: Added `UI.Zoom` setting to [re-enable page zoom](https://github.com/photoprism/photoprism/issues/799)
- UI: Updated default theme
- Translations: Added Hebrew & Japanese
- Albums & Cards View: Reduced tile size on large screens
- WebDAV: Less verbose logging

### January 2, 2021 ###

[210102-af71e5f7-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/613/1/0),
[210102-af71e5f7-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/613/2/0)

- WebDAV: Uploads and other changes trigger [auto indexing / importing](https://github.com/photoprism/photoprism/issues/281)
- Config: Use random hash for improved preview token security 
- UX: Disabled page zoom so that app feels more native on mobile devices
- UX: Reduced min password length to 4 characters
- UX: Improved [docker-compose.yml examples](https://dl.photoprism.org/docker/)
- UX: Reduced icon size in "add to album" dialog

### December 31, 2020 ###

[201231-8e22fbf8-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/601/1/0),
[201231-8e22fbf8-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/601/2/0)

- Initial Stable Release
