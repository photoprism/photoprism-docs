# Config Options #

!!! tldr ""
    Changing values in `docker-compose.yml` or in [Advanced Settings](../user-guide/settings/advanced.md) 
    always **requires a restart** to take effect. Open a terminal, run `docker-compose stop` and then
    `docker-compose up -d` to restart all services.

### Authentication ###

|         Variable          |        Flag        |                                     Usage                                      |
|---------------------------|--------------------|--------------------------------------------------------------------------------|
| PHOTOPRISM_ADMIN_PASSWORD | admin-password, pw | initial admin `PASSWORD`, must have at least 8 characters                      |
| PHOTOPRISM_PUBLIC         | public, p          | disable password authentication, WebDAV, and the advanced settings page        |
| PHOTOPRISM_AUTH           | auth, a            | always require password authentication, overrides the public flag if it is set |

### Logging ###

|       Variable       |     Flag     |                                      Usage                                       |
|----------------------|--------------|----------------------------------------------------------------------------------|
| PHOTOPRISM_LOG_LEVEL | log-level, l | log message verbosity `LEVEL` (trace, debug, info, warning, error, fatal, panic) |
| PHOTOPRISM_DEBUG     | debug        | enable debug mode, show non-essential log messages                               |
| PHOTOPRISM_TRACE     | trace        | enable trace mode, show all log messages                                         |

### Storage ###

|          Variable           |         Flag         |                                                Usage                                                 |
|-----------------------------|----------------------|------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_CONFIG_PATH      | config-path, c       | config storage `PATH`, values in options.yml override CLI flags and environment variables if present |
| PHOTOPRISM_DEFAULTS_YAML    | defaults-yaml, y     | load config defaults from `FILE` if exists, does not override CLI flags and environment variables    |
| PHOTOPRISM_ORIGINALS_PATH   | originals-path, o    | storage `PATH` of your original media files (photos and videos)                                      |
| PHOTOPRISM_ORIGINALS_LIMIT  | originals-limit, mb  | maximum size of media files in `MB` (1-100000; -1 to disable)                                        |
| PHOTOPRISM_RESOLUTION_LIMIT | resolution-limit, mp | maximum resolution of media files in `MEGAPIXELS` (1-900; -1 to disable) *sponsors only*             |
| PHOTOPRISM_STORAGE_PATH     | storage-path, s      | writable storage `PATH` for sidecar, cache, and database files                                       |
| PHOTOPRISM_SIDECAR_PATH     | sidecar-path, sc     | custom relative or absolute sidecar `PATH` (optional)                                                |
| PHOTOPRISM_BACKUP_PATH      | backup-path, ba      | custom backup `PATH` for index backup files (optional)                                               |
| PHOTOPRISM_CACHE_PATH       | cache-path, ca       | custom cache `PATH` for sessions and thumbnail files (optional)                                      |
| PHOTOPRISM_IMPORT_PATH      | import-path, im      | base `PATH` from which files can be imported to originals (optional)                                 |
| PHOTOPRISM_ASSETS_PATH      | assets-path, as      | assets `PATH` containing static resources like icons, models, and translations                       |
| PHOTOPRISM_TEMP_PATH        | temp-path, tmp       | temporary file `PATH` (optional)                                                                     |

### Index Workers ###

|          Variable          |        Flag        |                                             Usage                                             |
|----------------------------|--------------------|-----------------------------------------------------------------------------------------------|
| PHOTOPRISM_WORKERS         | workers, w         | maximum `NUMBER` of indexing workers, default depends on the number of physical cores         |
| PHOTOPRISM_WAKEUP_INTERVAL | wakeup-interval, i | `DURATION` between worker runs required for face recognition and index maintenance (1-86400s) |
| PHOTOPRISM_AUTO_INDEX      | auto-index         | WebDAV auto index safety delay in `SECONDS` (-1 to disable)                                   |
| PHOTOPRISM_AUTO_IMPORT     | auto-import        | WebDAV auto import safety delay in `SECONDS` (-1 to disable)                                  |

### Feature Flags ###

