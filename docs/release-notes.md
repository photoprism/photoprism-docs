# Release Notes

!!! tip "Preview Builds"
    Update your `docker-compose.yml` to use `photoprism/photoprism:preview` instead of
    `photoprism/photoprism:latest` for testing our development preview.

### September 25, 2021 ###

Build [210925-96168e4b](https://drone.photoprism.app/photoprism/photoprism/1895)

- [Recognizes faces so that specific people can be found](https://github.com/photoprism/photoprism/issues/22)
- UX: [Improved UI design, navigation, and wording](https://github.com/photoprism/photoprism/search?o=desc&q=UX&s=committer-date&type=commits)
- Search: [Omit full text index if query is too short](https://github.com/photoprism/photoprism/issues/1517)
- Search: [Added `keywords:…`, `subjects:…`, and `albums:…` filters](https://github.com/photoprism/photoprism/issues/882)
- Places: [Internationalized maps incl RTL support](https://github.com/photoprism/photoprism/issues/1391)
- Labels: [Added photo counts to overview page](https://github.com/photoprism/photoprism/issues/584) 
- Albums: [Fixed share expiration date in form label](https://github.com/photoprism/photoprism/issues/621)
- Calendar: [Empty month albums are hidden](https://github.com/photoprism/photoprism/issues/1456)
- Viewer: [Photos will be updated when search filters change](https://github.com/photoprism/photoprism/issues/1343)
- Index: [Ignore Synology `@eaDir` folders](https://github.com/photoprism/photoprism/issues/1543)
- Import: [Ignore dot files listed in `.ppignore`](https://github.com/photoprism/photoprism/issues/1348)
- Upload: [Added more detailed error logs](https://github.com/photoprism/photoprism/issues/1486)
- Videos: [Skip related images when downloading](https://github.com/photoprism/photoprism/issues/1436)
- Videos: [Added .mp as known MP4 file extension](https://github.com/photoprism/photoprism/issues/1501)
- Videos: [Default to UTC as metadata time zone](https://github.com/photoprism/photoprism/issues/1388)
- Exiftool: [Enabled large file support](https://github.com/photoprism/photoprism/issues/1401)
- Metadata: [Improved Exif parser with cycle detection](https://github.com/photoprism/photoprism/issues/1326)
- Metadata: [Support for long projection type names like transverse-cylindrical](https://github.com/photoprism/photoprism/issues/1508)
- Config: [Added RAW file extension blacklists for Darktable and RawTherapee](https://github.com/photoprism/photoprism/issues/1362)
- Config: [Added disable options for image classification and facial recognition](https://github.com/photoprism/photoprism/commit/a1822f9b19753140c14f4ff0242f5d931b0cae9b)
- Config: [Added support for non-root site URLs](https://github.com/photoprism/photoprism/issues/425)
- Config: [Added content delivery network URL option](https://github.com/photoprism/photoprism/issues/1351)
- MariaDB: [Set explicit table engine, charset, and collation](https://github.com/photoprism/photoprism/issues/1371)
- MariaDB: [Added log message for old versions with broken table name resolution](https://github.com/photoprism/photoprism/issues/1544)
- Docker: [Added `HOME` env for Darktable & RawTherapee](https://github.com/photoprism/photoprism/issues/1525)
- Docker: [Single multi-arch image for AMD64, ARM64, and ARMv7](https://github.com/photoprism/photoprism/issues/1158)

### May 23, 2021 ###

[210523-b1856b9d-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1375/1/0),
[210523-b1856b9d-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1375/2/0)

- RAW: [Added RawTherapee flag to use existing sidecar files](https://github.com/photoprism/photoprism/issues/1267)
- Import: [Never remove ignored folders such as for Syncthing](https://github.com/photoprism/photoprism/issues/1319)

### May 20, 2021 ###

[210520-4b32bac7-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1366/1/0),
[210520-4b32bac7-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1366/2/0)

- Docker: [Fixed home directory permissions in new base image](https://github.com/photoprism/photoprism/issues/1301)
- HEIF: [Test if JPEG was already rotated based on video metadata](https://github.com/photoprism/photoprism/blob/develop/docker/scripts/heif-convert.sh)

### May 19, 2021 ###

[210519-24b5c7e6-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1355/1/0),
[210519-24b5c7e6-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1355/2/0)

- Metadata: [Upgraded Exiftool to fix security issue](https://github.com/photoprism/photoprism/issues/1302)

### May 18, 2021 ###

[210518-80981c25-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1351/1/0),
[210518-80981c25-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1351/2/0)

- Safari: [Fixed PWA file download on iOS](https://github.com/photoprism/photoprism/issues/895)
- Docker: [Added config example for scheduled background tasks](https://dl.photoprism.org/docker/scheduler/)
- Docker: [Updated base image includes Darktable 3.4.1, RawTherapee 5.8, and FFmpeg 4.3.2](https://github.com/photoprism/photoprism/commit/77ddcecf29c95e1b33ba11046fd002ed3d408382)
- TensorFlow: [Improved error handling](https://github.com/photoprism/photoprism/issues/1270)
- Translations: [Updated French](https://github.com/photoprism/photoprism/pull/1286)

### May 5, 2021 ###

[210505-d3e53a89-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1311/1/0),
[210505-d3e53a89-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1311/2/0)

- UI: [Improved RTL (right-to-left language) alignment](https://github.com/photoprism/photoprism/pull/1220)
- RAW: [Added config options to disable specific converters](https://github.com/photoprism/photoprism/issues/1245)
- Metadata: [Preserve stopwords in existing keywords](https://github.com/photoprism/photoprism/issues/1153)
- Metadata: [Allow single quotes in keywords](https://github.com/photoprism/photoprism/issues/1196)
- WebDAV: [Keep favorite flag when uploading via PhotoSync](https://github.com/photoprism/photoprism/issues/1210)
- Translations: Updated [Dutch](https://github.com/photoprism/photoprism/pull/1247)
  and [German](https://github.com/photoprism/photoprism/commit/c9795495ee5b2a57be8ddcdb16ca29cfab018bb4)

### April 26, 2021 ###

[210426-da6e948f-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1263/1/0),
[210426-da6e948f-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1263/2/0)

- UI: [Added Yellowstone theme for sponsors, unlocked Grayscale theme for everyone](https://github.com/photoprism/photoprism/commit/180e46b95f52a5ef2d67ea8ac5e1d8a9b08ef970)
- Metadata: [Support for XMP sidecar CreateDate and Keywords](https://github.com/photoprism/photoprism/issues/1151)
- Metadata: [Merge keywords from different sources](https://github.com/photoprism/photoprism/issues/1153)
- Translations: Updated [Hebrew](https://github.com/photoprism/photoprism/pull/1221)
  
### April 22, 2021 ###

[210422-97e75b04-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1239/1/0),
[210422-97e75b04-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1239/2/0)

- UX: [Improved touch event accuracy](https://github.com/photoprism/photoprism/issues/1048)
- UX: [Optimized rendering on small screens](https://github.com/photoprism/photoprism/commit/b07ba63108dace2a8d5b2df18a06647252a36272)
- UX: [Fixed autocomplete in "add to album" dialog](https://github.com/photoprism/photoprism/issues/1130)
- HEIF: [Prevent redundant sidecar JPEG files](https://github.com/photoprism/photoprism/issues/1200)
- Backup: [Added command flags and usage docs](https://github.com/photoprism/photoprism/issues/1190)
- Translations: Added [Danish](https://github.com/photoprism/photoprism/commits?author=tcarlsen) 
  and [Kurdish](https://github.com/photoprism/photoprism/commits?author=Hrazhan)

### February 22, 2021 ###

[210222-ac5a9d5e-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1149/1/0),
[210222-ac5a9d5e-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1149/2/0)

- UX: [Autofocus for input fields and confirm on enter](https://github.com/photoprism/photoprism/issues/1078)
- Restore: [Find YAML album backups in originals folder](https://github.com/photoprism/photoprism/commit/32ef03083d9414e0ab1f52bbb3837251e0438689)
- Metadata: [Improved location labels and moments](https://github.com/photoprism/photoprism/commit/d42eb4e01b8844d46f7332e1b8d8dc7a18e41a14)
- Thumbnails: [Fixed auto-rotation for HEIF, TIFF, and PNG images](https://github.com/photoprism/photoprism/issues/1064)
- Translations: [Added Norwegian (Bokmål)](https://github.com/photoprism/photoprism/pull/1079)

### February 17, 2021 ###

[210217-49039368-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1113/1/0),
[210217-49039368-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1113/2/0)

- Videos: [Optimized transcoding parameters](https://github.com/photoprism/photoprism/issues/703)
- Videos: [Use AAC audio for MP4 transcoding](https://github.com/photoprism/photoprism/issues/1061)  
- Metadata: [Default to landscape orientation if data is invalid](https://github.com/photoprism/photoprism/issues/1052)
- Translations: [Updated Brazilian Portuguese](https://github.com/photoprism/photoprism/pull/1053)

### February 16, 2021 ###

[210216-4939e36a-Linux-x86_64](https://drone.photoprism.app/photoprism/photoprism/1100/1/0),
[210216-4939e36a-Linux-aarch64](https://drone.photoprism.app/photoprism/photoprism/1100/2/0)

- UX: Automatically hide scrollbar in photo viewer and Places
- Delete: [Permanently remove all related sidecar files](https://github.com/photoprism/photoprism/issues/167#issuecomment-779179817)
- Videos: [Added transcoding config options](https://github.com/photoprism/photoprism/issues/703)
- Videos: [Added batch transcoding via convert command](https://github.com/photoprism/photoprism/issues/703)
- Metadata: [Remove estimate when setting a new country](https://github.com/photoprism/photoprism/issues/1018)
- Metadata: [Workaround for Exif strings containing newlines](https://github.com/dsoprea/go-exif/issues/55)

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
