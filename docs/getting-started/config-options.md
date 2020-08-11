Environment Variable       | Parameter            | Description                                  
:------------------------- |:-------------------- |:-------------------------------------------
`PHOTOPRISM_DEBUG`         | --debug              | run in debug mode (shows additional log messages)
`PHOTOPRISM_PUBLIC`        | --public, -p         | no authentication required (disables password protection)
`PHOTOPRISM_READONLY`      | --read-only, -r      | don't modify originals directory (import and upload disabled)
`PHOTOPRISM_TENSORFLOW_OFF` | --tf-off           | don't use TensorFlow for image classification (or anything else)
`PHOTOPRISM_EXPERIMENTAL`  | --experimental, -e   | enable experimental features
`PHOTOPRISM_ADMIN_PASSWORD` | --admin-password value  | initial admin password (can be changed in settings)
`PHOTOPRISM_WORKERS`       | --workers value, -w value | number of workers for indexing (default: 0)
`PHOTOPRISM_WAKEUP_INTERVAL` | --wakeup-interval value  |  background worker wakeup interval in seconds (default: 0)
`PHOTOPRISM_SITE_URL`      | --site-url URL       | public site URL (default: "http://localhost:2342/")
`PHOTOPRISM_SITE_PREVIEW`  | --site-preview URL   | public preview image URL
`PHOTOPRISM_SITE_TITLE`    | --site-title value   | site title (default: "PhotoPrism")
`PHOTOPRISM_SITE_CAPTION`  | --site-caption value | short site caption (default: "Browse Your Life")
`PHOTOPRISM_SITE_DESCRIPTION` |  --site-description value | long site description
`PHOTOPRISM_SITE_AUTHOR`   | --site-author value | site artist or copyright
`PHOTOPRISM_HTTP_PORT`     | --http-port NUMBER | http server port NUMBER (default: 2342)
`PHOTOPRISM_HTTP_HOST`     | --http-host IP     | http server IP address
`PHOTOPRISM_HTTP_MODE`     | --http-mode value, -m value  | debug, release or test
`PHOTOPRISM_DATABASE_DRIVER` | --database-driver NAME    | database driver NAME (sqlite or mysql) (default: "sqlite")
`PHOTOPRISM_DATABASE_DSN`  | --database-dsn DSN           | data source or file name (DSN)
`PHOTOPRISM_DATABASE_CONNS` | --database-conns NUMBER    | max NUMBER of open connections to the database (default: 0)
`PHOTOPRISM_DATABASE_CONNS_IDLE` |   --database-conns-idle NUMBER  | max NUMBER of idle connections (equal or less than open) (default: 0)
`PHOTOPRISM_ASSETS_PATH`   | --assets-path PATH                     | assets PATH for static files like templates and TensorFlow models
`PHOTOPRISM_STORAGE_PATH`  | --storage-path PATH                    | storage PATH for generated files like cache and index
`PHOTOPRISM_IMPORT_PATH`   | --import-path PATH                     | optional import PATH for copying files to originals
`PHOTOPRISM_ORIGINALS_PATH` | --originals-path PATH                 | originals PATH for photo, video and sidecar files
`PHOTOPRISM_ORIGINALS_LIMIT` |   --originals-limit MEGABYTE         | file size limit for originals in MEGABYTE (default: 1000)
`PHOTOPRISM_LOG_LEVEL`     | --log-level value, -l value            | trace, debug, info, warning, error, fatal or panic (default: "info")
`PHOTOPRISM_LOG_FILENAME`  | --log-filename value                   | filename for storing server logs
`PHOTOPRISM_PID_FILENAME`  | --pid-filename value                   | filename for the server process id (pid)
`PHOTOPRISM_CACHE_PATH`    | --cache-path PATH                      | cache PATH
`PHOTOPRISM_TEMP_PATH`     | --temp-path PATH                       | temporary PATH for uploads and downloads
`PHOTOPRISM_CONFIG_FILE`   | --config-file FILENAME, -c FILENAME    | load configuration from FILENAME
`PHOTOPRISM_SETTINGS_PATH` | --settings-path PATH                   | settings PATH
`PHOTOPRISM_SETTINGS_HIDDEN` | --settings-hidden                    | users can not view or change settings
`PHOTOPRISM_DARKTABLE_BIN` | --darktable-bin FILENAME               | darktable-cli executable FILENAME (default: "darktable-cli")
`PHOTOPRISM_DARKTABLE_PRESETS` | --darktable-presets                | use darktable presets (disables concurrent raw to jpeg conversion)
`PHOTOPRISM_SIPS_BIN`      | --sips-bin FILENAME                    | sips executable FILENAME (default: "sips")
`PHOTOPRISM_HEIFCONVERT_BIN` | --heifconvert-bin FILENAME           | heif-convert executable FILENAME (default: "heif-convert")
`PHOTOPRISM_FFMPEG_BIN`    | --ffmpeg-bin FILENAME                  | ffmpeg executable FILENAME (default: "ffmpeg")
`PHOTOPRISM_EXIFTOOL_BIN`  | --exiftool-bin FILENAME                | exiftool executable FILENAME (default: "exiftool")
`PHOTOPRISM_SIDECAR_JSON`  | --sidecar-json, -j                     | read metadata from JSON sidecar files created by exiftool
`PHOTOPRISM_SIDECAR_YAML`  | --sidecar-yaml, -y                     | backup photo metadata to YAML sidecar files 
`PHOTOPRISM_SIDECAR_HIDDEN` | --sidecar-hidden                      | create JSON and YAML sidecar files in .photoprism if enabled
`PHOTOPRISM_SIDECAR_PATH`  | --sidecar-path PATH                    | storage PATH for automatically created sidecar files (relative or absolute)
`PHOTOPRISM_DETECT_NSFW`   | --detect-nsfw                          | flag photos as private that may be offensive
`PHOTOPRISM_UPLOAD_NSFW`   | --upload-nsfw                          | allow uploads that may be offensive
`PHOTOPRISM_GEOCODING_API` | --geocoding-api value, -g value        | geocoding api (none, osm or places) (default: "places")
`PHOTOPRISM_DOWNLOAD_TOKEN` | --download-token SECRET               | SECRET url token for file downloads
`PHOTOPRISM_PREVIEW_TOKEN` | --preview-token SECRET                 | SECRET url token for preview images and video streaming (default: "public")
`PHOTOPRISM_THUMB_FILTER`  | --thumb-filter NAME, -f NAME           | resample filter NAME (best to worst: blackman, lanczos, cubic, linear) (default: "lanczos")
`PHOTOPRISM_THUMB_UNCACHED` | --thumb-uncached, -u                  | enable on-demand thumbnail rendering (high memory and cpu usage)
`PHOTOPRISM_THUMB_SIZE`    | --thumb-size PIXELS, -s PIXELS         | pre-rendered thumbnail size limit in PIXELS (720-7680) (default: 2048)
`PHOTOPRISM_THUMB_SIZE_UNCACHED` |  --thumb-size-uncached PIXELS, -x PIXELS | on-demand rendering size limit in PIXELS (720-7680) (default: 7680)
`PHOTOPRISM_JPEG_SIZE`     | --jpeg-size PIXELS                     | size limit for converted image files in PIXELS (720-30000) (default: 7680)
`PHOTOPRISM_JPEG_QUALITY`  | --jpeg-quality value, -q value         | choose 95 for high-quality thumbnails (25-100) (default: 90)