|             Variable              |          Flag          |                                          Usage                                          |
|-----------------------------------|------------------------|-----------------------------------------------------------------------------------------|
| PHOTOPRISM_READONLY               | read-only, r           | disable import, upload, delete, and all other operations that require write permissions |
| PHOTOPRISM_EXPERIMENTAL           | experimental, e        | enable experimental features                                                            |
| PHOTOPRISM_DISABLE_WEBDAV         | disable-webdav         | disable built-in WebDAV server                                                          |
| PHOTOPRISM_DISABLE_SETTINGS       | disable-settings       | disable settings UI and API                                                             |
| PHOTOPRISM_DISABLE_PLACES         | disable-places         | disable reverse geocoding and maps                                                      |
| PHOTOPRISM_DISABLE_BACKUPS        | disable-backups        | disable backing up albums and photo metadata to YAML files                              |
| PHOTOPRISM_DISABLE_TENSORFLOW     | disable-tensorflow     | disable all features depending on TensorFlow                                            |
| PHOTOPRISM_DISABLE_FACES          | disable-faces          | disable facial recognition                                                              |
| PHOTOPRISM_DISABLE_CLASSIFICATION | disable-classification | disable image classification                                                            |
| PHOTOPRISM_DISABLE_FFMPEG         | disable-ffmpeg         | disable video transcoding and thumbnail extraction with FFmpeg                          |
| PHOTOPRISM_DISABLE_EXIFTOOL       | disable-exiftool       | disable creating JSON metadata sidecar files with ExifTool                              |
| PHOTOPRISM_DISABLE_HEIFCONVERT    | disable-heifconvert    | disable conversion of HEIC/HEIF files                                                   |
| PHOTOPRISM_DISABLE_DARKTABLE      | disable-darktable      | disable conversion of RAW files with Darktable                                          |
| PHOTOPRISM_DISABLE_RAWTHERAPEE    | disable-rawtherapee    | disable conversion of RAW files with RawTherapee                                        |
| PHOTOPRISM_DISABLE_SIPS           | disable-sips           | disable conversion of RAW files with Sips *macOS only*                                  |
| PHOTOPRISM_DISABLE_RAW            | disable-raw            | disable indexing and conversion of RAW files                                            |
| PHOTOPRISM_RAW_PRESETS            | raw-presets            | enables applying user presets when converting RAW files (reduces performance)           |
| PHOTOPRISM_EXIF_BRUTEFORCE        | exif-bruteforce        | always perform a brute-force search if no Exif headers were found                       |
| PHOTOPRISM_DETECT_NSFW            | detect-nsfw            | flag photos as private that may be offensive (requires TensorFlow)                      |
| PHOTOPRISM_UPLOAD_NSFW            | upload-nsfw, n         | allow uploads that may be offensive                                                     |
| PHOTOPRISM_DEFAULT_LOCALE         | default-locale, lang   | standard user interface language `CODE`                                                 |

### Customization ###

|         Variable         |     Flag      |                             Usage                             |
|--------------------------|---------------|---------------------------------------------------------------|
| PHOTOPRISM_DEFAULT_THEME | default-theme | standard user interface theme `NAME` *sponsors only*          |
| PHOTOPRISM_APP_ICON      | app-icon      | web app `ICON` (logo, app, crisp, mint, bold) *sponsors only* |
| PHOTOPRISM_APP_NAME      | app-name      | web app `NAME` when installed on a device *sponsors only*     |
| PHOTOPRISM_APP_MODE      | app-mode      | web app `MODE` (fullscreen, standalone, minimal-ui, browser)  |

### Site Information ###

|          Variable           |       Flag       |                           Usage                            |
|-----------------------------|------------------|------------------------------------------------------------|
| PHOTOPRISM_CDN_URL          | cdn-url          | content delivery network `URL` *sponsors only*             |
| PHOTOPRISM_SITE_URL         | site-url, url    | public site `URL`                                          |
| PHOTOPRISM_SITE_AUTHOR      | site-author      | site `OWNER`, copyright, or artist                         |
| PHOTOPRISM_SITE_TITLE       | site-title       | site `TITLE` *sponsors only*                               |
| PHOTOPRISM_SITE_CAPTION     | site-caption     | site `CAPTION`                                             |
| PHOTOPRISM_SITE_DESCRIPTION | site-description | site `DESCRIPTION` (optional)                              |
| PHOTOPRISM_SITE_PREVIEW     | site-preview     | site preview image `URL` (optional) *sponsors only*        |
| PHOTOPRISM_IMPRINT          | imprint          | legal `INFO`, displayed in the page footer *sponsors only* |
| PHOTOPRISM_IMPRINT_URL      | imprint-url      | optional legal info `URL` *sponsors only*                  |

