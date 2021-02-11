# Release Notes

!!! tip "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of
    `photoprism/photoprism:latest` for testing our development preview.
    The preview image for ARM64 is `photoprism/photoprism-arm64:preview`.

### February 11, 2021 ###

[210211-b9595dd4-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1047/1/0), 
[210211-b9595dd4-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1047/2/0)

- Videos: [Native player featuring performance and UX improvements](https://github.com/photoprism/photoprism/issues/915)
- Index: [Improved detection of missing photos, files, and folders](https://github.com/photoprism/photoprism/issues/1010)

### February 8, 2021 ###

[210208-9e10ba69-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1034/1/0),
[210208-9e10ba69-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1034/2/0)

- Upload: [Adds duplicates to selected albums as well](https://github.com/photoprism/photoprism/issues/991)
- Library: [Show folder covers in Originals](https://github.com/photoprism/photoprism/issues/1011)
- Metadata: [Automatically remove orphan countries, cameras, and lenses](https://github.com/photoprism/photoprism/issues/982)
- Metadata: [Improved Exif parser](https://github.com/photoprism/photoprism/issues/990)
- Backup: [Restore archive flag from YAML files](https://github.com/photoprism/photoprism/issues/912)
- Docker: [Improved entrypoint script](https://github.com/photoprism/photoprism/issues/1000)

### January 28, 2021 ###

[210128-a82061e0-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/967/1/0),
[210128-a82061e0-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/967/2/0)

- UX: Improved theme colors and icons
- UX: Download all related media files using their current name by default
- UX: Redirect already authenticated users from /login to /browse
- Mobile: [Prevent like on touch swipe](https://github.com/photoprism/photoprism/issues/953)
- Translations: Updated German and French
- Config: Reduced auto index & import safety delay defaults
- Metadata: [Improved photo titles, removed small words from title endings](https://github.com/photoprism/photoprism/commit/57dc591b124b071cb943cca8c11e98824b65cefc)
- Metadata: Improved date extraction from current and original file names
- Metadata: [Fallback to earliest file mod time in case there is no other date](https://github.com/photoprism/photoprism/issues/930)
- Import: [Index keywords from non-primary filenames as well](https://github.com/photoprism/photoprism/issues/920)
- WebDAV: [Improved service discovery](https://github.com/photoprism/photoprism/issues/496)
- Purge: [Hide missing files in edit dialog and set new primary if needed](https://github.com/photoprism/photoprism/issues/917)
- Archive: [Physically delete files after confirmation](https://github.com/photoprism/photoprism/issues/167) (early-access feature for our [sponsors](https://www.patreon.com/photoprism) and [contributors](https://docs.photoprism.org/developer-guide/))
- Moments: [Added delete button to context menu](https://github.com/photoprism/photoprism/issues/942)
- Settings: [Added Estimates and Delete feature flags](https://github.com/photoprism/photoprism/issues/954)
- CLI: Added cleanup command to remove orphaned index entries and thumbnails

### January 21, 2021 ###

[210121-07e559df-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/882/1/0),
[210121-07e559df-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/882/2/0)

- UX: [Improved video playback and icons](https://github.com/photoprism/photoprism/issues/935)
- UX: [Restructured main navigation](https://github.com/photoprism/photoprism/issues/859)
- Mobile: [Show search field in albums](https://github.com/photoprism/photoprism/issues/937)

### January 20, 2021 ###

[210120-e7cd5e9a-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/856/1/0),
[210120-e7cd5e9a-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/856/2/0)

- API: [Apply limit, offset and sort order when searching for IDs](https://github.com/photoprism/photoprism/issues/890)
- ARM64: [Reverted database image back to arm64v8/mariadb in config example](https://github.com/photoprism/photoprism/issues/535#issuecomment-763210250)

### January 19, 2021 ###

[210119-a5399f06-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/835/1/0),
[210119-a5399f06-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/835/2/0)

- UX: Optimized user interface for [iOS and tablets](https://github.com/photoprism/photoprism/issues/832)
- UX: Improved theme colors
- UX: [Scroll position is restored when navigating back](https://github.com/photoprism/photoprism/issues/896)
- UX: Added two [dark themes](https://github.com/photoprism/photoprism/issues/700) as early-access
  feature for our [sponsors](https://www.patreon.com/photoprism) 
  and [contributors](https://docs.photoprism.org/developer-guide/)
- Translations: Added [Czech](https://github.com/photoprism/photoprism/issues/902)
- Metadata: [Estimate timezone](https://github.com/photoprism/photoprism/issues/914) 
  and [allow overwriting estimated locations](https://github.com/photoprism/photoprism/pull/918) 
- Settings: [Fixed disabling logs](https://github.com/photoprism/photoprism/issues/891)

### January 11, 2021 ###

[210111-cc05c430-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/744/1/0),
[210111-cc05c430-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/744/2/0)

- UX: Disabled preloading in live photo player to reduce memory footprint
- UX: [Updated main navigation, find all media types via /browse](https://github.com/photoprism/photoprism/issues/859)
- UX: [Removed lag when selecting pictures](https://github.com/photoprism/photoprism/issues/477)
- UX: Tweaked tile size breakpoints in *Albums*, *Labels*, and *Search*
- UX: [Added tooltips to navigation expand and minimize buttons](https://github.com/photoprism/photoprism/issues/823)
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
- Index: Automatically create [JPEGs for related media files](https://github.com/photoprism/photoprism/issues/813) as well
- Import: Improved [error handling](https://github.com/photoprism/photoprism/issues/261) when the file system becomes unavailable
- Config: [Updated docker-compose.yml examples](https://dl.photoprism.org/docker/)
- Config: [Added optional gzip compression for built-in web server](getting-started/config-options.md)
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
