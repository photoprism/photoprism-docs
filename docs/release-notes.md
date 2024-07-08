# Release Notes

!!! note ""
    You can test [**upcoming features and enhancements**](https://link.photoprism.app/roadmap) by changing the image tag from `:latest` to [`:preview`](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&name=preview) and then following [our update guide](getting-started/updates.md#development-preview) to download the newest image from [Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags) and restart your instance.

### Development Preview ###
<span class="build">Build 240708-5546a5618</span>

Our upcoming release adds support for single sign-on via [OpenID Connect (OIDC)](https://docs.photoprism.app/getting-started/advanced/openid-connect/).

What's new?

- Auth: [Added support for single sign-on via OpenID Connect (OIDC)](https://github.com/photoprism/photoprism/issues/782)
- Index: [Slashes and null bytes are trimmed from `.ppignore` patterns](https://github.com/photoprism/photoprism/discussions/4349#discussioncomment-9848756)
- Videos: [Added support for MPEG-5 Essential Video Coding (EVC)](https://github.com/photoprism/photoprism/issues/4314)
- Videos: [Added filter to transcode 10bit videos with Intel QSV](https://github.com/photoprism/photoprism/issues/4380)
- Security: [Go has been updated to the latest stable release v1.22.5](https://github.com/golang/go/issues?q=milestone%3AGo1.22.5) 
- Translations: [Updated French and Japanese](https://docs.photoprism.app/developer-guide/translations-weblate/)

### May 31, 2024 ###
<span class="build">Build 240531-60b3a4628</span>

With this update, you can [choose to install FFmpeg 7](https://ffmpeg.org/index.html#pr7.0) for faster [software video transcoding](https://docs.photoprism.app/getting-started/advanced/transcoding/#software-transcoding). You also get the latest translations [contributed by our community](https://docs.photoprism.app/developer-guide/translations-weblate/) as well as improved [backup commands](https://docs.photoprism.app/user-guide/backups/) and [configuration defaults](https://docs.photoprism.app/getting-started/config-options/).

What's new?

- Videos: [You can choose to install FFmpeg 7.0 for faster transcoding](https://docs.photoprism.app/getting-started/advanced/transcoding/#software-transcoding)
- MariaDB: [Backup and restore commands support socket connections](https://github.com/photoprism/photoprism/issues/4306)
- Config: [Increased auto-index delay and disabled auto-import by default](https://github.com/photoprism/photoprism/issues/4310)
- Translations: [Updated Japanese](https://docs.photoprism.app/developer-guide/translations-weblate/)

### May 28, 2024 ###
<span class="build">Build 240528-977d6c0de</span>

This service release reduces the server load when [downloading many files](https://github.com/photoprism/photoprism/issues/4298), expands the list of [available config options](https://docs.photoprism.app/getting-started/config-options/), and gets you the latest translations [contributed by our community](https://docs.photoprism.app/developer-guide/translations-weblate/).

What's new?

- Download: [Zip archives are not compressed to reduce server load](https://github.com/photoprism/photoprism/issues/4298)
- Search: [Added `added`, `updated` and `edited` search filters for app developers](https://github.com/photoprism/photoprism/issues/4300)
- Config: [Replaced the terms whitelist and blacklist with alternatives](https://github.com/photoprism/photoprism/issues/3981)
- Config: [New feature flag `PHOTOPRISM_DISABLE_BACKUPS` disables all backups](https://github.com/photoprism/photoprism/issues/4294)
- Config: [New feature flag `PHOTOPRISM_DISABLE_VIPS` disables the use of libvips](https://github.com/photoprism/photoprism/issues/4296)
- Config: [Due to compatibility issues, libvips is disabled on 32-bit operating systems](https://github.com/photoprism/photoprism/issues/4299)
- Setup: [Improved .deb packages for installation on Ubuntu/Debian Linux](https://dl.photoprism.app/pkg/linux/README.html)
- Setup: [Improved AUR packages for installation on Arch Linux (Thomas Eizinger)](https://docs.photoprism.app/getting-started/faq/#arch-linux-packages)
- Translations: [Updated French and German](https://docs.photoprism.app/developer-guide/translations-weblate/)

### May 23, 2024 ###
<span class="build">Build 240523-923ee0cf7</span>

This update adds a scheduler so you can [easily create database backups](https://docs.photoprism.app/getting-started/config-options/#backup) and [re-index your library](https://docs.photoprism.app/getting-started/config-options/#indexing) at regular intervals. It also includes [many updated dependencies](https://github.com/photoprism/photoprism/issues/4084#issuecomment-2112733848) and [support for ICC color profiles](https://docs.photoprism.app/getting-started/config-options/#preview-images), which especially benefits Apple iPhone and professional users working with color spaces other than sRGB. 🎨

Important Changes

- If you keep the [default settings](https://docs.photoprism.app/getting-started/config-options/#backup), daily database backups will be automatically created, with up to 3 backup files being retained. This is to prevent the available storage space from filling up. We recommend [setting the corresponding config options](https://docs.photoprism.app/getting-started/config-options/#backup) before installing the update if you want to disable scheduled backups, keep more backup files, or prefer a specific time for creating backups. The previously available `--disable-backups` flag has been deprecated in favor of [these finer-grained options](https://docs.photoprism.app/getting-started/config-options/#backup).
- In order to preserve ICC color profiles and reduce memory usage, new thumbnails will be [generated with the `libvips` image processing library](https://github.com/photoprism/photoprism/issues/1474). You can run the `photoprism thumbs -f` [command in a terminal](https://docs.photoprism.app/getting-started/docker-compose/#command-line-interface) to regenerate your existing thumbs as needed, or delete the `storage/cache/thumbnails` folder and then re-index your library. To continue using the native image processing library, set `PHOTOPRISM_THUMB_LIBRARY` to `"imaging"` in your `compose.yaml` or `docker-compose.yml` [configuration file](https://docs.photoprism.app/getting-started/config-options/#preview-images). If you [build from source](https://docs.photoprism.app/getting-started/faq/#building-from-source) or use one of our [binary installation packages](https://dl.photoprism.app/pkg/linux/README.html), the system on which you build and/or run PhotoPrism must have `libvips` >= 8.10 installed.

What's new?

- Colors: [Added libvips support to preserve ICC profiles in thumbnails](https://github.com/photoprism/photoprism/issues/1474)
- Search: [Clicking on a timestamp finds pictures taken on the same day](https://github.com/photoprism/photoprism/issues/4273)
- Search: [Added a sort option to order search results by picture title](https://github.com/photoprism/photoprism/pull/4218)
- Review: [Photos are automatically approved when adding them to an album](https://github.com/photoprism/photoprism/issues/4229)
- People: [Faces tagged on private or archived pictures will be ignored](https://github.com/photoprism/photoprism/issues/4238)
- Index: [`*.thm` thumbnail files are not used as primary image anymore](https://github.com/photoprism/photoprism/issues/3900)
- Index: [Added a config option for scheduling automatic library rescans](https://github.com/photoprism/photoprism/issues/4251)
- Index: [Improved recovery of metadata from sidecar YAML files](https://github.com/photoprism/photoprism/issues/4286)
- Upload: [Improved ETA display when using the web upload dialog](https://github.com/photoprism/photoprism/issues/4285)
- Backups: [Added config options for creating backups at regular intervals](https://github.com/photoprism/photoprism/issues/4243)
- Moments: [Background worker no longer creates backups to avoid disk activity](https://github.com/photoprism/photoprism/issues/4237)
- Docker: [Upgraded base image from Ubuntu 23.10 to Ubuntu 24.04 LTS](https://github.com/photoprism/photoprism/issues/4084)
- Security: [Go has been updated to the latest stable release v1.22.3](https://github.com/golang/go/issues?q=milestone%3AGo1.22.3)
- Translations: [Updated Chinese (traditional), Danish, French, and German](https://docs.photoprism.app/developer-guide/translations-weblate/)

!!! info ""
    Missing user interface translations have been generated with the help of DeepL and Google Translate. Native speakers are [welcome to help us improve them](https://docs.photoprism.app/developer-guide/translations-weblate/), if necessary.

### April 20, 2024 ###
<span class="build">Build 240420-ef5f14bc4</span>

Our new stable release comes with a long list of indexing and security-related improvements. Most notably, we've added support for [2-Factor Authentication (2FA)](https://docs.photoprism.app/user-guide/users/2fa/) to protect your account in case someone gains access to your password. As all security-related changes had to be thoroughly tested, this is one of the updates that were longer in the making. We appreciate your patience while we've been working on this and would like to thank everyone involved! 🔐

What's new?

- Account: [Added support for 2-Factor Authentication (2FA)](https://github.com/photoprism/photoprism/issues/808)
- Account: [Added dialog to manage App Passwords from the UI](https://github.com/photoprism/photoprism/issues/4114)
- Places: [Updated reverse geocoding data and standard map tiles](https://github.com/photoprism/photoprism/issues/3849)
- Albums: [Fixed links to albums in the settings tab of the edit dialog](https://github.com/photoprism/photoprism/issues/4060)
- Photos: [Non-JPEG files like HEIC are no longer flagged as stacks in the UI](https://github.com/photoprism/photoprism/issues/3993)
- Videos: [Improved Intel QSV hardware transcoding support and performance](https://github.com/photoprism/photoprism/issues/4030)
- Videos: [Added support for Material Exchange Format (MXF) files](https://github.com/photoprism/photoprism/issues/3935)
- UI/UX: [Improved visibility of buttons and toggles in search results](https://github.com/photoprism/photoprism/issues/4174)
- Index: [A warning is shown for files with an invalid filename extension](https://github.com/photoprism/photoprism/issues/3518)
- Index: [Nested storage folders within the originals path are ignored](https://github.com/photoprism/photoprism/issues/1642)
- Import: [Modification times are preserved when moving or copying files](https://github.com/photoprism/photoprism/issues/4139)
- Metadata: [Media files with a matching `ContentIdentifier` can be stacked](https://github.com/photoprism/photoprism/issues/3960)
- Metadata: [File mod time instead of birth time is used as creation time fallback](https://github.com/photoprism/photoprism/issues/4157)
- Metadata: [Improved validation for focal length, f-number, and exposure values](https://github.com/photoprism/photoprism/issues/4170)
- Metadata: [Stop words are no longer ignored when generating titles from filenames](https://github.com/photoprism/photoprism/issues/4192)
- WebDAV: [File modification date is preserved if client submits an `X-OC-MTime` header](https://github.com/photoprism/photoprism/issues/3959)
- API: [Added support for OAuth2 Client Credentials and Access Tokens](https://github.com/photoprism/photoprism/issues/3943)
- API: [Added Prometheus-compatible metrics and monitoring endpoint](https://github.com/photoprism/photoprism/issues/213)
- CDN: [Improved Cross-Origin Resource Sharing (CORS) and cache headers](https://github.com/photoprism/photoprism/issues/3931)
- MariaDB: [Info log is shown when waiting for the database to become available](https://github.com/photoprism/photoprism/issues/4059)
- MariaDB: [Changed image name in Docker Compose config example for ARMv7](https://github.com/photoprism/photoprism/pull/4199)
- Docker: [Missing user accounts are automatically created by the entrypoint script](https://github.com/photoprism/photoprism/issues/4000)
- Setup: [Added ARMv7 `tar.gz` packages for installation without Docker](https://github.com/photoprism/photoprism/issues/4082)
- Performance: [Added index for `files.file_error` to reduce query time](https://github.com/photoprism/photoprism/issues/4149)
- Security: [Go has been updated to the latest stable release v1.22.2](https://github.com/golang/go/issues?q=milestone%3AGo1.22.2)

!!! info ""
    Missing user interface translations have been generated with the help of DeepL and Google Translate. Native speakers are [welcome to help us improve them](https://docs.photoprism.app/developer-guide/translations-weblate/), if necessary.
 
### November 28, 2023 ###
<span class="build">Build 231128-f48ff16ef</span>

Our latest service release provides updated dependencies and fixes for recently discovered issues. In addition, official [installation packages with binaries for Linux are now available](https://dl.photoprism.app/pkg/linux/README.html) as an alternative to [our Docker images](https://docs.photoprism.app/getting-started/docker-compose/). Please note that only experienced users should choose this installation method, since these [do not include all dependencies](https://dl.photoprism.app/pkg/linux/README.html#dependencies) and need to be set up manually.

What's new?

- Search: [Improved camera and lens information in the cards view details](https://github.com/photoprism/photoprism/issues/3816)
- Search: [Fixed cards view rendering when a lens has no model description](https://github.com/photoprism/photoprism/issues/3918)
- Search: [Added filter to find pictures by resolution range in Megapixels (MP)](https://github.com/photoprism/photoprism/issues/3896)
- PWA: [Fixed list of available icon sizes in the app manifest file](https://github.com/photoprism/photoprism/pull/3838)
- JPEG: [Fixed regression when handling image files with EOF error](https://github.com/photoprism/photoprism/issues/3855)
- JPEG: [Fixed indexing of image files with invalid color metadata](https://github.com/photoprism/photoprism/issues/3843)
- JPEG/PNG: [Added panic handler for unexpected thumbnail save errors](https://github.com/photoprism/photoprism/issues/3858)
- HEIC: [Libheif has been upgraded from version 1.13.0 to 1.17.1](https://github.com/photoprism/photoprism/issues/3852)
- RAW: [Darktable has been upgraded from version 4.2.1 to 4.4.2](https://github.com/photoprism/photoprism/issues/3741)
- Videos: [Improved performance when extracting still images for creating thumbnails](https://github.com/photoprism/photoprism/pull/3893)
- Vectors: [Improved SVG conversion using RSVG instead of ImageMagick](https://github.com/photoprism/photoprism/issues/3885)
- Docker: [Base image has been upgraded from Ubuntu 23.04 to 23.10 (Mantic Minotaur)](https://github.com/photoprism/photoprism/blob/develop/docker/develop/mantic/Dockerfile)
- Setup: [Added `tar.gz`, `deb` and `rpm` packages for installation without Docker](https://github.com/photoprism/photoprism/issues/3861)
- Security: [Go has been updated to the latest stable release v1.21.4](https://github.com/golang/go/issues?q=milestone%3AGo1.21.4)

### October 21, 2023 ###
<span class="build">Build 231021-9abea5b55</span>

This update adds search filters for finding pictures by ISO number, focal length, aperture, and altitude. It also includes a number of user interface improvements, updated translations, as well as fixes for recently discovered issues. We would like to thank everyone who [submitted pull requests](https://docs.photoprism.app/developer-guide/), [helped with testing](https://github.com/orgs/photoprism/projects/5), or [contributed in other ways](https://www.photoprism.app/oss/faq)! ✨

What's new?

- Search: [Added filters for ISO number, focal length, and aperture range](https://github.com/photoprism/photoprism/issues/3818)
- Search: [Added `alt:...` filter to find pictures by altitude range](https://github.com/photoprism/photoprism/pull/3800)
- Search: [Cards view shows ISO number, focal length, aperture, and exposure](https://github.com/photoprism/photoprism/issues/3816)
- Live Photos: [Fixed Google HEVC motion photo playback and transcoding](https://github.com/photoprism/photoprism/issues/3814)
- Live Photos: [Improved indexing of related files with vendor-specific naming schemes](https://github.com/photoprism/photoprism/issues/2983)
- Metadata: [Updated offline map data for more accurate timezone lookups](https://github.com/photoprism/go-tz)
- Metadata: [Creation time is calculated with UTC offset if timezone is unknown](https://github.com/photoprism/photoprism/discussions/3780)
- Config: [Creation of default certificate is skipped if HTTPS/TLS is disabled](https://github.com/photoprism/photoprism/issues/3823)
- Translations: [Updated German, Greek, and Romanian](https://translate.photoprism.app/projects/photoprism/)

### October 11, 2023 ###
<span class="build">Build 231011-63f708417</span>

This service release includes an [updated ARMv7 build](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&ordering=last_updated&name=armv7), a number of usability improvements requested by our community, and fixes for recently discovered issues. We would like to thank everyone involved!

What's new?

- PWA: [Fixed automatic screen orientation in Google Chrome on Android](https://github.com/photoprism/photoprism/issues/3413)
- Upload: [Current album is preselected when using the mobile nav menu](https://github.com/photoprism/photoprism/issues/3784)
- Videos: [Creation of thumbnails can only be disabled in experimental mode](https://github.com/photoprism/photoprism/issues/3793)
- Settings: [Ability to permanently delete files is now enabled by default](https://github.com/photoprism/photoprism/issues/3801)
- RAW/HEIC: [Original media information is shown in the cards view details](https://github.com/photoprism/photoprism/issues/2040)
- Live Photos: [Embedded video files can be streamed and transcoded](https://github.com/photoprism/photoprism/issues/3764)
- Metadata: [Improved camera make and model name normalization](https://github.com/photoprism/photoprism/discussions/3077)
- Docker: [An updated ARMv7 image is available on Docker Hub](https://hub.docker.com/r/photoprism/photoprism/tags?page=1&ordering=last_updated&name=armv7)
- Security: [Go has been updated to the latest stable release v1.21.3](https://github.com/golang/go/issues?q=milestone%3AGo1.21.3)

### September 23, 2023 ###
<span class="build">Build 230923-e59851350</span>

Our [latest release](getting-started/updates.md) includes a [redesigned Places view](https://user-images.githubusercontent.com/301686/269433540-cd48e79f-b2a8-4fb5-bc54-52467b15b743.jpg), with the search box moved to the top and a preview for selected clusters at the bottom. We've also added support for [Samsung](https://github.com/photoprism/photoprism/issues/439)/[Google Motion Photos](https://github.com/photoprism/photoprism/issues/1739), so you can view them like Apple Live Photos after [re-indexing your library](user-guide/library/originals.md). Beyond those highlights, you'll get many usability improvements, new search filters, and fixes for recently discovered issues. A big thank you to [everyone who contributed](https://github.com/photoprism/photoprism/graphs/contributors)!

What's new?

- UX: [Added a preview image to the Labels tab in the photo edit dialog](https://github.com/photoprism/photoprism/pull/3532)
- UX: [Reduced padding in mosaic view in favor of larger thumbnails](https://github.com/photoprism/photoprism/issues/3572)
- UX: [Edit dialog allows pasting latitude and longitude in a single operation](https://github.com/photoprism/photoprism/pull/3568)
- UX: [Reduced the number of info notifications in the user interface](https://github.com/photoprism/photoprism/issues/3608)
- UX: [Improved user interface styles, added new "Chrome" and "Mint" themes](https://github.com/photoprism/photoprism/commit/20df14e9d16b456a5edbc456544f875ee9da16a4)
- Search: [Added `scan:false` filter to find photos that are not scans](https://github.com/photoprism/photoprism/commit/be0fdc1774266bd4ec09e01ab93496fb07a4cbed)
- Search: [Added `favorite:false` filter to find pictures not marked as favorites](https://github.com/photoprism/photoprism/commit/20d20c7fa923baa9b5041631b3bcf6873bc2c874)
- Albums: [New share preview shows album contents as a stack of Polaroids](https://github.com/photoprism/photoprism/issues/3658#issuecomment-1711870557)
- Albums: [Fixed preview image URL when sharing album links](https://github.com/photoprism/photoprism/issues/3658)
- Albums: [Current album is preselected when opening the upload dialog](https://github.com/photoprism/photoprism/issues/3644)
- Albums: [Last edited timestamp is updated when pictures are added](https://github.com/photoprism/photoprism/issues/3080)
- People: [Fixed an error when reusing the name of a previously deleted person](https://github.com/photoprism/photoprism/issues/3414)
- Places: [Added cluster view to browse pictures close to each other in an overlay](https://github.com/photoprism/photoprism/issues/1187)
- Places: [Added support sub-km distances when searching for locations](https://github.com/photoprism/photoprism/issues/3558)
- Places: [Added support for the `label` and `category` search filters](https://github.com/photoprism/photoprism/commit/a865300666bfa26f8de47ac3fb19a31617f97056)
- Places: [Added map style selector and a scale for comparing distances](https://github.com/photoprism/photoprism/issues/2106)
- Archive: [Added "Delete All" button to permanently delete all archived files](https://github.com/photoprism/photoprism/issues/3701)
- Library: [Added option for admins to perform index and cache cleanup from the UI](https://github.com/photoprism/photoprism/issues/3699)
- Library: [Fixed escaping of hash characters in folder names](https://github.com/photoprism/photoprism/issues/3695)
- Live Photos: [Added support for Samsung Motion Photos](https://github.com/photoprism/photoprism/issues/439)
- Live Photos: [Added support for Google Camera Motion Photos](https://github.com/photoprism/photoprism/issues/1739)
- Live Photos: [Fixed indexing of sidecar video file properties](https://github.com/photoprism/photoprism/issues/3559)
- Videos: [Added support for AMD GPUs in `install-gpu.sh` script](https://github.com/photoprism/photoprism/pull/3710)
- Videos: [Removed deprecated FFmpeg `-vsync vfr` command flag](https://github.com/photoprism/photoprism/issues/3659#issuecomment-1707529050)
- Metadata: [Changed order of field names from which the title is extracted](https://github.com/photoprism/photoprism/commit/82dac4b7db65f1e490d3cd26a17b122832b0445f)
- Metadata: [Added support for reading fstop favorite flag from XMP sidecar files](https://github.com/photoprism/photoprism/pull/1873)
- Metadata: [Samsung/Google Motion Photos are flagged as Live Photos](https://github.com/photoprism/photoprism/issues/2788)
- Config: [Added support for serving HTTP requests over Unix sockets](https://github.com/photoprism/photoprism/issues/2337)
- Config: [A lower cache duration can be set for video content](https://github.com/photoprism/photoprism/issues/3631)
- SQLite: [Updates are performed in batches to limit the number of variables](https://github.com/photoprism/photoprism/issues/3742)
- Docker: [Added support for user ID ranges 1201-1250 and 2000-2100](https://github.com/photoprism/photoprism/issues/3719)
- Security: [Reduced bcrypt cost for faster login on small devices](https://github.com/photoprism/photoprism/issues/3718)
- Security: [Go has been updated to the latest stable release v1.21.1](https://github.com/golang/go/issues?q=milestone%3AGo1.21.1)
- Translations: [Updated Chinese (Simplified and Traditional)](https://translate.photoprism.app/projects/photoprism/)

### July 19, 2023 ###
<span class="build">Build 230719-73fa7bbe8</span>

Our latest release includes [new features and enhancements](https://github.com/photoprism/photoprism/pulls) contributed [by our community](https://docs.photoprism.app/developer-guide/pull-requests/), a number of security improvements, as well as fixes for recently discovered issues. Thank you to everyone who submitted pull requests, helped with testing, signed up as a member, or contributed in other ways! We appreciate it very much.

What's new?

- Setup: [Added a batch script for simplified installation under Windows](https://dl.photoprism.app/docker/windows/install.bat)
- Search: [Added `geo:false` filter to find pictures without GPS coordinates](https://github.com/photoprism/photoprism/issues/3493)
- Photos: [JPEG files with missing EOI marker are automatically repaired](https://github.com/photoprism/photoprism/pull/2721)
- Photos: [Fixed an error when opening panoramas taken with a Samsung S21](https://github.com/photoprism/photoprism/issues/3363)
- Videos: [Added a config option to limit the resolution of transcoded videos](https://github.com/photoprism/photoprism/issues/3466)
- Videos: [Fixed container and codec checks in `photoprism convert` command](https://github.com/photoprism/photoprism/issues/3525)
- Metadata: [Dates in WhatsApp generated file names can be parsed](https://github.com/photoprism/photoprism/issues/1102)
- Metadata: [Year 0000 is mapped to 0001 when parsing dates from Exiftool](https://github.com/photoprism/photoprism/pull/2508)
- Security: [Default to a self-signed HTTPS/TLS certificate if no other certificate is available](https://github.com/photoprism/photoprism/issues/3509)
- Security: [Clipboard contents are cleared on logout and when user privileges change](https://github.com/photoprism/photoprism/issues/3512)
- Security: [Go has been updated to v1.20.6, which includes bug fixes and enhancements](https://github.com/golang/go/issues?q=milestone%3AGo1.20.6)
- Translations: [Updated Japanese](https://translate.photoprism.app/projects/photoprism/)

!!! info ""
    We recommend that you [explicitly disable TLS](https://docs.photoprism.app/getting-started/config-options/#web-server) by adding `PHOTOPRISM_DISABLE_TLS: "true"` to your `docker-compose.yml` file when running PhotoPrism behind a reverse proxy. HTTPS could otherwise be accidentally enabled if a certificate matching the site URL is found or [`PHOTOPRISM_DEFAULT_TLS` is set to `"true"`](https://docs.photoprism.app/getting-started/config-options/#web-server). 

### June 25, 2023 ###
<span class="build">Build 230625-17242fb07</span>

This service release includes the [latest translations contributed by our community](https://translate.photoprism.app/projects/photoprism/), as well as fixes for recently discovered issues.

What's new?

- Albums: [Invalid entries are automatically hidden and flagged as missing](https://github.com/photoprism/photoprism/issues/3481)
- CLI: [Fixed an issue where entering a very long password could disable the login](https://github.com/photoprism/photoprism/issues/3482)
- Security: [Updated third-party dependencies in backend](https://github.com/photoprism/photoprism/commit/96e0981c3179a428ea4c5614ee3ffec417232d52) [and frontend](https://github.com/photoprism/photoprism/commit/ee6e6c66e388ddb901e212dc6736f5dbfa28c459)
- Translations: [Updated Chinese (Simplified), Italian, and Japanese](https://translate.photoprism.app/projects/photoprism/)

### June 15, 2023 ###
<span class="build">Build 230615-90a18f6e7</span>

This update includes [new features and enhancements](https://github.com/photoprism/photoprism/pulls?q=is%3Apr+is%3Aclosed+label%3Amerged+sort%3Aupdated-desc) contributed [by our community](https://docs.photoprism.app/developer-guide/pull-requests/),
as well as fixes for recently discovered issues. We would like to thank everyone involved!

What's new?

- Photos: [Related albums are displayed in the Info tab of the edit dialog](https://github.com/photoprism/photoprism/pull/3095)
- Photos: [Added a link from the Files tab to the related folder in the file browser](https://github.com/photoprism/photoprism/pull/2926)
- Moments: [Added labels to match *Holidays* as well as additional *Pets*](https://github.com/photoprism/photoprism/pull/3081)
- CLI: [Added `photoprism find` command to search the index for specific files](https://github.com/photoprism/photoprism/pull/3222)
- CLI: [Fixed the `photoprism import` command destination parameter type](https://github.com/photoprism/photoprism/issues/3473)
- PikaPods: [Fixed an issue that caused newly deployed instances to require a restart](https://www.reddit.com/r/photoprism/comments/13z9x5r/comment/jmqp8t0/)
- Security: [Updated third-party dependencies in backend](https://github.com/photoprism/photoprism/commit/b91723e90caf3012cf55a4d2b2f68dda81c9f702) [and frontend](https://github.com/photoprism/photoprism/commit/9a5af3176e937a494d69f96e99d9191e0f1b5ee2)

### June 7, 2023 ###
<span class="build">Build 230607-9e086c7eb</span>

With this much anticipated update, our new high-resolution vector world map becomes available to all users. It also features a special terrain mode for mountain lovers, so you can view the "Satellite", "Outdoor" and "Topography" maps in 3D!

What's new?

- Places: [Improved the level of detail of the freely available default world map](https://github.com/photoprism/photoprism/issues/2998#issuecomment-1575607476)
- Places: [Added terrain mode to display the satellite, outdoor and topography maps in 3D](https://github.com/photoprism/photoprism/issues/3455)
- Security: [Go has been updated to v1.20.5, which includes bug fixes and enhancements](https://github.com/golang/go/issues?q=milestone%3AGo1.20.5)
- Translations: [Updated Chinese (Simplified), Italian, and Slovak](https://translate.photoprism.app/projects/photoprism/)

PhotoPrism® Plus

- Config: [CSP header is updated automatically when a CDN is configured](https://github.com/photoprism/photoprism/issues/3454)

### June 3, 2023 ###
<span class="build">Build 230603-378d4746a</span>

This service release fixes recently discovered issues and improves compatibility with the upcoming [MariaDB v11.0](https://mariadb.com/kb/en/release-notes-mariadb-11-0-series/). If you are upgrading from MariaDB 10.x to 11.0, please [make sure that you replace](https://github.com/photoprism/photoprism/commit/bff649469d084498a1e75492c0bd99bda3f5a340#diff-03a31d6e73f48b7bba98b65352ce67a7d153fe2461f9c7b5e76be49a97ebf0cb) `command: mysqld` with `command: ` (followed by the command flags) in your `docker-compose.yml` file, otherwise the database server might fail to start. Thank you to everyone who contributed with pull requests, [reported bugs](https://www.photoprism.app/kb/reporting-bugs), and helped us test the changes!

What's new?

- Folders: [Searching for substrings now returns all matching albums](https://github.com/photoprism/photoprism/issues/3441)
- Search: [Fixed an issue where the "Unknown country" filter has been ignored](https://github.com/photoprism/photoprism/issues/3412)
- Navigation: [Fixed account feature check when clicking on the profile picture](https://github.com/photoprism/photoprism/pull/3365)
- Config: [Fixed setting the title of the search page based on the site title](https://github.com/photoprism/photoprism/issues/3439)
- MariaDB: [Improved compatibility with the upcoming release 11.0](https://github.com/photoprism/photoprism/issues/3443)
- Security: [Updated third-party dependencies in backend and frontend](https://github.com/photoprism/photoprism/commit/0ff2fee91d791f203a3c64bc0409746cd8a62a47)
- Security: [Go has been updated to v1.20.4, which includes bug fixes and enhancements](https://github.com/golang/go/issues?q=milestone%3AGo1.20.4)
- Translations: [Updated Chinese (Traditional), Dutch, German, and French](https://translate.photoprism.app/projects/photoprism/)

PhotoPrism® Plus

- Security: [Malicious client requests can be automatically detected and blocked](https://docs.photoprism.app/getting-started/config-options/#web-server)

### May 13, 2023 ###
<span class="build">Build 230513-0b780defb</span>

As [promised](https://twitter.com/photoprism_app/status/1632036907419877377), this update makes hardware transcoding and many other config options available to all users. [A big thank you to all of our contributors, members, and sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md), whose generous support has been and continues to be essential to the success of the project! :octicons-heart-fill-24:{ .heart .purple }

What's new?

- Config: [Additional options are now available to all users](https://github.com/photoprism/photoprism/commit/0e415fec1ce173b185bc8b2efcb63a83022b5ef2)

### May 6, 2023 ###
<span class="build">Build 230506-9de9a3540</span>

This update resolves two recently reported issues and includes updated translations.

What's new?

- Sharing: [Upload checks if files have been deleted](https://github.com/photoprism/photoprism/issues/3379)
- CLI: [Logging output is reduced in production mode](https://github.com/photoprism/photoprism/issues/3370)
- Translations: [Updated French](https://github.com/photoprism/photoprism/pull/3373)

### May 4, 2023 ###
<span class="build">Build 230504-cbf48798c</span>

This service release makes the Nordic theme and the [Hide People](user-guide/organize/people.md#hiding-people) feature available to all users. It also changes the theme order in [Settings](user-guide/settings/general.md) so that the freely available themes come first.

What's new?

- Settings: [Changed order in the theme dropdown so the freely available themes come first](https://github.com/photoprism/photoprism/issues/3368)

### May 2, 2023 ###
<span class="build">Build 230502-c405f6eff</span>

With this major new release, you'll get a long list of new features and enhancements with a focus on [performance](https://twitter.com/photoprism_app/status/1628850699772600323), [security](https://twitter.com/photoprism_app/status/1651596098249662465), and [file type support](https://www.photoprism.app/kb/file-formats). In addition, our [Plus Members](https://www.photoprism.app/editions#compare) can now register [directly in the app](https://www.photoprism.app/kb/activation) to unlock additional features like [vector graphics support](https://demo.photoprism.app/library/browse?view=cards&order=added&q=vectors) and a new [admin web UI](https://demo.photoprism.app/library/admin/users) for [user and session management](https://www.photoprism.app/plus/kb/multi-user). Thank you to all [contributors](https://github.com/photoprism/photoprism/graphs/contributors), [members](https://www.photoprism.app/membership), and [sponsors](https://github.com/photoprism/photoprism/blob/develop/SPONSORS.md) who made this possible!

What's new?

- UX: [Improved user interface layout for right-to-left languages](https://github.com/photoprism/photoprism/commit/3a1293d5d42ba8d0cf6f4efa1540a9db7f3681d9)
- UX: [Improved highlight and background colors in the cards view](https://github.com/photoprism/photoprism/commit/c243d45c118a6691c626397a9f81f08385ee6a60)
- UX: [Improved theme styles and search field contrast in Places](https://github.com/photoprism/photoprism/commit/0d2a25eb0cd12e114dff87570e4015b6eba8c73c)
- UX: [Navigation shows the total number of pictures without those under review](https://github.com/photoprism/photoprism/issues/3164)
- UX: [Enabled long-touch menu in photo viewer on iOS Safari](https://github.com/photoprism/photoprism/issues/1233)
- PWA: [Increased allowed length of app name on home screen](https://github.com/photoprism/photoprism/commit/5dc71ff1ff69c157568c11d08b941b1d1875dc38)
- PWA: [Improved manifest.json for more reliable installation prompts](https://github.com/photoprism/photoprism/issues/3181)
- Themes: [Added "Carbon", "Neon"](https://github.com/photoprism/photoprism/commit/93251d77a02a7de1ced8e28caf3deb2220a442c4), [and "Nordic"](https://github.com/photoprism/photoprism/commit/53cddf5a4365614024670bb455de41e2b45da2b0) based on [colors from nordtheme.com](https://www.nordtheme.com/)
- Themes: [Removed "Electra", "Moonlight", "Seaweed"](https://github.com/photoprism/photoprism/commit/e1405eba5430d30769d90292bdc69debe0e27092), [and "Cyano"](https://github.com/photoprism/photoprism/commit/53cddf5a4365614024670bb455de41e2b45da2b0)
- People: [Ambiguous faces are skipped when matching to improve performance](https://github.com/photoprism/photoprism/issues/3124)
- People: [Entering names is faster with many faces tagged](https://github.com/photoprism/photoprism/issues/3151)
- Search: [Added `id:...` filter to find pictures by Exif UID, XMP Document ID or Instance ID](https://github.com/photoprism/photoprism/issues/3035)
- Search: [Increased batch size for better performance when loading results](https://github.com/photoprism/photoprism/ssues/3009)
- Search: [Deleted albums are ignored when using the `unsorted` filter](https://github.com/photoprism/photoprism/issues/3051)
- Search: [Sepia colored pictures are excluded when using the `mono` filter](https://github.com/photoprism/photoprism/issues/2657)
- Photos: [Image orientation can be changed through the user interface](https://github.com/photoprism/photoprism/issues/464)
- RAW: [Upgraded RawTherapee from v5.8 to v.5.9 to fix ProRAW support](https://github.com/photoprism/photoprism/issues/2291)
- Videos: [Improved player compatibility with browser plugins](https://github.com/photoprism/photoprism/issues/1439)
- Videos: [Improved preview image generation depending on duration](https://github.com/photoprism/photoprism/issues/1241#issuecomment-1363473310)
- Videos: [Playback durations of less than one second can be indexed and displayed](https://github.com/photoprism/photoprism/issues/3224)
- Videos: [Added .dv to the list of known video file types](https://github.com/photoprism/photoprism/issues/3226)
- Videos: [Specific video and audio streams can be selected for transcoding](https://github.com/photoprism/photoprism/issues/3284)
- Videos: [Improved detection of HEVC support for Google Chrome](https://github.com/photoprism/photoprism/issues/3275)
- Albums: [Added extended search form with sorting options](https://github.com/photoprism/photoprism/issues/353)
- Albums: [Fixed form field styles in the share dialog](https://github.com/photoprism/photoprism/commit/7c671e0dfc52936b1a3af426db1e0f5e165a12f7)
- Albums: [Double quotes in album names are replaced by Unicode characters](https://github.com/photoprism/photoprism/issues/2891)
- Albums: [Improved error handling and validation of query parameters](https://github.com/photoprism/photoprism/issues/3320)
- Albums: ["Download as zip" button is displayed on mobile screens](https://github.com/photoprism/photoprism/issues/3340)
- Moments: [Changed default sort order in the overview to "newest"](https://github.com/photoprism/photoprism/issues/3280)
- Folders: [Search is case-insensitive and uses wildcards for improved usability](https://github.com/photoprism/photoprism/issues/2050)
- Metadata: [GPS coordinates are normalized to be within a common range](https://github.com/photoprism/photoprism/issues/2109)
- Metadata: [Out-of-range altitude values are ignored to prevent indexing errors](https://github.com/photoprism/photoprism/issues/3182)
- Metadata: [Date defaults caused by software or camera bugs are ignored](https://github.com/photoprism/photoprism/issues/3229)
- Metadata: [Software name is displayed on the Files tab, if available](https://github.com/photoprism/photoprism/commit/3c1b7acf1191c48620e3bdc8256694b7513856c9)
- Metadata: [Valid year range in Exif data and filenames has been extended from 1990 to 1970](https://github.com/photoprism/photoprism/issues/3220)
- Metadata: [Scanned images are automatically recognized by device name](https://github.com/photoprism/photoprism/issues/3221)
- Metadata: [Added TakenAtLocal to YAML backups to prevent incorrectly restored times](https://github.com/photoprism/photoprism/issues/3338)
- Metadata: [Notes can be extracted from the Comment and UserComment fields](https://github.com/photoprism/photoprism/issues/3352)
- Index: [Improved performance by skipping updates when there are no changes](https://github.com/photoprism/photoprism/issues/3227)
- Index: [Improved performance when flagging hidden files](https://github.com/photoprism/photoprism/issues/2928)
- Index: [Added file format support for Adobe Photoshop PSD images](https://github.com/photoprism/photoprism/issues/2207)
- Index: [Added support for decoding JPEG XL and playing PNG animations](https://github.com/photoprism/photoprism/issues/3197)
- Index: [Corrupted JPEG images are automatically repaired if necessary](https://github.com/photoprism/photoprism/issues/2463)
- Index: [TIFF images with unsupported file format features can be converted](https://github.com/photoprism/photoprism/issues/1612)
- Upload: [Estimated time remaining is displayed in minutes and seconds](https://github.com/photoprism/photoprism/issues/3049)
- Download: [Added settings to choose which files to download by default](https://github.com/photoprism/photoprism/issues/449)
- Backups: [Improved backup and restore commands to better handle large index dumps](https://github.com/photoprism/photoprism/issues/3140)
- WebDAV: [Enabled access to the originals and import folders in read-only mode](https://github.com/photoprism/photoprism/issues/3183)
- WebDAV: [Replaced client library to prevent incomplete uploads to other servers](https://github.com/photoprism/photoprism/issues/3310)
- WebDAV: [Download sync is prevented when read-only mode is enabled](https://github.com/photoprism/photoprism/commit/d48db6cae4b25e8ff3daf867db42e106ea4c2297)
- API: [Search results can be sorted randomly to get a random set of pictures](https://github.com/photoprism/photoprism/issues/153#issuecomment-1408480166)
- API: [HEAD requests are now supported for frontend bootstrap paths](https://github.com/photoprism/photoprism/issues/2965)
- CLI: [Added file extension flag to the `photoprism convert` command](https://github.com/photoprism/photoprism/issues/3038)
- CLI: [Commands create thumbnails and convert files in deterministic order](https://github.com/photoprism/photoprism/issues/3194)
- Config: [Migrations are skipped if the same version has already been initialized](https://github.com/photoprism/photoprism/issues/3215)
- Config: [Use dynamic social preview image based on app name](https://github.com/photoprism/photoprism/issues/3160)
- Config: [Custom template path is not searched for files if not specified](https://github.com/photoprism/photoprism/issues/2946)
- Config: [Advanced settings include additional options for PNGs and vector graphics](https://github.com/photoprism/photoprism/issues/2207#issuecomment-1436041896)
- Config: [Added advanced HTTP cache control options](https://github.com/photoprism/photoprism/issues/3297)
- Config: [Added option to stream videos over a Content Delivery Network (CDN)](https://github.com/photoprism/photoprism/issues/2875)
- Docker: [Ubuntu base image has been upgraded from v22.04 to v23.04](https://github.com/photoprism/photoprism/issues/3305)
- Docker: [MariaDB image and binaries have been upgraded from v10.9 to v10.11](https://github.com/photoprism/photoprism/issues/3332)
- Podman: [Added config examples for users of Red Hat-based Linux distributions](https://github.com/photoprism/photoprism/tree/develop/setup/podman)
- Security: [Improved bcrypt password support with explicit 72-character limit](https://github.com/photoprism/photoprism/issues/1987#issuecomment-1507190623)
- Security: [Go has been updated to v1.20.3, which includes bug fixes and other improvements](https://github.com/golang/go/issues?q=milestone%3AGo1.20.3)
- Translations: [Added Afrikaans (South Africa)](https://github.com/photoprism/photoprism/pull/3031/files) and [Basque](https://github.com/photoprism/photoprism/pull/3323/files) (Euskara)
- Translations: Updated Arabic, Bulgarian, Chinese, Czech, Dutch, Estonian, French, German, Italian, Malay, Russian, Ukrainian and many others

PhotoPrism® Plus

- Auth: [Admins can manage user accounts and active sessions through the web UI](https://demo.photoprism.plus/library/admin/users) 
- Index: [Added file format support for SVG, AI, PS and EPS vector graphics](https://github.com/photoprism/photoprism/issues/2207)

!!! info ""
    Our new [Plus License](https://www.photoprism.app/plus/license) is used for both the extensions [we provide to our members](https://www.photoprism.app/membership/faq#how-can-i-install-photoprism-plus-without-the-docker-image) and the standard [Docker images](https://hub.docker.com/r/photoprism/photoprism/tags) available on Docker Hub. This allows us to bundle the extensions with the compiled application, while the [Community Edition](https://github.com/photoprism/photoprism) remains freely available under the terms of the [GNU Affero General Public License (AGPL)](license/agpl.md).

    If you don't plan to use [any additional features](https://www.photoprism.app/editions#compare), you can alternatively use the "ce" tag instead of "latest" to get a slightly smaller Docker image distributed under the AGPL. Note that system dependencies and other third-party components included in this image are still subject to additional terms and conditions.
    
    [View Membership FAQ ›](https://www.photoprism.app/membership/faq){ class="pr-3 block-xs" } [View Plus License ›](https://www.photoprism.app/plus/license)

### November 18, 2022 ###
<span class="build">Build 221118-e58fee0fb</span>

This service release includes compatibility fixes for MariaDB 10.10, the [latest translations](https://translate.photoprism.app/projects/photoprism/), a new theme, and updated dependencies.
We recommend not using the `:latest` tag for the MariaDB Docker image and to [upgrade manually](getting-started/updates.md#mariadb-server) by changing the tag once we had a chance to test a new major version.

What's new?

- UI: [Added "Electra" theme](https://github.com/photoprism/photoprism/issues/2916)
- MariaDB: [Compatibility fixes for version 10.10](https://github.com/photoprism/photoprism/issues/2913)
- Translations: [Updated Czech and Estonian](https://github.com/photoprism/photoprism/pull/2911/files)

### November 17, 2022 ###
<span class="build">Build 221117-3268c4de8</span>

This update includes [video transcoding](https://docs.photoprism.app/getting-started/advanced/transcoding/) improvements and the latest [translations contributed by our community](https://translate.photoprism.app/projects/photoprism/).

What's new?

- Videos: [Fixed installation of Intel Quick Sync drivers for hardware transcoding](https://github.com/photoprism/photoprism/issues/2700)
- Videos: [Added `.m2ts` to known file extensions](https://github.com/photoprism/photoprism/issues/2899)
- Translations: [Updated Chinese (Traditional)](https://github.com/photoprism/photoprism/pull/2903/files) and [Estonian](https://github.com/photoprism/photoprism/pull/2906/files)

### November 16, 2022 ###
<span class="build">Build 221116-122ebfb70</span>

With this update you get the [latest translations](https://translate.photoprism.app/projects/photoprism/), updated dependencies, and two metadata bug fixes. Thanks to [all who contributed](https://github.com/photoprism/photoprism/graphs/contributors)!

What's new?

- Metadata: [Bad Unicode strings are sanitized automatically](https://github.com/photoprism/photoprism/issues/2897) 
- Metadata: [UTC can be overridden by local time with unknown zone](https://github.com/photoprism/photoprism/issues/2876)
- MariaDB: [Unsupported versions are allowed in "unsafe" mode](https://github.com/photoprism/photoprism/issues/2878)
- Translations: [Added Estonian](https://github.com/photoprism/photoprism/pull/2879)
- Translations: [Updated Polish](https://github.com/photoprism/photoprism/commit/196fc8b2077267a8fd6fddc66c091a53617dbfa4), [Italian](https://github.com/photoprism/photoprism/pull/2886/files), [Korean, Romanian](https://github.com/photoprism/photoprism/pull/2884/files), and [Chinese (Traditional)](https://github.com/photoprism/photoprism/pull/2890)

### November 5, 2022 ###
<span class="build">Build 221105-7a295cab4</span>

This service release provides UX improvements for the photo editing dialog and includes the latest [translations contributed by our community](https://translate.photoprism.app/projects/photoprism/). Note that [our guides now use the new `docker compose` command](https://docs.photoprism.app/getting-started/docker-compose/#step-2-start-the-server) by default. If your server does not yet support it, you can still use `docker-compose` to start and stop your instance.

What's new?

- UX: [Improved layout of form fields in photo edit dialog](https://github.com/photoprism/photoprism/commit/7a295cab4931d15d685e272b9363c734cfe78c0f)
- Account: [Disabled "gender" dropdown when busy or in demo mode](https://github.com/photoprism/photoprism/commit/08a7ab2b78885e698e9cc026ac66d818769d6705)
- Docker: [Changed "docker-compose" command to "docker compose"](https://github.com/photoprism/photoprism/pull/1192)
- Translations: [Updated Estonian, Hungarian, and Russian](https://github.com/photoprism/photoprism/commit/95c0ff6c7f908a90b927939e96c2475f8087cd5f#diff-1669a8e9dc01e9e39ed09a83475354fdc8ed4617fa36f9904c7272991ee35ed2)

### November 4, 2022 ###
<span class="build">Build 221104-20d180b21</span>

A small update featuring [improved NVIDIA GPU support](https://docs.photoprism.app/getting-started/advanced/transcoding/#nvidia-container-toolkit), the latest [translations contributed by our community](https://translate.photoprism.app/projects/photoprism/), and updated dependencies.

What's new?

- NVIDIA: [Added a ready-to-use `docker-compose.yml` config example](https://dl.photoprism.app/docker/nvidia/docker-compose.yml)
- NVIDIA: [Updated FFmpeg parameters for hardware video transcoding](https://github.com/photoprism/photoprism/issues/2613#issuecomment-1288293791)
- NVIDIA: [Updated install-gpu.sh script](https://github.com/photoprism/photoprism/commit/6d865152df0736ce2e3f826684015d982d2882c6) and [related documentation](https://docs.photoprism.app/getting-started/advanced/transcoding/#nvidia-container-toolkit)
- Translations: [Updated Chinese](https://github.com/photoprism/photoprism/commit/ddc1da8a30463932fc3792698827c01f270b1035)

### November 3, 2022 ###
<span class="build">Build 221103-211eb36ea</span>

With this update you'll get the latest [translations contributed by our community](https://translate.photoprism.app/projects/photoprism/), updated dependencies as well as a few minor bug fixes and improvements.

What's new?

- Index: [Paths starting with `_.` and `__` like `__MACOSX` are ignored](https://github.com/photoprism/photoprism/issues/2844)
- Config: [Updated new trusted proxy header options and command help](https://github.com/photoprism/photoprism/commit/c29bc5a8d4c9ef49e7c265fca1338515d0008d64)
- MariaDB: [Improved server version check on startup](https://github.com/photoprism/photoprism/issues/2845)
- Security: [Go has been updated to v1.19.3, which includes security fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.19.3)
- Translations: [Updated Chinese, French, Norwegian Bokmål, and Romanian](https://github.com/photoprism/photoprism/commit/46d6c3200b50d0afb2536e8042733582d2a097c3)

### November 2, 2022 ###
<span class="build">Build 221102-905925b4d</span>

Due to the many new features, enhancements and bug fixes, this is one of those updates that took longer to release.
Before upgrading, please read the full release notes and note that this release does not yet include support for user roles other than *Admin*, as we need to specify, create and test each new role before we can release it. Once this is done, we will also provide additional user management documentation.

!!! example ""
    We've generated missing translations with the help of DeepL and Google Translate. Native speakers are
    invited to [help us improve those if needed](developer-guide/translations-weblate.md).
    A special thank you to [everyone who contributed](https://docs.photoprism.app/developer-guide/)!

Breaking Changes

- In order to improve security and compatibility, the default Docker image is now based on Ubuntu 22.04 LTS (Jammy Jellyfish) instead of Debian 12 (Bookworm). The entrypoint script has been updated to [preserve group permissions required for hardware transcoding](https://github.com/photoprism/photoprism/issues/2739).
- Session and user management have been re-implemented. **If you are upgrading from a preview build, you will need to run the `photoprism users reset --yes` [command in a terminal](getting-started/docker-compose.md#command-line-interface) after the upgrade to recreate the new database tables so that they are compatible with the stable version. This will not affect your pictures or albums.**
- Upgrading from the last stable version should work without any problems. However, if you have already created additional accounts with the previously offered unofficial multi-user support, you will notice that only the main admin account is migrated automatically. Run `photoprism users legacy` [in a terminal](getting-started/docker-compose.md#command-line-interface) to display the legacy accounts so you can migrate them manually if needed.
- Sharing link visitors can now see the picture locations in the regular album view and optionally on a map after clicking the link. Based on user feedback, we may add settings to hide the locations for enhanced privacy.
- We recommend performing a full rescan after the upgrade to take advantage of new search filters and sort options.
- Indexing is also necessary to find and view HEIC, DNG, and AVIF images that were previously unsupported or had errors. In some cases with incorrectly converted images, it may be necessary to recreate the JPEG sidecar files by running the `photoprism convert -f` command [in a terminal](getting-started/docker-compose.md#command-line-interface) before starting the rescan. To regenerate your thumbnails, run `photoprism thumbs -f`.

What's new?

- Auth: [Session and user management have been re-implemented](https://github.com/photoprism/photoprism/issues/98)
- Auth: [API has been improved to prevent unnecessary re-logins](https://github.com/photoprism/photoprism/pull/1746)
- Auth: [User interface routes have been prefixed with `/library`](https://github.com/photoprism/photoprism/issues/840)
- UX: [Scroll position is restored again when navigating back](https://github.com/photoprism/photoprism/pull/2782)
- UX: [Loading screen and mobile toolbar menu have been redesigned](https://github.com/photoprism/photoprism/issues/2409)
- UX: [Improved user interface styles for RTL languages](https://github.com/photoprism/photoprism/pull/2732)
- Search: [Added `city:...` and `state:...` to filter by location details](https://github.com/photoprism/photoprism/pull/2670)
- Search: [Results can now also be sorted by "File Size" and "Video Duration"](https://github.com/photoprism/photoprism/issues/2620)
- Albums: [Added breadcrumbs to navigate back on large screens](https://github.com/photoprism/photoprism/issues/1409)
- Albums: [Deselected labels are ignored when adding photos by label](https://github.com/photoprism/photoprism/issues/2821)
- HEIC: [Added support for Sony's `.HIF` file extension](https://github.com/photoprism/photoprism/pull/2693)
- HEIC: [Updated `heif-convert` tool to fix conversion problems](https://github.com/photoprism/photoprism/issues/2726)
- AVIF: [Added support for the AV1 Image File Format](https://github.com/photoprism/photoprism/issues/2706)
- RAW: [Updated Darktable from v3.8.1 to v4.0.1 (AMD64 only)](https://github.com/photoprism/photoprism/issues/2703)
- ProRAW: [JPEGs embedded in `.DNG` files can be searched and viewed](https://github.com/photoprism/photoprism/issues/2291#issuecomment-1271704046)
- Videos: [Added VAAPI hardware AVC encoder support](https://github.com/photoprism/photoprism/pull/2709)
- Index: [Delayed RAW file format check to improve indexing performance](https://github.com/photoprism/photoprism/pull/2683)
- Import: [Selection of a source folder with dots in its name is now possible](https://github.com/photoprism/photoprism/issues/2807)
- Import: [Related original names are indexed in addition to the main filename](https://github.com/photoprism/photoprism/pull/2623)
- Settings: [Services cannot be managed in public mode to increase security](https://github.com/photoprism/photoprism/discussions/2468#discussioncomment-3678435)
- Backups: [Worker no longer recreates all album YAML files on every run](https://github.com/photoprism/photoprism/issues/2705)
- Metadata: [Added more place names with known countries](https://github.com/photoprism/photoprism/pull/2720)
- Metadata: [Default to UTC when reading time from XMP file](https://github.com/photoprism/photoprism/issues/636#issuecomment-1241686328)
- Config: [Increased default resolution limit from 100 to 150 MP](https://github.com/photoprism/photoprism/discussions/2677)
- Config: [`imprint` info text option has been renamed to `legal-info`](https://github.com/photoprism/photoprism/issues/2797)
- SQLite: [Added busy timeout preset to reduce locking errors when indexing](https://github.com/photoprism/photoprism/issues/2707)
- MariaDB: [Startup fails with an error message if an unsupported version is used](https://github.com/photoprism/photoprism/issues/2381)
- Docker: [Default image is based on Ubuntu 22.04 LTS (Jammy Jellyfish)](https://github.com/photoprism/photoprism/issues/2178)
- Docker: [Switched from `gosu` to `setpriv` in entrypoint.sh script](https://github.com/photoprism/photoprism/pull/2730)
- Security: [New files are created without execution permission](https://github.com/photoprism/photoprism/issues/2809)
- Security: [Go has been updated to v1.19.2, which includes security fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.19.2)
- Translations: Added [Persian](https://github.com/photoprism/photoprism/pull/2767)
- Translations: Updated [Chinese](https://github.com/photoprism/photoprism/commit/6d435cab9e23c9c64fe418dafb26e0ac41970175), [Dutch](https://github.com/photoprism/photoprism/pull/2841), [Finnish](https://github.com/photoprism/photoprism/pull/2712/files), [French](https://github.com/photoprism/photoprism/pull/2830), [German](https://github.com/photoprism/photoprism/pull/2825), [Spanish](https://github.com/photoprism/photoprism/pull/2835/files), and many more

### September 1, 2022 ###
<span class="build">Build 220901-f493607b0</span>

With this update you get all the [latest translations contributed by our community](https://translate.photoprism.app/projects/photoprism/), [mobile navigation enhancements](https://dl.photoprism.app/img/ui/mobile-toolbar-navigation-open.jpg), updated dependencies and, as usual, fixes for recently discovered issues. Thanks to everyone involved!

What's new?

- UX: [Mobile toolbar menu has been redesigned and expanded](https://github.com/photoprism/photoprism/commit/ecadf17d506e2a4cfa9fb1bb33e942f1a6499c25)
- UX: [Improved search result and *Gemstone* theme styles](https://github.com/photoprism/photoprism/commit/3612ea016dd3b20af352009e92258f55d47a550b)
- Search: [Known file extensions are stripped from `name:...` filter string](https://github.com/photoprism/photoprism/issues/2667)
- Library: [Indexing will be aborted if the originals folder is empty](https://github.com/photoprism/photoprism/pull/2299)
- Videos: [Local time is extracted from `DateTimeOriginal` if possible](https://github.com/photoprism/photoprism/issues/2640)
- Albums: [All pictures are shown if "Private" has been disabled in *Settings*](https://github.com/photoprism/photoprism/issues/2570)
- Thumbs: [`photoprism thumbs` command regenerates thumbnails of sidecar files](https://github.com/photoprism/photoprism/issues/2669)
- Docker: [Permissions of original media files are no longer updated on startup](https://github.com/photoprism/photoprism/pull/2371)
- Build: [Go has been updated to v1.19, which includes fixes and enhancements](https://tip.golang.org/doc/go1.19)
- Build: [NodeJS has been updated from v16 to v18](https://nodejs.org/en/blog/announcements/v18-release-announce/)
- Translations: [Added Catalan, Finnish, Ukrainian](https://github.com/photoprism/photoprism/pull/2574), [and Slovene](https://github.com/photoprism/photoprism/pull/2636)

### July 30, 2022 ###
<span class="build">Build 220730-0e1222c83</span>

Fixes the activation of public mode with `PHOTOPRISM_AUTH_MODE` instead of `PHOTOPRISM_PUBLIC`.

What's new?

- Auth: [Activate public mode via `PHOTOPRISM_AUTH_MODE="public"`](https://github.com/photoprism/photoprism/issues/2565)

### July 28, 2022 ###
<span class="build">Build 220728-729ddd920</span>

Includes indexing, metadata, and authentication enhancements, as well as [updated translations](https://translate.photoprism.app/projects/photoprism/).

What's new?

- Library: [Added support for indexing and importing symbolically linked files](https://github.com/photoprism/photoprism/issues/1049)
- Thumbs: [Creating redundant JPEG files is skipped to save disk space](https://github.com/photoprism/photoprism/issues/1874)
- Zip: [Improved file system rights detection and temporary file handling](https://github.com/photoprism/photoprism/issues/2532)
- Metadata: [Creation time is extracted from DateTimeCreated, if available](https://github.com/photoprism/photoprism/pull/2513)
- Metadata: [Unknown values are ignored when parsing timestamps](https://github.com/photoprism/photoprism/issues/2510)
- Purge: [Fixed SQL error when the photo ID of a file is missing](https://github.com/photoprism/photoprism/issues/2540)
- Cleanup: [Improved logging when deleting related sidecar files](https://github.com/photoprism/photoprism/issues/2521)
- Config: [Added `PHOTOPRISM_AUTH_MODE` option to select authentication mode](https://github.com/photoprism/photoprism/commit/591a6562707457045f504defba69e693afccba65)
- Config: [Improved inline docs in `docker-compose.yml` examples](https://github.com/photoprism/photoprism/pull/2536)
- Build: [Updated Go to v1.18.4, which includes a number of security and compiler fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.18.4+label%3ACherryPickApproved)
- Translations: [Added Greek](https://github.com/photoprism/photoprism/pull/2529)

Breaking Changes

- Config: [`PHOTOPRISM_AUTH` has been removed in favor of `PHOTOPRISM_AUTH_MODE`](https://github.com/photoprism/photoprism/commit/591a6562707457045f504defba69e693afccba65)
- Config: [`PHOTOPRISM_PUBLIC` has been deprecated in favor of `PHOTOPRISM_AUTH_MODE`](https://github.com/photoprism/photoprism/commit/591a6562707457045f504defba69e693afccba65)

### June 29, 2022 ###
<span class="build">Build 220629-5d7448d2</span>

With this update, you'll enjoy a much faster and [smoother scrolling experience](https://github.com/photoprism/photoprism/pull/2433) as well as [direct streaming](https://github.com/photoprism/photoprism/issues/2461) of OGV, VP8, VP9, AV1, WebM and HEVC videos if they do not exceed the [configured bitrate limit](https://docs.photoprism.app/getting-started/config-options/#file-conversion). Special thanks to [Heiko Mathes](https://github.com/heikomat) and [Andre Carrera](https://github.com/acarrera94) for their contributions!

- UX: [Much faster and smoother scrolling experience in albums and search results](https://github.com/photoprism/photoprism/pull/2433)
- Videos: [Direct streaming of OGV, VP8, VP9, AV1, WebM, and HEVC where supported](https://github.com/photoprism/photoprism/issues/2461)
- Videos: [Fixed incorrect frame rate when using NVIDIA hardware transcoding](https://github.com/photoprism/photoprism/issues/2442)
- Sharing: [Fixed the spacing of the top navigation toolbar on small screens](https://github.com/photoprism/photoprism/pull/2430)
- RAW: [Display actual dimensions as Exif metadata can be wrong, e.g. for `.NEF` files](https://github.com/photoprism/photoprism/issues/2447)
- WebDAV: [Endpoints have been disabled in public mode as they cannot be used](https://github.com/photoprism/photoprism/issues/2464)
- API: [Maximum number of search results has been increased to 100,000 files](https://github.com/photoprism/photoprism/commit/b6d32f828b6f4beea504e433f67c5395df178053)
- CLI: [Config command also lists `disable-webdav` and `http-compression`](https://github.com/photoprism/photoprism/issues/2476)
- Documentation: [Added notes about manual session invalidation and other known issues](https://docs.photoprism.app/known-issues/)
- Translations: [Updated Arabic](https://github.com/photoprism/photoprism/pull/2458/files), [Dutch, Polish](https://github.com/photoprism/photoprism/pull/2435/files), [Japanese, Chinese](https://github.com/photoprism/photoprism/pull/2445/files), [French](https://github.com/photoprism/photoprism/commit/0f0d2b4df05ff0534c9435a7802e47672f0adcb7), [German, and Italian](https://github.com/photoprism/photoprism/commit/49b9c4afb76ea316620194142e836003b0298f23)

### June 17, 2022 ###
<span class="build">Build 220617-0402b8d3</span>

This update features updated translations as well as fixes for recently discovered issues.

- Albums: [A deleted album is restored when trying to add a new album with the same name](https://github.com/photoprism/photoprism/issues/2429)
- WebDAV: [Added support for auto indexing/importing in a sub-directory on a shared domain](https://github.com/photoprism/photoprism/pull/2392)
- Translations: [Updated Arabic, Czech, Korean, and Norwegian Bokmål](https://github.com/photoprism/photoprism/pull/2421)

### June 14, 2022 ###
<span class="build">Build 220614-dea9ff68</span>

A small but important update that includes translations to Arabic, a migration fix for MariaDB, and many updated dependencies.

- Security: [Updated Go to v1.18.3](https://github.com/photoprism/photoprism/commit/942fedf67992ef5eb9d8f371da88aec333a13af0), [which includes TLS and validation fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.18.3)
- MariaDB: [Removed migration that could corrupt photo descriptions in the index](https://github.com/photoprism/photoprism/issues/2398)
- Translations: [Added Arabic](https://github.com/photoprism/photoprism/pull/2417), [updated Danish and Polish](https://github.com/photoprism/photoprism/pull/2413)

### May 28, 2022 ###
<span class="build">Build 220528-efb5d710</span>

This update includes translations that were recently contributed via [translate.photoprism.app](https://translate.photoprism.app/). Missing translations were added by us using DeepL and Google Translate. Native speakers are invited to help improve those if needed. Thank you very much!

- UX: [Mobile toolbar menu has been redesigned](https://dl.photoprism.app/img/ui/mobile-grayscale-submenu.png) and [made accessible in public mode](https://github.com/photoprism/photoprism/issues/2370)
- Themes: [*Gemstone* and *Raspberry* have been updated](https://dl.photoprism.app/img/ui/desktop-gemstone-plus.png)

### May 27, 2022 ###
<span class="build">Build 220527-005770ca</span>

This update improves navigation fonts and [mobile submenu colors](https://dl.photoprism.app/img/ui/mobile-submenu-light-797x567.png) for light themes. We are also working to establish [PhotoPrism+](https://www.photoprism.app/membership) as the name for our community membership and associated benefits. For this, membership [information in the app](https://try.photoprism.app/library/about), [on our website](https://www.photoprism.app/membership), on [GitHub Sponsors](https://link.photoprism.app/sponsor) and [Patreon](https://link.photoprism.app/patreon) is gradually being updated.

- UX: [Fixed light theme colors of mobile navigation submenu](https://github.com/photoprism/photoprism/issues/2359)
- UX: [Splash screen has been updated and no longer depends on admin theme](https://github.com/photoprism/photoprism/issues/2360)

### May 24, 2022 ###
<span class="build">Build 220524-c76de0df</span>

This service release fixes potential issues with our new Debian 12-based Docker image that shipped with the last update. These may have prevented users from deploying it without making changes to their environment. In our ongoing effort to improve usability and performance, we have also implemented a number of UX/UI optimizations, such as using the default operating system font instead of Google's Roboto.

- UX: [Added submenu to mobile navigation toolbar](https://github.com/photoprism/photoprism/commit/8b5fbec950ddf6209609f17fa829cc8adabf3699)
- UX: [Updated splash screen information and animation](https://github.com/photoprism/photoprism/commit/c1d06f5d2b74e1975442589f2b7ac280cbd4da88)
- UX: [Numerous translations have been added and updated](https://translate.photoprism.app/)
- UX: [Improved UI styles for right-to-left languages](https://github.com/photoprism/photoprism/commit/ab185f719e9f79f01a32f1d38279ec1dfddc826a)
- Auth: [Short initial passwords are permitted again to avoid login problems](https://github.com/photoprism/photoprism/issues/2339)
- Logs: [Repeated log messages are omitted to prevent feedback loops](https://github.com/photoprism/photoprism/issues/2335)
- Logs: [Trace and debug messages are no longer displayed in the UI to avoid information leaks and reduce websocket communication overhead](https://github.com/photoprism/photoprism/issues/2335)
- Search: [`mono:true` filter now omits files with unknown chroma](https://github.com/photoprism/photoprism/issues/2341)
- Docker: [Removed incorrect permission check for storage folder on startup](https://github.com/photoprism/photoprism/issues/2334)
- Docker: [Supported User and Group ID ranges have been documented](https://github.com/photoprism/photoprism/issues/2336)

**Thank you to everyone who [helped with testing](https://github.com/photoprism/photoprism/projects/5?card_filter_query=label%3Aplease-test), [signed up as a member](https://www.photoprism.app/membership), or [contributed](https://github.com/photoprism/photoprism/graphs/contributors) in other ways! We appreciate it very much.**

### May 17, 2022 ###
<span class="build">Build 220517-b9c68f8f</span>

This update features search UX enhancements, a new Docker base image based on Debian 12 "Bookworm",
as well as fixes for recently discovered issues. Front- and backend [translations](https://translate.photoprism.app/) in numerous
languages have been added and updated. Thanks to all involved!

- File Formats: [Added native support for WebP images](https://github.com/photoprism/photoprism/issues/1226) and [animated GIFs](https://github.com/photoprism/photoprism/commit/82d61d1f93961daa5b9ffea31e2ae4ab8897d2a7)
- UX: [RAW files are skipped by default when downloading photos and ZIP archives](https://github.com/photoprism/photoprism/issues/2234)
- Auth: [Passwords must have at least 8 characters to mitigate brute-force attacks](https://github.com/photoprism/photoprism/issues/2248)
- Search: [User interface and database performance optimizations](https://github.com/photoprism/photoprism/issues/1438)
- Search: [Fixed occasional lag when entering queries in the search toolbar](https://github.com/photoprism/photoprism/issues/1995)
- Search: [Improved `album:...` filter supports numeric names, `albums:..` also AND/OR](https://github.com/photoprism/photoprism/issues/1994)
- Search: [Improved `camera:...` and `lens:...` filters accept names in addition to IDs](https://github.com/photoprism/photoprism/issues/2079)
- Search: [Added `square:yes` and `landscape:yes` filters](https://github.com/photoprism/photoprism/issues/2169)
- Albums: ["Add to album" dialog preloads more names for auto-completion](https://github.com/photoprism/photoprism/pull/2152)
- Albums: [Album names are shortened if necessary to avoid errors when saving](https://github.com/photoprism/photoprism/issues/2181)
- Albums: [Fixed accidental creation of duplicates by pressing Enter multiple times](https://github.com/photoprism/photoprism/issues/2233)
- People: [Improved logging and fixed potential issues with matching unrecognized faces](https://github.com/photoprism/photoprism/issues/2182)
- Places: [Number of pictures rendered on the map has been limited to 500,000](https://github.com/photoprism/photoprism/commit/49e923232380117c8b1eab9ff5b41de878d46ab2)
- Library: [Added button to clear log history in *Library* > *Errors*](https://github.com/photoprism/photoprism/discussions/1683)
- Library: [RAW previews and the number of actual files are shown under Originals](https://github.com/photoprism/photoprism/issues/2273)
- Library: [Disabled hidden files warning while indexing as it can be misleading](https://github.com/photoprism/photoprism/issues/2189)
- Index: [Fixed errors when re-indexing libraries with archived photos](https://github.com/photoprism/photoprism/issues/2257)
- Index: [RAW and video conversion commands run in a virtual home directory](https://github.com/photoprism/photoprism/issues/2262)
- Thumbnails: [Reduced default JPEG quality from 92 to 85 to optimize storage and loading](https://github.com/photoprism/photoprism/issues/2215)
- Metadata: [Manual local time changes are always preserved when reindexing](https://github.com/photoprism/photoprism/issues/2239)
- Metadata: [Fixed Exif orientation flag when converting HEIF/HEIC images to JPEG](https://github.com/photoprism/photoprism/discussions/2214)
- Metadata: [Fault-tolerant parsing of timestamps from Exif and JSON sidecar files](https://github.com/photoprism/photoprism/issues/625)
- Metadata: [Improved parsing of two-digit years in original file paths](https://github.com/photoprism/photoprism/issues/2271)
- Metadata: [Exif IFD1 tags with existing IFD0 values are ignored to improve standard compliance](https://github.com/photoprism/photoprism/issues/2231)
- Metadata: [Brute-force search is skipped by default if no Exif headers were found in JPEG, PNG, TIFF, and HEIF files](https://github.com/photoprism/photoprism/issues/2196)
- Metadata: [SubSecDateTimeOriginal and SubSecCreateDate timestamps are preferred](https://github.com/photoprism/photoprism/issues/2320)
- WebDAV: [Up- and download sync can no longer be enabled at the same time to prevent unexpected behavior](https://github.com/photoprism/photoprism/issues/1785)
- WebDAV: [Added timeout/retry settings and improved handling of sync errors](https://github.com/photoprism/photoprism/issues/1781)
- WebDAV: [Fixed sharing videos and uploading automatically created albums](https://github.com/photoprism/photoprism/issues/2293)
- CLI: [Renamed `--config-file` to `--defaults-yaml` and improved command help](https://github.com/photoprism/photoprism/issues/2250)
- CLI: [Added short names for common config flags, e.g. `-i` for `--wakeup-interval`](https://github.com/photoprism/photoprism/issues/2195)
- CLI: [Run `photoprism show tags` to display metadata tags and supported standards](https://github.com/photoprism/photoprism/issues/2252)
- CLI: [Run `photoprism show formats` to display supported media and sidecar file formats](https://github.com/photoprism/photoprism/issues/2247)
- CLI: [Run `photoprism show filters` to display a search filter overview with examples](https://github.com/photoprism/photoprism/commit/7291c1d70329d85af2dfc1e9de512d28378974a5)
- Config: [Improved FFmpeg parameters for Intel QSV hardware transcoding](https://github.com/photoprism/photoprism/issues/2222)
- Config: [Added NVIDIA hardware video transcoding support for members](https://github.com/photoprism/photoprism/issues/2125)
- Config: [Added `--disable-raw` flag to disable indexing and conversion of RAW files](https://github.com/photoprism/photoprism/issues/2227)
- Config: [Added `--resolution-limit` option to skip high-resolution images when indexing](https://github.com/photoprism/photoprism/issues/1017)
- Docker: [New Debian 12 "Bookworm" base image with FFmpeg 4.4.1 and Darktable 3.8.1](https://github.com/photoprism/photoprism/issues/2178)
- Docker: [Added default users and groups for enhanced video transcoding compatibility](https://github.com/photoprism/photoprism/issues/2228)
- Translations: [Added Swedish, Romanian, Turkish, Lithuanian, Bulgarian, Malay, and Croatian](https://translate.photoprism.app/)

### March 2, 2022 ###
<span class="build">Build 220302-0059f429</span>

The [Docker images](https://hub.docker.com/r/photoprism/photoprism/tags) for this release are based on Debian 11
"Bullseye" and include many updated dependencies such as [Darktable 3.8](https://www.darktable.org/2022/02/darktable-3.8.1-released/).
Behind the scenes, the build process has also been improved so that it will be easier to provide standalone packages in the future.

- Auth: [New login screen with more space for buttons, links, and legal information](https://github.com/photoprism/photoprism/issues/782)
- Metadata: [Redesigned file details tab in the edit dialog](https://github.com/photoprism/photoprism/issues/2017)
- Metadata: [Support for Zulu formatted timestamps in Exiftool JSON and XMP](https://github.com/photoprism/photoprism/issues/2082)
- Sharing: [Fixed upload of complete albums via WebDAV](https://github.com/photoprism/photoprism/issues/1376)
- Sharing: [Manual WebDAV upload of video and RAW files](https://github.com/photoprism/photoprism/issues/829)
- iOS: [Fixed multi-select via long touch in Safari PWA mode](https://github.com/photoprism/photoprism/issues/2074)
- API: [Added cache control header for faster thumbnail loading](https://github.com/photoprism/photoprism/issues/822#issuecomment-1046276315)
- Config: [Simplified configuration of Unix domain socket database connections](https://github.com/photoprism/photoprism/commit/9c1325f38ec38bc4ca01df4ca8bc723841cc7cc7)
- Config: [Added `--imprint` and `--imprint-url` to display legal information in the footer](https://github.com/photoprism/photoprism/issues/1990)
- Docker: [Automatic installation of compatible CPU and GPU drivers](https://github.com/photoprism/photoprism/issues/2076)
- Translations: [Updated all front- and backend locales](https://github.com/photoprism/photoprism/issues/2083)

*You can now join us on [translate.photoprism.app](https://translate.photoprism.app/) to help translate the UI!*

### January 21, 2022 ###
<span class="build">Build 220121-2b4c8e1f</span>

We've generated missing translations with the help of DeepL and Google Translate. Native speakers are
invited to help us improve those if needed. [Learn how to contribute](developer-guide/translations-weblate.md).

- [Minimum memory requirements have been reduced to 3 GB](https://github.com/photoprism/photoprism/discussions/1921#discussioncomment-2005493)
- Photos: [Fixed buttons in full screen view](https://github.com/photoprism/photoprism/issues/1961)
- People: [Fixed typo that prevented face matching optimization](https://github.com/photoprism/photoprism/issues/1957)
- Moments: [Improved update performance on MariaDB](https://github.com/photoprism/photoprism/issues/1953)
- Translations: [Pre-translated missing UI messages](https://github.com/photoprism/photoprism/commit/f7b82f616d73ed2f61e0195e31d5029ca1bda3b6)

### January 18, 2022 ###
<span class="build">Build 220118-76c94a1f</span>

- Auth: [Logout redirects to base URI instead of site root](https://github.com/photoprism/photoprism/issues/1901)
- Videos: [Excluded streaming from gzip compression](https://github.com/photoprism/photoprism/commit/4d8292a9c3e357dc8d956a13ee9d6faa34b69119)
- Videos: [Fixed Content-Type header and streaming in Safari](https://github.com/photoprism/photoprism/issues/1648)
- Folders: [Fixed search query string substitutions and sanitation](https://github.com/photoprism/photoprism/issues/1930)
- UI: [Updated information and links in *Settings* > *About*](https://try.photoprism.app/library/about)
- UI: [Improved bootstrap template rendering performance](https://github.com/photoprism/photoprism/commit/03457bdb755b7cfb088a72f564119fb8e7a46ec2)

### January 7, 2022 ###
<span class="build">Build 220107-f5b7ef83</span>

Based on our zero bug policy, this update focuses on bug fixes, security, and UX enhancements for search 
filters, metadata, and the indexer. In addition, one of the merged pull requests may improve face recognition 
performance on smaller devices and with large libraries.

- People: [Improved update performance on MariaDB](https://github.com/photoprism/photoprism/pull/1804)
- People: [Improved contrast of person selection menu](https://github.com/photoprism/photoprism/issues/1824)
- Albums: [Private pictures are excluded from download as zip](https://github.com/photoprism/photoprism/issues/1836)
- Search: [Improved query parser for additional security](https://github.com/photoprism/photoprism/issues/1814)
- Search: [Added `uid:...` search filter to find photos by uid](https://github.com/photoprism/photoprism/issues/1820)
- Search: [`keywords:...` filter does not exclude stopwords anymore](https://github.com/photoprism/photoprism/issues/1859)
- Index: [Original filenames can be extracted from Exiftool JSON](https://github.com/photoprism/photoprism/issues/1892)
- Index: [More accurate and resilient handling of related files and photo stacks](https://github.com/photoprism/photoprism/issues/1823)
- Live Photos: [HEIF is used to create primary JPEG instead of a MOV still image](https://github.com/photoprism/photoprism/issues/926)
- Metadata: [Reduced log level for missing Exif data from warn to info](https://github.com/photoprism/photoprism/commit/5462b1e69eddccedbf0259263aba04b68cf8044c)
- Metadata: [Increased size of projection and color profile fields to 40 characters](https://github.com/photoprism/photoprism/issues/1830)
- Backups: [Improved help for config options and CLI commands](https://github.com/photoprism/photoprism/issues/1887)
- Help: [Fixed reverse proxy documentation links](https://github.com/photoprism/photoprism/pull/1870)
- Config: [Added Apple Video Toolbox hardware transcoding support for macOS](https://github.com/photoprism/photoprism/pull/1843)
- Config: [Added `/opt/photoprism` to search path for asset and storage folders](https://github.com/photoprism/photoprism/issues/1821)

### December 15, 2021 ###
<span class="build">Build 211215-93b26f19</span>

PhotoPrism is not directly affected by the [Apache Log4j](https://www.malwarebytes.com/blog/news/2021/12/log4j-zero-day-log4shell-arrives-just-in-time-to-ruin-your-weekend) vulnerability.
Logs may still contain messages that can cause harm if consumed by an unpatched Java application.
As a precaution, this release includes additional [rules and filters to validate user input](https://github.com/photoprism/photoprism/issues/1814).

- Sharing: [Fixed album link redirect on shared domains](https://github.com/photoprism/photoprism/issues/1617)
- Import: [More helpful warning when another import is already running](https://github.com/photoprism/photoprism/issues/1810)
- Docker: [ARMv7 image for 32-bit processors and operating systems](https://github.com/photoprism/photoprism/issues/1815)

### December 10, 2021 ###
<span class="build">Build 211210-2cb90e7e</span>

Starting with this release, the [regular multi-arch Docker image](https://hub.docker.com/r/photoprism/photoprism/tags?name=latest) is 64-bit only. 
A 32-bit version of our stable release for [older devices](getting-started/raspberry-pi.md#older-armv7-based-devices) 
is offered separately. This frees up development and infrastructure resources with minimal impact.

- Security: [Updated Go to v1.17.5, which includes HTTP/2 and networking fixes](https://groups.google.com/g/golang-announce/c/hcmEScgc00k)
- People: [Concurrent updates are no longer possible to prevent inconsistencies](https://github.com/photoprism/photoprism/commit/1b583e071e80b68352b1b366d60e010d8f8f9535)
- Places: [Additional logs to detect invalid GPS coordinates in metadata](https://github.com/photoprism/photoprism/commit/4e358bbfd488eda86efa3265a6c443be0ae8f038)
- SQLite: [Reduced routine maintenance log levels and fixed migration warnings](https://github.com/photoprism/photoprism/discussions/1791)
- Thumbnails: [Apple Display P3 profile support for more accurate colors](https://github.com/photoprism/photoprism/issues/1798)
- Translations: [Updated French](https://github.com/photoprism/photoprism/pull/1799)

### December 3, 2021 ###
<span class="build">Build 211203-fdb6b5e1</span>

Since the [funding goal](https://link.photoprism.app/sponsor) required to make all features and maps generally
available has not been reached, *early-access features* have been renamed to *sponsor features* in this update.
Offline and high-resolution street maps remain free for everyone, while hybrid, topographic, and outdoor maps are 
now a member feature. We believe this is fair. A big thank you to all our [sponsors](https://link.photoprism.app/sponsors)
and [contributors](https://github.com/photoprism/photoprism/graphs/contributors/)!

- CLI: [Improved parameter](https://github.com/photoprism/photoprism/issues/1778) and [command descriptions](https://github.com/photoprism/photoprism/issues/1735)
- CLI: [Reset command optionally also deletes files in the cache folder](https://github.com/photoprism/photoprism/issues/1787)
- Config: [Improved `docker-compose.yml` examples](https://dl.photoprism.app/docker/)

### November 30, 2021 ###
<span class="build">Build 211130-13cfcf6d</span>

- Videos: [Live photos page has been added to the sub-navigation](https://github.com/photoprism/photoprism/issues/1761)
- Albums: [Manually created albums are sorted by name, with favorites first](https://github.com/photoprism/photoprism/issues/1777)
- Places: [Improved location details in border regions](https://github.com/photoprism/photoprism/issues/1767) and [near Paris](https://github.com/photoprism/photoprism/issues/1776)
- PWA: [Updated app icons, style is now also applied to the user interface](https://github.com/photoprism/photoprism/tree/develop/assets/static/icons)

*For our [sponsors](https://link.photoprism.app/patreon) and [contributors](https://docs.photoprism.app/developer-guide/):*

- UI: New *Abyss* and *Gemstone* dark themes 💎

### November 28, 2021 ###
<span class="build">Build 211128-7e8974fd</span>

Official support for MySQL 8 is discontinued with this update as Oracle seems to have stopped shipping [new features and enhancements](https://github.com/photoprism/photoprism/issues/1764).
As a result, the testing effort required before each release is no longer feasible. We recommend [upgrading](https://docs.photoprism.app/getting-started/troubleshooting/#version-upgrade)
to [MariaDB 10.6](https://mariadb.com/kb/en/function-differences-between-mariadb-106-and-mysql-80/) or later.
PostgreSQL support is [planned for 2022](https://github.com/photoprism/photoprism/issues/47) without a specific release date yet.

- CLI: [`photoprism migrations run --failed` will re-run previously failed migrations](https://github.com/photoprism/photoprism/commit/7e8974fd20fcbf3ec403541125599deaeb1ee353)

### November 27, 2021 ###
<span class="build">Build 211127-86c43159</span>

When possible, location estimates now include a latitude and longitude. Photos load faster when you open 
them in *Places*, and the viewer sorts them by distance. Time zone handling has been completely reworked, 
in particular for UTC. The Docker base image has been updated to Ubuntu 21.10, which ships with 
Darktable 3.6 among other updated dependencies. 

- UX: Redesigned [splash screen](https://github.com/photoprism/photoprism/commit/293fa0ca784ae19998cc8ff3459883a137fff4c2) based on theme colors
- Places: [Viewer loads faster and sorts photos by distance instead of date](https://try.photoprism.app/library/places)
- Places: [Less frequent estimates to reduce background activity](https://github.com/photoprism/photoprism/issues/1736)
- Places: [Normalized names of states, oceans, and lakes](https://github.com/photoprism/photoprism/issues/1664)
- Places: [Updated location data from OpenStreetMap](https://www.openstreetmap.org/)
- Places: [State albums are grouped by country name](https://github.com/photoprism/photoprism/issues/1608)
- Folders: [Path names are searched in addition to titles](https://github.com/photoprism/photoprism/issues/1737)
- People: [Improved face detection performance](https://github.com/esimov/pigo/releases/tag/v1.4.5)
- People: [Fixed naming faces in non-primary files](https://github.com/photoprism/photoprism/issues/1710)
- People: [Optimized matching of children's faces](https://github.com/photoprism/photoprism/issues/1587)
- RAW: [Updated Darktable to 3.6.0](https://github.com/photoprism/photoprism/issues/1632)
- Metadata: [Improved estimates and UTC time zone handling](https://github.com/photoprism/photoprism/issues/1668)
- Metadata: [Altitude is indexed even if coordinates are missing](https://github.com/photoprism/photoprism/issues/1749)
- Auth: [Usernames are not case-sensitive anymore](https://github.com/photoprism/photoprism/commit/a354a170418371384ae047aef2bf49888e444dc5)
- CLI: [Added `--force` flag to `photoprism optimize` command](https://github.com/photoprism/photoprism/commit/04cde0f39254c7eff04b3e481ebdca4ead747b16)
- CLI: [Improved parameter and command descriptions](https://github.com/photoprism/photoprism/commit/9da2e92fb603057cf7e2e596391e88db161d2bbc)
- Config: [Improved `docker-compose.yml` examples](https://dl.photoprism.app/docker/)
- Translations: Added [Bahasa Indonesia](https://github.com/photoprism/photoprism/issues/1689) and [Hungarian](https://github.com/photoprism/photoprism/pull/1751)
- Translations: Updated [Polish](https://github.com/photoprism/photoprism/pull/1674) and [Italian](https://github.com/photoprism/photoprism/pull/1706)

*For our [sponsors](https://link.photoprism.app/patreon) and [contributors](https://docs.photoprism.app/developer-guide/):*

- CLI: [Run `photoprism places update` to retrieve updated location details](https://docs.photoprism.app/getting-started/docker-compose/#command-line-interface)
- Config: [Set `PHOTOPRISM_APP_ICON` to choose an alternative PWA icon](getting-started/config-options.md)

### October 18, 2021 ###
<span class="build">Build 211018-e200f322</span>

- UI: [Updated *Lavender* theme](https://github.com/photoprism/photoprism/commit/1efdf1c1a3690fa22658bc42786aa6b1fff217e4)
- Places: [Fixed maps initialization after reload in non-public mode](https://github.com/photoprism/photoprism/commit/e200f322be07f6ada9cd88902ba65372c69f0364)
- Search: [Added `live` and `raw:true` filters as alternative to `type:…`](https://github.com/photoprism/photoprism/commit/25a954d56821108369cc1a397f1b0a7a3a22c504)
- Search: [Added `faces:new` alias for `face:new`](https://docs.photoprism.app/user-guide/organize/people/#recognized-new-people)
- Config: [Maximum background worker interval has been increased to 7 days](https://github.com/photoprism/photoprism/issues/1618)
- Security: [Added `Content-Security-Policy` header to prevent framing attacks](https://github.com/photoprism/photoprism/commit/2ddb1d6daaab847cd95f38aaa2f9293f35023f9a)
- Translations: Updated [Russian](https://github.com/photoprism/photoprism/pull/1622) and [Slovak](https://github.com/photoprism/photoprism/pull/1620)

*For our [sponsors](https://link.photoprism.app/patreon) and [contributors](https://docs.photoprism.app/developer-guide/):*

- UI: New *Vanta* dark theme ✨

### October 10, 2021 ###
<span class="build">Build 211010-83b4f783</span>

- Translations: [Fixed German frontend typo](https://github.com/photoprism/photoprism/blob/fa57db7aa43fa03eef7a738122e15a98af574713/frontend/src/locales/de.po#L494)
- Translations: [Updated all backend locales](https://github.com/photoprism/photoprism/tree/develop/assets/locales)

*We've generated missing translations with the help of DeepL and Google Translate. Native speakers are 
invited to help us improve those if needed. [Learn how to contribute](developer-guide/translations-weblate.md).*

### October 9, 2021 ###
<span class="build">Build 211009-d6cc8df5`</span>

- UX: [Improved wording of search result notifications](https://github.com/photoprism/photoprism/commit/67d06fd647a7bf4fcf2c3e487a590b6597111d08)
- UX: [Fixed sidebar navigation on small screens](https://github.com/photoprism/photoprism/issues/1175)
- Users: [Show name and email in sidebar navigation](https://github.com/photoprism/photoprism/commit/d6cc8df531dbc17ffc6f55bc259bb45c8ea60011)
- Folders: [Directory names listed in .ppignore are ignored](https://github.com/photoprism/photoprism/issues/1609)
- Config: [Allows bypassing low memory suggestion](https://github.com/photoprism/photoprism/issues/1611)
- Docs: [Updated about page](https://github.com/photoprism/photoprism/commit/1cc8cb7ad42bcd847a03a3bba52ad265b0f3fce2)
- Translations: [Updated all frontend locales](https://github.com/photoprism/photoprism/tree/develop/frontend/src/locales)

### October 7, 2021 ###
<span class="build">Build 211007-8f55d6f8</span>

- People: [Improved stability and performance of new faces overview page](https://github.com/photoprism/photoprism/issues/1576)
- Index: [Duplicate error logs caused by broken JPEG files have been removed](https://github.com/photoprism/photoprism/commit/f7153cdd219d487733a7a3a8809b333bdace6294)
- UX: [Enhanced visibility of file errors in the edit dialog files tab](https://github.com/photoprism/photoprism/commit/6cd5ee6d9b53aed74d92c46ccb29f78adf11811a)
- CLI: [Revised descriptions of commands and configuration flags](https://github.com/photoprism/photoprism/search?q=cli+help&type=commits)

*For our [sponsors](https://link.photoprism.app/patreon) and [contributors](https://docs.photoprism.app/developer-guide/):*

- People: [Recognized faces can be hidden on the overview page](https://github.com/photoprism/photoprism/issues/1554) 

### October 2, 2021 ###
<span class="build">Build 211002-bf015326</span>

- People: [Enhanced UI / UX for renaming and merging faces](https://github.com/photoprism/photoprism/issues/1557)
- People: [Improved face detection accuracy](https://github.com/photoprism/photoprism/commit/582a3308375b8a2aaf5ca578d3c2e7d9081b580d)
- Labels: [Improved photo count accuracy](https://github.com/photoprism/photoprism/issues/584)
- Covers: [Thumbnails load and update faster](https://github.com/photoprism/photoprism/issues/383)
- Search: [Finds titles when query is too short for full-text index](https://github.com/photoprism/photoprism/issues/1560)
- Search: [`name:…` filter ignores path and extension](https://github.com/photoprism/photoprism/commit/39dc5cb777fbcb5b433430836373d136c6c5ec08)
- Videos: [Optional Intel GPU hardware transcoding support](https://github.com/photoprism/photoprism/issues/1337)
- Index: [Automatic cleanup of orphaned file entries](https://github.com/photoprism/photoprism/issues/1559)
- Logs: [Updated log messages for improved readability](https://github.com/photoprism/photoprism/commit/9a88d7fc6acf2ad5e7cfa215c78ccae39ccbb7ed)
- Translations: [Updated German and French](https://github.com/photoprism/photoprism/tree/develop/frontend/src/locales)
- Docker: [Simplified installation of TensorFlow with AVX / AVX2 support](https://github.com/photoprism/photoprism/issues/1337)
- Docker: [Entrypoint script uses prefixed environment variables, `UID` and `GID` are deprecated](https://github.com/photoprism/photoprism/issues/1545#issuecomment-929511730)

### September 25, 2021 ###
<span class="build">Build 210925-96168e4b</span>

- [Recognizes faces so that specific people can be found](https://github.com/photoprism/photoprism/issues/22)
- UX: [Improved UI design, navigation, and wording](https://github.com/photoprism/photoprism/search?o=desc&q=UX&s=committer-date&type=commits)
- Search: [Omit full-text index if query is too short](https://github.com/photoprism/photoprism/issues/1517)
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
- Config: [Added disable options for image classification and facial recognition](https://docs.photoprism.app/getting-started/config-options/)
- Config: [Added support for non-root site URLs](https://github.com/photoprism/photoprism/issues/425)
- Config: [Added content delivery network URL option](https://github.com/photoprism/photoprism/issues/1351)
- MariaDB: [Set explicit table engine, charset, and collation](https://github.com/photoprism/photoprism/issues/1371)
- MariaDB: [Added log message for old versions with broken table name resolution](https://github.com/photoprism/photoprism/issues/1544)
- Docker: [Added `HOME` env for Darktable & RawTherapee](https://github.com/photoprism/photoprism/issues/1525)
- Docker: [Single multi-arch image for AMD64, ARM64, and ARMv7](https://github.com/photoprism/photoprism/issues/1158)

### May 23, 2021 ###
<span class="build">Build 210523-b1856b9d</span>

- RAW: [Added RawTherapee flag to use existing sidecar files](https://github.com/photoprism/photoprism/issues/1267)
- Import: [Never remove ignored folders such as for Syncthing](https://github.com/photoprism/photoprism/issues/1319)

### May 20, 2021 ###
<span class="build">Build 210520-4b32bac7</span>

- Docker: [Fixed home directory permissions in new base image](https://github.com/photoprism/photoprism/issues/1301)
- HEIF: [Test if JPEG was already rotated based on video metadata](https://github.com/photoprism/photoprism/blob/develop/scripts/dist/heif-convert.sh)

### May 19, 2021 ###
<span class="build">Build 210519-24b5c7e6</span>

- Metadata: [Updated Exiftool to fix security issue](https://github.com/photoprism/photoprism/issues/1302)

### May 18, 2021 ###
<span class="build">Build 210518-80981c25</span>

- Safari: [Fixed PWA file download on iOS](https://github.com/photoprism/photoprism/issues/895)
- Docker: [Added config example for scheduled background tasks](https://dl.photoprism.app/docker/scheduler/)
- Docker: [Updated base image includes Darktable 3.4.1, RawTherapee 5.8, and FFmpeg 4.3.2](https://github.com/photoprism/photoprism/commit/77ddcecf29c95e1b33ba11046fd002ed3d408382)
- TensorFlow: [Improved error handling](https://github.com/photoprism/photoprism/issues/1270)
- Translations: [Updated French](https://github.com/photoprism/photoprism/pull/1286)

### May 5, 2021 ###
<span class="build">Build 210505-d3e53a89</span>

- UI: [Improved RTL (right-to-left language) alignment](https://github.com/photoprism/photoprism/pull/1220)
- RAW: [Added config options to disable specific converters](https://github.com/photoprism/photoprism/issues/1245)
- Metadata: [Preserve stopwords in existing keywords](https://github.com/photoprism/photoprism/issues/1153)
- Metadata: [Allow single quotes in keywords](https://github.com/photoprism/photoprism/issues/1196)
- WebDAV: [Keep favorite flag when uploading via PhotoSync](https://github.com/photoprism/photoprism/issues/1210)
- Translations: Updated [Dutch](https://github.com/photoprism/photoprism/pull/1247)
  and [German](https://github.com/photoprism/photoprism/commit/c9795495ee5b2a57be8ddcdb16ca29cfab018bb4)

### April 26, 2021 ###
<span class="build">Build 210426-da6e948f</span>

- UI: [Added Yellowstone theme for members, unlocked Grayscale theme for everyone](https://github.com/photoprism/photoprism/commit/180e46b95f52a5ef2d67ea8ac5e1d8a9b08ef970)
- Metadata: [Support for XMP sidecar CreateDate and Keywords](https://github.com/photoprism/photoprism/issues/1151)
- Metadata: [Merge keywords from different sources](https://github.com/photoprism/photoprism/issues/1153)
- Translations: Updated [Hebrew](https://github.com/photoprism/photoprism/pull/1221)
  
### April 22, 2021 ###
<span class="build">Build 210422-97e75b04</span>

- UX: [Improved touch event accuracy](https://github.com/photoprism/photoprism/issues/1048)
- UX: [Optimized rendering on small screens](https://github.com/photoprism/photoprism/commit/b07ba63108dace2a8d5b2df18a06647252a36272)
- UX: [Fixed autocomplete in "add to album" dialog](https://github.com/photoprism/photoprism/issues/1130)
- HEIF: [Prevent redundant sidecar JPEG files](https://github.com/photoprism/photoprism/issues/926)
- Backup: [Added command flags and usage docs](https://github.com/photoprism/photoprism/issues/1190)
- Translations: Added [Danish](https://github.com/photoprism/photoprism/commits?author=tcarlsen) 
  and [Kurdish](https://github.com/photoprism/photoprism/commits?author=Hrazhan)

### February 22, 2021 ###
<span class="build">Build 210222-ac5a9d5e</span>

- UX: [Autofocus for input fields and confirm on enter](https://github.com/photoprism/photoprism/issues/1078)
- Restore: [Find YAML album backups in originals folder](https://github.com/photoprism/photoprism/commit/32ef03083d9414e0ab1f52bbb3837251e0438689)
- Metadata: [Improved location labels and moments](https://github.com/photoprism/photoprism/commit/d42eb4e01b8844d46f7332e1b8d8dc7a18e41a14)
- Thumbnails: [Fixed auto-rotation for HEIF, TIFF, and PNG images](https://github.com/photoprism/photoprism/issues/1064)
- Translations: [Added Norwegian (Bokmål)](https://github.com/photoprism/photoprism/pull/1079)

### February 17, 2021 ###
<span class="build">Build 210217-49039368</span>

- Videos: [Optimized transcoding parameters](https://github.com/photoprism/photoprism/issues/703)
- Videos: [Use AAC audio for MP4 transcoding](https://github.com/photoprism/photoprism/issues/1061)  
- Metadata: [Default to landscape orientation if data is invalid](https://github.com/photoprism/photoprism/issues/1052)
- Translations: [Updated Brazilian Portuguese](https://github.com/photoprism/photoprism/pull/1053)

### February 16, 2021 ###
<span class="build">Build 210216-4939e36a</span>

- UX: Automatically hide scrollbar in photo viewer and Places
- Delete: [Permanently remove all related sidecar files](https://github.com/photoprism/photoprism/issues/167#issuecomment-779179817)
- Videos: [Added transcoding config options](https://github.com/photoprism/photoprism/issues/703)
- Videos: [Added batch transcoding via convert command](https://github.com/photoprism/photoprism/issues/703)
- Metadata: [Remove estimate when setting a new country](https://github.com/photoprism/photoprism/issues/1018)
- Metadata: [Workaround for Exif strings containing newlines](https://github.com/dsoprea/go-exif/issues/55)

### February 11, 2021 ###
<span class="build">Build 210211-b9595dd4</span>

- Videos: [Native player featuring performance and UX enhancements](https://github.com/photoprism/photoprism/issues/915)
- Index: [Improved detection of missing photos, files, and folders](https://github.com/photoprism/photoprism/issues/1010)

### February 8, 2021 ###
<span class="build">Build 210208-9e10ba69</span>

- Upload: [Adds duplicates to selected albums as well](https://github.com/photoprism/photoprism/issues/991)
- Library: [Show folder covers in Originals](https://github.com/photoprism/photoprism/issues/1011)
- Metadata: [Automatically remove orphan countries, cameras, and lenses](https://github.com/photoprism/photoprism/issues/982)
- Metadata: [Improved Exif parser](https://github.com/photoprism/photoprism/issues/990)
- Backup: [Restore archive flag from YAML files](https://github.com/photoprism/photoprism/issues/912)
- Docker: [Improved entrypoint script](https://github.com/photoprism/photoprism/issues/1000)

### January 28, 2021 ###
<span class="build">Build 210128-a82061e0</span>

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
- Archive: [Physically delete files after confirmation](https://github.com/photoprism/photoprism/issues/167)
- Moments: [Added delete button to context menu](https://github.com/photoprism/photoprism/issues/942)
- Settings: [Added Estimates and Delete feature flags](https://github.com/photoprism/photoprism/issues/954)
- CLI: Added cleanup command to remove orphaned index entries and thumbnails

### January 21, 2021 ###
<span class="build">Build 210121-07e559df</span>

- UX: [Improved video playback and icons](https://github.com/photoprism/photoprism/issues/935)
- UX: [Restructured main navigation](https://github.com/photoprism/photoprism/issues/859)
- Mobile: [Show search field in albums](https://github.com/photoprism/photoprism/issues/937)

### January 20, 2021 ###
<span class="build">Build 210120-e7cd5e9a</span>

- API: [Apply limit, offset and sort order when searching for IDs](https://github.com/photoprism/photoprism/issues/890)
- ARM64: [Reverted database image back to arm64v8/mariadb in config example](https://github.com/photoprism/photoprism/issues/535#issuecomment-763210250)

### January 19, 2021 ###
<span class="build">Build 210119-a5399f06</span>

- UX: Optimized user interface for [iOS and tablets](https://github.com/photoprism/photoprism/issues/832)
- UX: Improved theme colors
- UX: [Scroll position is restored when navigating back](https://github.com/photoprism/photoprism/issues/896)
- Translations: Added [Czech](https://github.com/photoprism/photoprism/issues/902)
- Metadata: [Estimate timezone](https://github.com/photoprism/photoprism/issues/914) 
  and [allow overwriting estimated locations](https://github.com/photoprism/photoprism/pull/918) 
- Settings: [Fixed disabling logs](https://github.com/photoprism/photoprism/issues/891)

*For our [sponsors](https://link.photoprism.app/patreon) and [contributors](https://docs.photoprism.app/developer-guide/):*

- UX: Added two [dark themes](https://github.com/photoprism/photoprism/issues/700)

### January 11, 2021 ###
<span class="build">Build 210111-cc05c430</span>

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
- Config: [Updated docker-compose.yml examples](https://dl.photoprism.app/docker/)
- Config: [Added optional gzip compression for built-in web server](getting-started/config-options.md)
- Config: Limit number of indexing workers to half the number of physical cores by default to 
  avoid [high load](https://twitter.com/miguelarios_/status/1347775696492503040) on hyper-threading capable CPUs

### January 4, 2021 ###
<span class="build">Build 210104-7f9e806a</span>

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
<span class="build">Build 210102-af71e5f7</span>

- WebDAV: Uploads and other changes trigger [auto indexing / importing](https://github.com/photoprism/photoprism/issues/281)
- Config: Use random hash for improved preview token security 
- UX: Disabled page zoom so that app feels more native on mobile devices
- UX: Reduced min password length to 4 characters
- UX: Improved [docker-compose.yml examples](https://dl.photoprism.app/docker/)
- UX: Reduced icon size in "add to album" dialog

### December 31, 2020 ###
<span class="build">Build 201231-8e22fbf8</span>

- Initial Stable Release

### Getting Updates ###

Even when you use an image with the `:latest` tag, Docker does not automatically download new images for you. To update, you can either [manually pull the newest image](getting-started/updates.md) and restart, or set up a service like [Watchtower](getting-started/updates.md#watchtower) to get automatic updates.