### Web Server ###

|          Variable           |        Flag         |                      Usage                      |
|-----------------------------|---------------------|-------------------------------------------------|
| PHOTOPRISM_HTTP_PORT        | http-port, port     | http server port `NUMBER`                       |
| PHOTOPRISM_HTTP_HOST        | http-host, ip       | http server `IP` address                        |
| PHOTOPRISM_HTTP_MODE        | http-mode, mode     | http server `MODE` (debug, release, or test)    |
| PHOTOPRISM_HTTP_COMPRESSION | http-compression, z | http server compression `METHOD` (none or gzip) |

### Database Connection ###

|            Variable            |            Flag            |                              Usage                              |
|--------------------------------|----------------------------|-----------------------------------------------------------------|
| PHOTOPRISM_DATABASE_DRIVER     | database-driver, db        | database `DRIVER` (sqlite, mysql)                               |
| PHOTOPRISM_DATABASE_DSN        | database-dsn, dsn          | database connection `DSN` (sqlite file, optional for mysql)     |
| PHOTOPRISM_DATABASE_SERVER     | database-server, db-server | database `HOST` incl. port e.g. "mariadb:3306" (or socket path) |
| PHOTOPRISM_DATABASE_NAME       | database-name, db-name     | database schema `NAME`                                          |
| PHOTOPRISM_DATABASE_USER       | database-user, db-user     | database user `NAME`                                            |
| PHOTOPRISM_DATABASE_PASSWORD   | database-password, db-pass | database user `PASSWORD`                                        |
| PHOTOPRISM_DATABASE_CONNS      | database-conns             | maximum `NUMBER` of open database connections                   |
| PHOTOPRISM_DATABASE_CONNS_IDLE | database-conns-idle        | maximum `NUMBER` of idle database connections                   |

### File Converters ###

|             Variable             |         Flag          |                              Usage                              |
|----------------------------------|-----------------------|-----------------------------------------------------------------|
| PHOTOPRISM_DARKTABLE_BIN         | darktable-bin         | Darktable CLI `COMMAND` for RAW to JPEG conversion              |
| PHOTOPRISM_DARKTABLE_BLACKLIST   | darktable-blacklist   | do not use Darktable to convert files with these `EXTENSIONS`   |
| PHOTOPRISM_DARKTABLE_CACHE_PATH  | darktable-cache-path  | custom Darktable cache `PATH`                                   |
| PHOTOPRISM_DARKTABLE_CONFIG_PATH | darktable-config-path | custom Darktable config `PATH`                                  |
| PHOTOPRISM_RAWTHERAPEE_BIN       | rawtherapee-bin       | RawTherapee CLI `COMMAND` for RAW to JPEG conversion            |
| PHOTOPRISM_RAWTHERAPEE_BLACKLIST | rawtherapee-blacklist | do not use RawTherapee to convert files with these `EXTENSIONS` |
| PHOTOPRISM_SIPS_BIN              | sips-bin              | Sips `COMMAND` for RAW to JPEG conversion *macOS only*          |
| PHOTOPRISM_HEIFCONVERT_BIN       | heifconvert-bin       | HEIC/HEIF image conversion `COMMAND`                            |
| PHOTOPRISM_FFMPEG_BIN            | ffmpeg-bin            | FFmpeg `COMMAND` for video transcoding and thumbnail extraction |
| PHOTOPRISM_FFMPEG_ENCODER        | ffmpeg-encoder, vc    | FFmpeg AVC encoder `NAME` *sponsors only*                       |
| PHOTOPRISM_FFMPEG_BITRATE        | ffmpeg-bitrate, vb    | maximum FFmpeg encoding `BITRATE` (Mbit/s)                      |
| PHOTOPRISM_EXIFTOOL_BIN          | exiftool-bin          | ExifTool `COMMAND` for extracting metadata                      |

### Security Tokens ###

