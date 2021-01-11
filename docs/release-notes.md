# Release Notes

!!! tip "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of
    `photoprism/photoprism:latest` for testing our development preview.
    The preview image for ARM64 is `photoprism/photoprism-arm64:preview`.

### Development Preview ###

- UX: [Removed lag when selecting pictures](https://github.com/photoprism/photoprism/issues/477)
- UX: Tweaked tile size breakpoints in *Albums*, *Labels*, and *Photos*
- UX: [Added tooltips to navigation expand and minimize buttons](https://github.com/photoprism/photoprism/issues/823)
- UX: [Improved clipboard performance](https://github.com/photoprism/photoprism/issues/477)
- UX: [Preload additional search results](https://github.com/photoprism/photoprism/issues/500)
- UX: [Removed image loading spinners for faster rendering](https://github.com/photoprism/photoprism/issues/862)
- Thumbnails: [Added cache control headers for improved performance](https://github.com/photoprism/photoprism/issues/822)
- Album Covers: [Cache will be flushed after updating private flags](https://github.com/photoprism/photoprism/issues/807)
- Search: [Improved performance of photos query](https://github.com/photoprism/photoprism/commit/dcf94e26a53e2c3e78c9998f6e7b442fbbf3d544)
- [PWA](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps): Added service worker so that app can be installed [more easily](https://github.com/photoprism/photoprism/issues/852)
- [PWA](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps): [Enabled auto-rotate](https://github.com/photoprism/photoprism/issues/744)
  so that photos may be viewed in landscape mode
- Frontend: Removed [unused dependencies](https://github.com/photoprism/photoprism/pull/824) and 
  [reduced build size](https://github.com/photoprism/photoprism/pull/836)
- Translations: Updated [Russian](https://github.com/photoprism/photoprism/pull/837), 
  [French](https://github.com/photoprism/photoprism/pull/849),
  [Simplified Chinese](https://github.com/photoprism/photoprism/commit/614f93f696c7a180ff8196a01d3a10881847d459), and
  [German](https://github.com/photoprism/photoprism/commit/e015e17f3f2b7d29d2d7d71518b9d8657daff99c)
- Indexing: Automatically create [JPEGs for related media files](https://github.com/photoprism/photoprism/issues/813) as well
- Import: Improved [error handling](https://github.com/photoprism/photoprism/issues/261) when the file system becomes unavailable
- Config: Added optional gzip compression for built-in web server
- Config: Limit number of indexing workers to half the number of physical cores by default to 
  avoid [high load](https://twitter.com/miguelarios_/status/1347775696492503040) on hyper-threading capable CPUs

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
