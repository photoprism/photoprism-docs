# Config Options #

!!! attention ""
    Changing basic system config options in `docker-compose.yml` or on the [advanced settings](../user-guide/settings/advanced.md) 
    page always requires a restart to take effect. Open a terminal, run `docker-compose stop photoprism` and then
    `docker-compose up -d photoprism` to restart the app container.

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_DEBUG`              | --debug                    | enable debug mode, show additional log messages
`PHOTOPRISM_LOG_LEVEL`          | --log-level value, -l value| trace, debug, info, warning, error, fatal, or panic (default: "info")
`PHOTOPRISM_PUBLIC`             | --public, -p               | disable password authentication
`PHOTOPRISM_ADMIN_PASSWORD`     | --admin-password PASSWORD  | initial admin user PASSWORD, minimum 4 characters
`PHOTOPRISM_READONLY`           | --read-only, -r            | disable import, upload, and delete
`PHOTOPRISM_EXPERIMENTAL`       | --experimental, -e         | enable experimental features
`PHOTOPRISM_CONFIG_FILE`        | --config-file FILENAME, -c FILENAME  | load config values from FILENAME
`PHOTOPRISM_CONFIG_PATH`        | --config-path PATH         | config PATH to be searched for additional configuration and settings files

### Storage Folders ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_ORIGINALS_PATH`     | --originals-path PATH      | original media library PATH containing your photo and video collection
`PHOTOPRISM_ORIGINALS_LIMIT`    | --originals-limit MB       | original media file size limit in MB (default: 1000)
`PHOTOPRISM_IMPORT_PATH`        | --import-path PATH         | optional import PATH from which files can be added to originals
`PHOTOPRISM_STORAGE_PATH`       | --storage-path PATH        | writable storage PATH for cache, database, and sidecar files
`PHOTOPRISM_SIDECAR_PATH`       | --sidecar-path PATH        | optional custom relative or absolute sidecar PATH
`PHOTOPRISM_CACHE_PATH`         | --cache-path PATH          | optional custom cache PATH for sessions and thumbnail files
`PHOTOPRISM_TEMP_PATH`          | --temp-path PATH           | optional custom temporary file PATH
`PHOTOPRISM_BACKUP_PATH`        | --backup-path PATH         | optional custom backup PATH for index backup files
`PHOTOPRISM_ASSETS_PATH`        | --assets-path PATH         | assets PATH containing static resources like icons, models, and translations

### Index Workers ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_WORKERS`            | --workers NUMBER, -w NUMBER | maximum NUMBER of indexing workers, default and limit depend on the number of CPU cores
`PHOTOPRISM_WAKEUP_INTERVAL`    | --wakeup-interval SECONDS  | background worker wakeup interval in SECONDS (default: 900)
`PHOTOPRISM_AUTO_INDEX`         | --auto-index SECONDS       | WebDAV auto indexing safety delay in SECONDS, disable with -1 (default: 300)
`PHOTOPRISM_AUTO_IMPORT`        | --auto-import SECONDS      | WebDAV auto import safety delay in SECONDS, disable with -1 (default: 180)

### Feature Flags ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_DISABLE_WEBDAV`     | --disable-webdav           | disable built-in WebDAV server
`PHOTOPRISM_DISABLE_SETTINGS`   | --disable-settings         | disable settings UI and API
`PHOTOPRISM_DISABLE_PLACES`     | --disable-places           | disable reverse geocoding and map
`PHOTOPRISM_DISABLE_BACKUPS`    | --disable-backups          | disable creating YAML metadata backup files
`PHOTOPRISM_DISABLE_EXIFTOOL`   | --disable-exiftool         | disable creating JSON metadata sidecar files with ExifTool
`PHOTOPRISM_DISABLE_FFMPEG`     | --disable-ffmpeg           | disable video transcoding and still image extraction with FFmpeg
`PHOTOPRISM_DISABLE_DARKTABLE`  | --disable-darktable        | disable converting RAW files with Darktable
`PHOTOPRISM_DISABLE_RAWTHERAPEE`| --disable-rawtherapee      | disable converting RAW files with RawTherapee
`PHOTOPRISM_DISABLE_SIPS`       | --disable-sips             | disable converting RAW files with Sips (macOS only)
`PHOTOPRISM_DISABLE_HEIFCONVERT`| --disable-heifconvert      | disable converting HEIC/HEIF files
`PHOTOPRISM_DISABLE_TENSORFLOW` | --disable-tensorflow       | disable all features depending on TensorFlow
`PHOTOPRISM_DISABLE_FACES`      | --disable-faces            | disable facial recognition
`PHOTOPRISM_DISABLE_CLASSIFICATION`| --disable-classification| disable image classification
`PHOTOPRISM_DETECT_NSFW`        | --detect-nsfw              | flag photos as private that may be offensive (requires TensorFlow)
`PHOTOPRISM_UPLOAD_NSFW`        | --upload-nsfw              | allow uploads that may be offensive