|         Variable          |      Flag      |                               Usage                                |
|---------------------------|----------------|--------------------------------------------------------------------|
| PHOTOPRISM_DOWNLOAD_TOKEN | download-token | `SECRET` download URL token for originals (default: random)        |
| PHOTOPRISM_PREVIEW_TOKEN  | preview-token  | `SECRET` thumbnail and video streaming URL token (default: random) |
| PHOTOPRISM_THUMB_COLOR    | thumb-color    | standard color `PROFILE` for thumbnails (leave blank to disable)   |

### Image Quality ###

|            Variable            |         Flag         |                                            Usage                                            |
|--------------------------------|----------------------|---------------------------------------------------------------------------------------------|
| PHOTOPRISM_THUMB_FILTER        | thumb-filter, filter | image downscaling filter `NAME` (best to worst: blackman, lanczos, cubic, linear)           |
| PHOTOPRISM_THUMB_SIZE          | thumb-size           | maximum size of thumbnails created during indexing in `PIXELS` (720-7680)                   |
| PHOTOPRISM_THUMB_SIZE_UNCACHED | thumb-size-uncached  | maximum size of missing thumbnails created on demand in `PIXELS` (720-7680)                 |
| PHOTOPRISM_THUMB_UNCACHED      | thumb-uncached, u    | enable on-demand creation of missing thumbnails (high memory and cpu usage)                 |
| PHOTOPRISM_JPEG_QUALITY        | jpeg-quality, q      | `QUALITY` of created JPEG sidecars and thumbnails (25-100, best, high, default, low, worst) |
| PHOTOPRISM_JPEG_SIZE           | jpeg-size            | maximum size of created JPEG sidecar files in `PIXELS` (720-30000)                          |

### Face Recognition ###

!!! info ""    
    To [recognize faces](../user-guide/organize/people.md), PhotoPrism first extracts crops from your images using a
    [library](https://github.com/esimov/pigo) based on [pixel intensity comparisons](https://arxiv.org/pdf/1305.4537.pdf).
    These are then fed into TensorFlow to compute [512-dimensional vectors](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Schroff_FaceNet_A_Unified_2015_CVPR_paper.pdf)
    for characterization. In the final step, the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN)
    attempts to cluster these so-called face embeddings, so they can be matched to persons with just a few clicks.
    A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher
    value being more aggressive and leading to larger clusters with more false positives.
    To cluster a smaller number of faces, you can reduce the core to 3 or 2 similar faces.

We recommend that only advanced users change these parameters:

|           Variable            |        Flag        |                                          Usage                                          |
|-------------------------------|--------------------|-----------------------------------------------------------------------------------------|
| PHOTOPRISM_FACE_SIZE          | face-size          | minimum size of faces in `PIXELS` (20-10000)                                            |
| PHOTOPRISM_FACE_SCORE         | face-score         | minimum face `QUALITY` score (1-100)                                                    |
| PHOTOPRISM_FACE_OVERLAP       | face-overlap       | face area overlap threshold in `PERCENT` (1-100)                                        |
| PHOTOPRISM_FACE_CLUSTER_SIZE  | face-cluster-size  | minimum size of automatically clustered faces in `PIXELS` (20-10000) *sponsors only*    |
| PHOTOPRISM_FACE_CLUSTER_SCORE | face-cluster-score | minimum `QUALITY` score of automatically clustered faces (1-100) *sponsors only*        |
| PHOTOPRISM_FACE_CLUSTER_CORE  | face-cluster-core  | `NUMBER` of faces forming a cluster core (1-100) *sponsors only*                        |
| PHOTOPRISM_FACE_CLUSTER_DIST  | face-cluster-dist  | similarity `DISTANCE` of faces forming a cluster core (0.1-1.5) *sponsors only*         |
| PHOTOPRISM_FACE_MATCH_DIST    | face-match-dist    | similarity `OFFSET` for matching faces with existing clusters (0.1-1.5) *sponsors only* |

### Daemon Mode ###

If you start the server as a *daemon* in the background, you can additionally specify a filename for the log and the process ID:

|        Variable         |     Flag     |                Usage                 |
|-------------------------|--------------|--------------------------------------|
| PHOTOPRISM_PID_FILENAME | pid-filename | process id `FILE` *daemon-mode only* |
| PHOTOPRISM_LOG_FILENAME | log-filename | server log `FILE` *daemon-mode only* |