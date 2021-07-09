Variable                        | Parameter                  | Description                                  
:------------------------------ |:-------------------------- |:-------------------------------------------
`PHOTOPRISM_DEBUG`              | --debug                    | run in debug mode, shows additional log messages
`PHOTOPRISM_PUBLIC`             | --public, -p               | no authentication required, disables password protection
`PHOTOPRISM_READONLY`           | --read-only, -r            | don't modify originals folder; disables import, upload, and delete
`PHOTOPRISM_EXPERIMENTAL`       | --experimental, -e         | enable experimental features
`PHOTOPRISM_ADMIN_PASSWORD`     | --admin-password PASSWORD  | initial admin PASSWORD, min 4 characters
`PHOTOPRISM_CONFIG_FILE`        | --config-file FILENAME, -c FILENAME  | load initial config options from FILENAME
`PHOTOPRISM_CONFIG_PATH`        | --config-path PATH         | folder containing application settings
`PHOTOPRISM_ORIGINALS_PATH`     | --originals-path PATH      | originals PATH containing your photo and video collection
`PHOTOPRISM_ORIGINALS_LIMIT`    | --originals-limit MB       | file size limit for originals in MB (default: 1000)
`PHOTOPRISM_IMPORT_PATH`        | --import-path PATH         | optional PATH for importing files to originals
`PHOTOPRISM_STORAGE_PATH`       | --storage-path PATH        | storage PATH for cache, database and sidecar files
`PHOTOPRISM_SIDECAR_PATH`       | --sidecar-path PATH        | relative or absolute storage PATH for sidecar files
`PHOTOPRISM_CACHE_PATH`         | --cache-path PATH          | cache storage PATH for sessions and thumbnails
`PHOTOPRISM_TEMP_PATH`          | --temp-path PATH           | temporary PATH for storing uploads and downloads
`PHOTOPRISM_BACKUP_PATH`        | --backup-path PATH         | backup storage PATH
`PHOTOPRISM_ASSETS_PATH`        | --assets-path PATH         | assets PATH for static resources like models and templates
`PHOTOPRISM_WORKERS`            | --workers MAX, -w MAX      | adjusts MAX number of indexing workers
`PHOTOPRISM_WAKEUP_INTERVAL`    | --wakeup-interval SECONDS  | background worker wakeup interval in SECONDS
`PHOTOPRISM_AUTO_INDEX`         | --auto-index SECONDS       | auto indexing safety delay in SECONDS (WebDAV)
`PHOTOPRISM_AUTO_IMPORT`        | --auto-import SECONDS      | auto importing safety delay in SECONDS (WebDAV)
`PHOTOPRISM_DISABLE_BACKUPS`    | --disable-backups          | don't backup photo and album metadata to YAML files
`PHOTOPRISM_DISABLE_WEBDAV`     | --disable-webdav           | disable built-in WebDAV server
`PHOTOPRISM_DISABLE_SETTINGS`   | --disable-settings         | users can not view or change settings
`PHOTOPRISM_DISABLE_PLACES`     | --disable-places           | disables reverse geocoding and map
`PHOTOPRISM_DISABLE_EXIFTOOL`   | --disable-exiftool         | don't create ExifTool JSON files for enhanced metadata extraction
`PHOTOPRISM_DISABLE_TENSORFLOW` | --disable-tensorflow       | don't use TensorFlow for image classification
`PHOTOPRISM_DISABLE_DARKTABLE`  | --disable-darktable        | don't use Darktable to convert RAW files
`PHOTOPRISM_DISABLE_RAWTHERAPEE`| --disable-rawtherapee      | don't use RawTherapee to convert RAW files
`PHOTOPRISM_DISABLE_SIPS`       | --disable-sip              | don't use Sips to convert RAW files on macOS
`PHOTOPRISM_DISABLE_HEIFCONVERT`| --disable-heifconvert      | don't convert HEIC/HEIF files
`PHOTOPRISM_DISABLE_FFMPEG`     | --disable-ffmpeg           | don't transcode videos with FFmpeg
`PHOTOPRISM_DETECT_NSFW`        | --detect-nsfw              | flag photos as private that may be offensive
`PHOTOPRISM_UPLOAD_NSFW`        | --upload-nsfw              | allow uploads that may be offensive
`PHOTOPRISM_LOG_LEVEL`          | --log-level value, -l value| trace, debug, info, warning, error, fatal or panic (default: "info")
`PHOTOPRISM_LOG_FILENAME`       | --log-filename value       | server log FILENAME
`PHOTOPRISM_PID_FILENAME`       | --pid-filename value       | server process id FILENAME
`PHOTOPRISM_CDN_URL`            | --cdn-url URL              | content delivery network URL (optional)
`PHOTOPRISM_SITE_URL`           | --site-url URL             | public site URL (default: "http://localhost:2342/")
`PHOTOPRISM_SITE_PREVIEW`       | --site-preview URL         | public preview image URL
`PHOTOPRISM_SITE_TITLE`         | --site-title value         | site title (default: "PhotoPrism")
`PHOTOPRISM_SITE_CAPTION`       | --site-caption value       | short site caption (default: "Browse Your Life")
`PHOTOPRISM_SITE_DESCRIPTION`   | --site-description value   | long site description
`PHOTOPRISM_SITE_AUTHOR`        | --site-author value        | site artist or copyright
`PHOTOPRISM_HTTP_PORT`          | --http-port NUMBER         | http server port NUMBER (default: 2342)
`PHOTOPRISM_HTTP_HOST`          | --http-host IP             | http server IP address
`PHOTOPRISM_HTTP_MODE`          | --http-mode value, -m value| debug, release or test
`PHOTOPRISM_HTTP_COMPRESSION`   | --http-compression value, -z value | improves transfer speed and bandwidth utilization (none or gzip)
`PHOTOPRISM_DATABASE_DRIVER`    | --database-driver NAME     | database driver NAME (sqlite or mysql) (default: "sqlite")
`PHOTOPRISM_DATABASE_DSN`       | --database-dsn DSN         | sqlite file name, specifying a DSN is optional for mariadb and mysql
`PHOTOPRISM_DATABASE_SERVER`    | --database-server HOST     | database server HOST, specifying a :port is optional
`PHOTOPRISM_DATABASE_NAME`      | --database-name NAME       | database schema NAME (default: "photoprism")
`PHOTOPRISM_DATABASE_USER`      | --database-user NAME       | database user NAME (default: "photoprism")
`PHOTOPRISM_DATABASE_PASSWORD`  | --database-password PASSWORD | database user PASSWORD
`PHOTOPRISM_DATABASE_CONNS`     | --database-conns NUMBER    | max NUMBER of open connections to the database (default: 0)
`PHOTOPRISM_DATABASE_CONNS_IDLE`| --database-conns-idle NUMBER | max NUMBER of idle connections (equal or less than open) (default: 0)
`PHOTOPRISM_RAWTHERAPEE_BIN`    | --rawtherapee-bin COMMAND  | RawTherapee CLI COMMAND for raw image conversion (default: "rawtherapee-cli")
`PHOTOPRISM_DARKTABLE_BIN`      | --darktable-bin COMMAND    | Darktable CLI COMMAND for raw image conversion (default: "darktable-cli")
`PHOTOPRISM_RAW_PRESETS`        | --raw-presets              | enables RAW converter presets (may reduce performance)
`PHOTOPRISM_SIPS_BIN`           | --sips-bin FILENAME        | Scriptable Image Processing System COMMAND (default: "sips")
`PHOTOPRISM_HEIFCONVERT_BIN`    | --heifconvert-bin COMMAND  | HEIC/HEIF image convert COMMAND (default: "heif-convert")
`PHOTOPRISM_FFMPEG_BIN`         | --ffmpeg-bin COMMAND       | FFmpeg COMMAND for video transcoding and cover images (default: "ffmpeg")
`PHOTOPRISM_FFMPEG_ENCODER`     | --ffmpeg-encoder NAME      | FFmpeg AVC encoder NAME (default: "libx264")
`PHOTOPRISM_FFMPEG_BITRATE`     | --ffmpeg-bitrate LIMIT     | FFmpeg encoding bitrate LIMIT in Mbit/s (default: "50")
`PHOTOPRISM_FFMPEG_BUFFERS`     | --ffmpeg-buffers           | FFmpeg capture buffers (default: "532")
`PHOTOPRISM_EXIFTOOL_BIN`       | --exiftool-bin COMMAND     | ExifTool COMMAND for enhanced metadata extraction (default: "exiftool")
`PHOTOPRISM_DOWNLOAD_TOKEN`     | --download-token SECRET    | optional static SECRET url token for file downloads
`PHOTOPRISM_PREVIEW_TOKEN`      | --preview-token SECRET     | optional static SECRET url token for preview images and video streaming
`PHOTOPRISM_THUMB_FILTER`       | --thumb-filter NAME, -f NAME | downscaling filter NAME (best to worst: blackman, lanczos, cubic, linear) (default: "lanczos")
`PHOTOPRISM_THUMB_SIZE`         | --thumb-size PIXELS, -s PIXELS | static thumbnail size limit in PIXELS (720-7680) (default: 2048)
`PHOTOPRISM_THUMB_UNCACHED`     | --thumb-uncached, -u       | enable dynamic thumbnail rendering (high memory and cpu usage if thumbnails haven't been generated yet)
`PHOTOPRISM_THUMB_SIZE_UNCACHED`| --thumb-size-uncached PIXELS, -x PIXELS | dynamic rendering size limit in PIXELS (720-7680) (default: 7680)
`PHOTOPRISM_JPEG_SIZE`          | --jpeg-size PIXELS         | size limit for converted image files in PIXELS (720-30000) (default: 7680
`PHOTOPRISM_JPEG_QUALITY`       | --jpeg-quality value, -q value | choose 95 for high-quality thumbnails (25-100) (default: 92)
