# Release Notes

!!! example ""
    **Back us on [Patreon](https://link.photoprism.app/patreon) or [GitHub Sponsors](https://link.photoprism.app/sponsor).**
    Your continued support [helps us provide regular updates](https://photoprism.app/membership) and services like [world maps](https://try.photoprism.app/library/places). Thank you! 💜

!!! tldr ""
    You can test new features by changing the image tag in your [docker-compose.yml](https://dl.photoprism.app/docker/) from `:latest` to `:preview`, then pulling the most recent image, and finally [restarting your instance](getting-started/updates.md).

### Development Preview ###
<span class="build">Build 221129-51aae94e6</span>

What's new?

- UI: [Updated "Electra" theme and removed "Seaweed"](https://github.com/photoprism/photoprism/commit/e1405eba5430d30769d90292bdc69debe0e27092)
- Videos: [Improved player compatibility with browser plugins](https://github.com/photoprism/photoprism/issues/1439)
- Albums: [Double quotes in titles are replaced with Unicode instead of single quotes](https://github.com/photoprism/photoprism/issues/2891)
- Index: [Improved query performance when flagging hidden files](https://github.com/photoprism/photoprism/issues/2928)
- Config: [Custom template path is not searched for files if not specified](https://github.com/photoprism/photoprism/issues/2946) 
- Translations: Updated Bulgarian, Chinese (traditional), Estonian, German, and Ukrainian 

### November 18, 2022 ###
<span class="build">Build 221118-e58fee0fb</span>

This service release includes compatibility fixes for MariaDB 10.10, the [latest translations](https://translate.photoprism.app/projects/photoprism/), a new theme, and updated dependencies. Note that since it is possible that new major versions of MariaDB require changes in PhotoPrism to be compatible, you should check compatibility before upgrading to new MariaDB versions that have been released very recently. We therefore recommend not using the `:latest` tag for the Docker image and to upgrade manually by changing the tag e.g. from `:10.8` to `:10.9` once we had the chance to test the new release:

```yaml
services:
  mariadb:
    image: mariadb:10.9
    ...
```

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
- Security: [Go has been upgraded to v1.19.3, which includes security fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.19.3)
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
- RAW: [Upgraded Darktable from v3.8.1 to v4.0.1 (AMD64 only)](https://github.com/photoprism/photoprism/issues/2703)
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
- Security: [Go has been upgraded to v1.19.2, which includes security fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.19.2)
- Translations: Added [Persian](https://github.com/photoprism/photoprism/pull/2767)
- Translations: Updated [Chinese](https://github.com/photoprism/photoprism/commit/6d435cab9e23c9c64fe418dafb26e0ac41970175), [Dutch](https://github.com/photoprism/photoprism/pull/2841), [Finnish](https://github.com/photoprism/photoprism/pull/2712/files), [French](https://github.com/photoprism/photoprism/pull/2830), [German](https://github.com/photoprism/photoprism/pull/2825), [Spanish](https://github.com/photoprism/photoprism/pull/2835/files), and many more

### September 1, 2022 ###
<span class="build">Build 220901-f493607b0</span>

With this update you get all the [latest translations contributed by our community](https://translate.photoprism.app/projects/photoprism/), [mobile navigation enhancements](https://dl.photoprism.app/img/ui/mobile-toolbar-navigation-open.jpg), upgraded dependencies and, as usual, fixes for recently discovered issues. Thanks to everyone involved!

What's new?

- UX: [Mobile toolbar menu has been redesigned and expanded](https://github.com/photoprism/photoprism/commit/ecadf17d506e2a4cfa9fb1bb33e942f1a6499c25)
- UX: [Improved search result and *Gemstone* theme styles](https://github.com/photoprism/photoprism/commit/3612ea016dd3b20af352009e92258f55d47a550b)
- Search: [Known file extensions are stripped from `name:...` filter string](https://github.com/photoprism/photoprism/issues/2667)
- Library: [Indexing will be aborted if the originals folder is empty](https://github.com/photoprism/photoprism/pull/2299)
- Videos: [Local time is extracted from `DateTimeOriginal` if possible](https://github.com/photoprism/photoprism/issues/2640)
- Albums: [All pictures are shown if "Private" has been disabled in *Settings*](https://github.com/photoprism/photoprism/issues/2570)
- Thumbs: [`photoprism thumbs` command regenerates thumbnails of sidecar files](https://github.com/photoprism/photoprism/issues/2669)
- Docker: [Permissions of original media files are no longer updated on startup](https://github.com/photoprism/photoprism/pull/2371)
- Build: [Go has been upgraded to v1.19, which includes fixes and enhancements](https://tip.golang.org/doc/go1.19)
- Build: [NodeJS has been upgraded from v16 to v18](https://nodejs.org/en/blog/announcements/v18-release-announce/)
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

With this update, you'll enjoy a much faster and [smoother scrolling experience](https://github.com/photoprism/photoprism/pull/2433) as well as [direct streaming](https://github.com/photoprism/photoprism/issues/2461) of OGV, VP8, VP9, AV1, WebM and HEVC videos if they do not exceed the [configured bitrate limit](https://docs.photoprism.app/getting-started/config-options/#file-converters). Special thanks to [Heiko Mathes](https://github.com/heikomat) and [Andre Carrera](https://github.com/acarrera94) for their contributions!

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

- Security: [Upgraded Go to v1.18.3](https://github.com/photoprism/photoprism/commit/942fedf67992ef5eb9d8f371da88aec333a13af0), [which includes TLS and validation fixes](https://github.com/golang/go/issues?q=milestone%3AGo1.18.3)
- MariaDB: [Removed migration that could corrupt photo descriptions in the index](https://github.com/photoprism/photoprism/issues/2398)
- Translations: [Added Arabic](https://github.com/photoprism/photoprism/pull/2417), [updated Danish and Polish](https://github.com/photoprism/photoprism/pull/2413)

### May 28, 2022 ###
<span class="build">Build 220528-efb5d710</span>

This update includes translations that were recently contributed via [translate.photoprism.app](https://translate.photoprism.app/). Missing translations were added by us using DeepL and Google Translate. Native speakers are invited to help improve those if needed. Thank you very much!

- UX: [Mobile toolbar menu has been redesigned](https://dl.photoprism.app/img/ui/mobile-grayscale-submenu.png) and [made accessible in public mode](https://github.com/photoprism/photoprism/issues/2370)
- Themes: [*Gemstone* and *Raspberry* have been updated](https://dl.photoprism.app/img/ui/desktop-gemstone-plus.png)

### May 27, 2022 ###
<span class="build">Build 220527-005770ca</span>

This update improves navigation fonts and [mobile submenu colors](https://dl.photoprism.app/img/ui/mobile-submenu-light-797x567.png) for light themes. We are also working to establish [PhotoPrism+](https://photoprism.app/membership) as the name for our community membership and associated benefits. For this, sponsorship [information in the app](https://try.photoprism.app/library/about), [on our website](https://photoprism.app/membership), on [GitHub Sponsors](https://link.photoprism.app/sponsor) and [Patreon](https://link.photoprism.app/patreon) is gradually being updated.

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

**Thank you to everyone who [helped with testing](https://github.com/photoprism/photoprism/projects/5?card_filter_query=label%3Aplease-test), [signed up as a sponsor](https://photoprism.app/membership), or [contributed](https://github.com/photoprism/photoprism/graphs/contributors) in other ways! We appreciate it very much.**

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
- Config: [Added NVIDIA hardware video transcoding support for sponsors](https://github.com/photoprism/photoprism/issues/2125)
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

- Security: [Upgraded Go to v1.17.5, which includes HTTP/2 and networking fixes](https://groups.google.com/g/golang-announce/c/hcmEScgc00k)
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
now a sponsor feature. We believe this is fair. A big thank you to all our [sponsors](https://link.photoprism.app/sponsors)
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
in particular for UTC. The Docker base image has been upgraded to Ubuntu 21.10, which ships with 
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
- RAW: [Upgraded Darktable to 3.6.0](https://github.com/photoprism/photoprism/issues/1632)
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

- Metadata: [Upgraded Exiftool to fix security issue](https://github.com/photoprism/photoprism/issues/1302)

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

- UI: [Added Yellowstone theme for sponsors, unlocked Grayscale theme for everyone](https://github.com/photoprism/photoprism/commit/180e46b95f52a5ef2d67ea8ac5e1d8a9b08ef970)
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

Even when you use an image with the `:latest` tag, Docker does not automatically download new images for you. To update, you can either [manually pull the most recent image](getting-started/updates.md) and restart, or set up a service like [Watchtower](getting-started/updates.md#watchtower) to get automatic updates.