### Web App ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_APP_ICON`           | --app-icon ICON            | application ICON (logo, app, crisp, mint, bold) (default: "logo") |
`PHOTOPRISM_APP_NAME`           | --app-name NAME            | application NAME when installed on a device (default: "PhotoPrism") |
`PHOTOPRISM_APP_MODE`           | --app-mode MODE            | application MODE (fullscreen, standalone, minimal-ui, browser) (default: "standalone") |

### Site Information ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_CDN_URL`            | --cdn-url URL              | optional content delivery network URL
`PHOTOPRISM_SITE_URL`           | --site-url URL             | public site URL (default: "http://localhost:2342/")
`PHOTOPRISM_SITE_AUTHOR`        | --site-author COPYRIGHT        | site COPYRIGHT, artist, or owner name
`PHOTOPRISM_SITE_TITLE`         | --site-title TITLE             | site TITLE (default: "PhotoPrism")
`PHOTOPRISM_SITE_CAPTION`       | --site-caption CAPTION         | site CAPTION (default: "Browse Your Life")
`PHOTOPRISM_SITE_DESCRIPTION`   | --site-description DESCRIPTION | optional site DESCRIPTION
`PHOTOPRISM_SITE_PREVIEW`       | --site-preview URL         | optional preview image URL

### Web Server ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_HTTP_PORT`          | --http-port NUMBER         | http server port NUMBER (default: 2342)
`PHOTOPRISM_HTTP_HOST`          | --http-host IP             | http server IP address
`PHOTOPRISM_HTTP_MODE`          | --http-mode MODE, -m MODE| http server MODE (debug, release, or test)
`PHOTOPRISM_HTTP_COMPRESSION`   | --http-compression METHOD, -z METHOD | http server compression METHOD (none or gzip)

### Database Connection ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_DATABASE_DRIVER`    | --database-driver NAME     | database DRIVER (sqlite or mysql) (default: "sqlite")
`PHOTOPRISM_DATABASE_DSN`       | --database-dsn DSN         | sqlite file name, providing a DSN is optional for other drivers
`PHOTOPRISM_DATABASE_SERVER`    | --database-server HOST     | database server HOST with optional port e.g. mysql:3306
`PHOTOPRISM_DATABASE_NAME`      | --database-name NAME       | database schema NAME (default: "photoprism")
`PHOTOPRISM_DATABASE_USER`      | --database-user NAME       | database user NAME (default: "photoprism")
`PHOTOPRISM_DATABASE_PASSWORD`  | --database-password PASSWORD | database user PASSWORD
`PHOTOPRISM_DATABASE_CONNS`     | --database-conns NUMBER    | maximum NUMBER of open database connections
`PHOTOPRISM_DATABASE_CONNS_IDLE`| --database-conns-idle NUMBER | maximum NUMBER of idle database connections

