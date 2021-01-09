# Release Notes

!!! tip "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of
    `photoprism/photoprism:latest` for testing our development preview.
    The preview image for ARM64 is `photoprism/photoprism-arm64:preview`.

### Development Preview ###

- UX: Tweaked tile size breakpoints in *Albums*, *Labels*, and *Photos*
- UX: [Added titles to navigation expand and minimize buttons](https://github.com/photoprism/photoprism/issues/823)
- UX: [Improved clipboard performance](https://github.com/photoprism/photoprism/issues/477)
- UX: Added [PWA](https://github.com/photoprism/photoprism/issues/374) service worker so that web 
  app can be installed [more easily](https://github.com/photoprism/photoprism/issues/852) #374 #852
- UX: Changed orientation from `portrait` to `any` in `manifest.json`
- UX: [Removed image loading spinners for faster rendering](https://github.com/photoprism/photoprism/issues/862)
- Thumbnails: [Added cache control headers for improved performance](https://github.com/photoprism/photoprism/issues/822)
- Album Covers: [Cache will be flushed after updating private flags](https://github.com/photoprism/photoprism/issues/807)
- Frontend: Removed [unused dependencies](https://github.com/photoprism/photoprism/pull/824) and 
  [reduced build size](https://github.com/photoprism/photoprism/pull/836)
- Translations: Updated [Russian](https://github.com/photoprism/photoprism/pull/837) and 
  [French](https://github.com/photoprism/photoprism/pull/849)
- Indexer: [JPEGs for sidecar files will be created when needed](https://github.com/photoprism/photoprism/issues/813)
- Config: [Reduced default number of workers](https://github.com/photoprism/photoprism/commit/8627153288373b9560adaf5998e715d58fd9bd80)
  to half the logical CPU cores e.g. 2 workers when there are 4 cores

### January 4, 2021 ###

[210104-7f9e806a-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/645/1/0),
[210104-7f9e806a-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/645/2/0)

- Config: Added [auto index & import](https://github.com/photoprism/photoprism/issues/281) defaults to [Dockerfiles](https://github.com/photoprism/photoprism/commit/1d9ade4c22bba01e03182b04d5b819e0ee6211a5)
- Import: [Extract metadata with ExifTool before moving](https://github.com/photoprism/photoprism/issues/810)
- Import: Automatically create folder albums
- Help: Updated WebSocket page
- UX: Added `UI.Zoom` setting to [re-enable page zoom](https://github.com/photoprism/photoprism/issues/799)
- UI: Updated default theme
- Translations: Added Hebrew & Japanese, updated Brazilian Portuguese
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