### External Tools ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_RAW_PRESETS`        | --raw-presets              | enable RAW file converter presets (may reduce performance)
`PHOTOPRISM_DARKTABLE_BIN`      | --darktable-bin COMMAND    | Darktable CLI COMMAND for RAW file conversion (default: "darktable-cli")
`PHOTOPRISM_DARKTABLE_BLACKLIST` | --darktable-blacklist BLACKLIST | file EXTENSIONS not to be converted with Darktable (default: "raf,cr3,dng")
`PHOTOPRISM_RAWTHERAPEE_BIN`    | --rawtherapee-bin COMMAND  | RawTherapee CLI COMMAND for RAW file conversion (default: "rawtherapee-cli")
`PHOTOPRISM_RAWTHERAPEE_BLACKLIST` | --rawtherapee-blacklist BLACKLIST | file EXTENSIONS not to be converted with RawTherapee
`PHOTOPRISM_SIPS_BIN`           | --sips-bin FILENAME        | Sips COMMAND for RAW file conversion (macOS only) (default: "sips")
`PHOTOPRISM_HEIFCONVERT_BIN`    | --heifconvert-bin COMMAND  | HEIC/HEIF image convert COMMAND (default: "heif-convert")
`PHOTOPRISM_FFMPEG_BIN`         | --ffmpeg-bin COMMAND       | FFmpeg COMMAND for video transcoding and still image extraction (default: "ffmpeg")
`PHOTOPRISM_FFMPEG_ENCODER`     | --ffmpeg-encoder NAME      | maximum FFmpeg encoding BITRATE (Mbit/s) (default: 50)
`PHOTOPRISM_FFMPEG_BITRATE`     | --ffmpeg-bitrate LIMIT     | FFmpeg encoding bitrate LIMIT in Mbit/s (default: "50")
`PHOTOPRISM_FFMPEG_BUFFERS`     | --ffmpeg-buffers           | NUMBER of FFmpeg capture buffers (default: 32)
`PHOTOPRISM_EXIFTOOL_BIN`       | --exiftool-bin COMMAND     | ExifTool COMMAND for extracting metadata (default: "exiftool")

### Images ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_DOWNLOAD_TOKEN`     | --download-token TOKEN     | custom download URL TOKEN (default: random)
`PHOTOPRISM_PREVIEW_TOKEN`      | --preview-token TOKEN      | custom thumbnail and streaming URL TOKEN (default: random)
`PHOTOPRISM_THUMB_FILTER`       | --thumb-filter FILTER, -f FILTER | thumbnail downscaling FILTER (best to worst: blackman, lanczos, cubic, linear) (default: "lanczos")
`PHOTOPRISM_THUMB_SIZE`         | --thumb-size PIXELS, -s PIXELS | maximum pre-cached thumbnail image size in PIXELS (720-7680) (default: 2048)
`PHOTOPRISM_THUMB_UNCACHED`     | --thumb-uncached, -u       | enable on-demand thumbnail generation (high memory and cpu usage)
`PHOTOPRISM_THUMB_SIZE_UNCACHED`| --thumb-size-uncached PIXELS, -x PIXELS | maximum size of on-demand generated thumbnails in PIXELS (720-7680) (default: 7680)
`PHOTOPRISM_JPEG_SIZE`          | --jpeg-size PIXELS         | maximum size of generated JPEG images in PIXELS (720-30000) (default: 7680)
`PHOTOPRISM_JPEG_QUALITY`       | --jpeg-quality QUALITY, -q QUALITY | QUALITY of generated JPEG images, a higher value reduces compression (25-100) (default: 92)

### Facial Recognition ###

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_FACE_SIZE`          | --face-size PIXELS         | minimum face size in PIXELS (default: 50)
`PHOTOPRISM_FACE_SCORE`         | --face-score QUALITY       | minimum face QUALITY score (default: 9)
`PHOTOPRISM_FACE_OVERLAP`       | --face-overlap PERCENT      | face area overlap threshold in PERCENT (default: 42)
`PHOTOPRISM_FACE_CLUSTER_SIZE`  | --face-cluster-size PIXELS      | minimum size of automatically clustered faces in PIXELS (default: 80)
`PHOTOPRISM_FACE_CLUSTER_SCORE` | --face-cluster-score QUALITY  | minimum QUALITY score of automatically clustered faces (default: 15)
`PHOTOPRISM_FACE_CLUSTER_CORE`  | --face-cluster-core NUMBER | NUMBER of faces forming a cluster core (default: 4)
`PHOTOPRISM_FACE_CLUSTER_DIST`  | --face-cluster-dist DISTANCE | similarity DISTANCE of faces forming a cluster core (default: 0.64)
`PHOTOPRISM_FACE_MATCH_DIST`    | --face-match-dist OFFSET   | similarity OFFSET for matching faces with existing clusters (default: 0.46)

### Daemon Mode ###

If you start the server in the background (daemon mode), you can additionally specify a log and process id filename:

Variable                        | Parameter                  | Description
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_PID_FILENAME`       | --pid-filename FILENAME    | process id FILENAME (daemon mode only)
`PHOTOPRISM_LOG_FILENAME`       | --log-filename FILENAME    | server log FILENAME (daemon mode only)
