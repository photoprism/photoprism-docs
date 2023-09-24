# Config Options #

!!! tldr ""
    Changing values in a `docker-compose.yml` file or in the [Advanced Settings](../user-guide/settings/advanced.md) UI always **requires a restart** to take effect. Open a terminal, run `docker compose stop`, and then run `docker compose up -d` to restart all services.

### Authentication ###

!!! danger ""
    `PHOTOPRISM_AUTH_MODE: public` is NOT recommended for instances installed on a server accessible from outside your home network.

|          Environment          |       CLI Flag       | Default  | Description                                                                   |
|-------------------------------|----------------------|----------|-------------------------------------------------------------------------------|
| PHOTOPRISM_AUTH_MODE          | --auth-mode          | password | authentication `MODE` (public, password)                                      |
| PHOTOPRISM_ADMIN_USER         | --admin-user         | admin    | admin login `USERNAME`                                                        |
| PHOTOPRISM_ADMIN_PASSWORD     | --admin-password     |          | initial admin `PASSWORD` (8-72 characters)                                    |
| PHOTOPRISM_SESSION_MAXAGE     | --session-maxage     |  1209600 | time in `SECONDS` until API sessions expire automatically (-1 to disable)     |
| PHOTOPRISM_SESSION_TIMEOUT    | --session-timeout    |   604800 | time in `SECONDS` until API sessions expire due to inactivity (-1 to disable) |
| PHOTOPRISM_REGISTER_URI       | --register-uri       |          | user registration `URI` *plus*                                                |
| PHOTOPRISM_PASSWORD_LENGTH    | --password-length    |        8 | minimum password `LENGTH` in characters *plus*                                |
| PHOTOPRISM_PASSWORD_RESET_URI | --password-reset-uri |          | forgot password `URI` *plus*                                                  |

### Logging ###

|     Environment      |  CLI Flag   | Default |                                   Description                                    |
|----------------------|-------------|---------|----------------------------------------------------------------------------------|
| PHOTOPRISM_LOG_LEVEL | --log-level | info    | log message verbosity `LEVEL` (trace, debug, info, warning, error, fatal, panic) |
| PHOTOPRISM_DEBUG     | --debug     |         | enable debug mode, show non-essential log messages                               |
| PHOTOPRISM_TRACE     | --trace     |         | enable trace mode, show all log messages                                         |

### Storage ###

|         Environment         |      CLI Flag      |           Default            |                                             Description                                              |
|-----------------------------|--------------------|------------------------------|------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_CONFIG_PATH      | --config-path      |                              | config storage `PATH`, values in options.yml override CLI flags and environment variables if present |
| PHOTOPRISM_DEFAULTS_YAML    | --defaults-yaml    | /etc/photoprism/defaults.yml | load config defaults from `FILE` if exists, does not override CLI flags and environment variables    |
| PHOTOPRISM_ORIGINALS_PATH   | --originals-path   |                              | storage `PATH` of your original media files (photos and videos)                                      |
| PHOTOPRISM_ORIGINALS_LIMIT  | --originals-limit  |                         1000 | maximum size of media files in `MB` (1-100000; -1 to disable)                                        |
| PHOTOPRISM_RESOLUTION_LIMIT | --resolution-limit |                          150 | maximum resolution of media files in `MEGAPIXELS` (1-900; -1 to disable)                             |
| PHOTOPRISM_USERS_PATH       | --users-path       | users                        | relative `PATH` to create base and upload subdirectories for users                                   |
| PHOTOPRISM_STORAGE_PATH     | --storage-path     |                              | writable storage `PATH` for sidecar, cache, and database files                                       |
| PHOTOPRISM_SIDECAR_PATH     | --sidecar-path     |                              | custom relative or absolute sidecar `PATH` *optional*                                                |
| PHOTOPRISM_BACKUP_PATH      | --backup-path      |                              | custom backup `PATH` for index backup files *optional*                                               |
| PHOTOPRISM_CACHE_PATH       | --cache-path       |                              | custom cache `PATH` for sessions and thumbnail files *optional*                                      |
| PHOTOPRISM_IMPORT_PATH      | --import-path      |                              | base `PATH` from which files can be imported to originals *optional*                                 |
| PHOTOPRISM_IMPORT_DEST      | --import-dest      |                              | relative originals `PATH` to which the files should be imported by default *optional*                |
| PHOTOPRISM_ASSETS_PATH      | --assets-path      |                              | assets `PATH` containing static resources like icons, models, and translations                       |
| PHOTOPRISM_TEMP_PATH        | --temp-path        |                              | temporary file `PATH` *optional*                                                                     |

### Index Workers ###

|        Environment         |     CLI Flag      | Default |                                          Description                                          |
|----------------------------|-------------------|---------|-----------------------------------------------------------------------------------------------|
| PHOTOPRISM_WORKERS         | --workers         |       4 | maximum `NUMBER` of indexing workers, default depends on the number of physical cores         |
| PHOTOPRISM_WAKEUP_INTERVAL | --wakeup-interval | 15m0s   | `DURATION` between worker runs required for face recognition and index maintenance (1-86400s) |
| PHOTOPRISM_AUTO_INDEX      | --auto-index      |     300 | WebDAV auto index safety delay in `SECONDS` (-1 to disable)                                   |
| PHOTOPRISM_AUTO_IMPORT     | --auto-import     |     180 | WebDAV auto import safety delay in `SECONDS` (-1 to disable)                                  |

### Feature Flags ###

|            Environment            |         CLI Flag         | Default |                                       Description                                       |
|-----------------------------------|--------------------------|---------|-----------------------------------------------------------------------------------------|
| PHOTOPRISM_READONLY               | --read-only              |         | disable import, upload, delete, and all other operations that require write permissions |
| PHOTOPRISM_EXPERIMENTAL           | --experimental           |         | enable experimental features                                                            |
| PHOTOPRISM_DISABLE_SETTINGS       | --disable-settings       |         | disable settings UI and API                                                             |
| PHOTOPRISM_DISABLE_RESTART        | --disable-restart        |         | disable restarting the server from the user interface                                   |
| PHOTOPRISM_DISABLE_BACKUPS        | --disable-backups        |         | disable backing up albums and photo metadata to YAML files                              |
| PHOTOPRISM_DISABLE_WEBDAV         | --disable-webdav         |         | disable built-in WebDAV server                                                          |
| PHOTOPRISM_DISABLE_PLACES         | --disable-places         |         | disable reverse geocoding and maps                                                      |
| PHOTOPRISM_DISABLE_TENSORFLOW     | --disable-tensorflow     |         | disable all features depending on TensorFlow                                            |
| PHOTOPRISM_DISABLE_FACES          | --disable-faces          |         | disable face detection and recognition (requires TensorFlow)                            |
| PHOTOPRISM_DISABLE_CLASSIFICATION | --disable-classification |         | disable image classification (requires TensorFlow)                                      |
| PHOTOPRISM_DISABLE_SIPS           | --disable-sips           |         | disable conversion of media files with Sips *macOS only*                                |
| PHOTOPRISM_DISABLE_FFMPEG         | --disable-ffmpeg         |         | disable video transcoding and thumbnail extraction with FFmpeg                          |
| PHOTOPRISM_DISABLE_EXIFTOOL       | --disable-exiftool       |         | disable creating JSON metadata sidecar files with ExifTool                              |
| PHOTOPRISM_DISABLE_DARKTABLE      | --disable-darktable      |         | disable conversion of RAW images with Darktable                                         |
| PHOTOPRISM_DISABLE_RAWTHERAPEE    | --disable-rawtherapee    |         | disable conversion of RAW images with RawTherapee                                       |
| PHOTOPRISM_DISABLE_IMAGEMAGICK    | --disable-imagemagick    |         | disable conversion of image files with ImageMagick                                      |
| PHOTOPRISM_DISABLE_HEIFCONVERT    | --disable-heifconvert    |         | disable conversion of HEIC images with libheif                                          |
| PHOTOPRISM_DISABLE_RSVGCONVERT    | --disable-rsvgconvert    |         | disable conversion of SVG graphics with librsvg *plus*                                  |
| PHOTOPRISM_DISABLE_VECTORS        | --disable-vectors        |         | disable vector graphics support *plus*                                                  |
| PHOTOPRISM_DISABLE_JPEGXL         | --disable-jpegxl         |         | disable JPEG XL file format support                                                     |
| PHOTOPRISM_DISABLE_RAW            | --disable-raw            |         | disable indexing and conversion of RAW images                                           |
| PHOTOPRISM_RAW_PRESETS            | --raw-presets            |         | enables applying user presets when converting RAW images (reduces performance)          |
| PHOTOPRISM_EXIF_BRUTEFORCE        | --exif-bruteforce        |         | always perform a brute-force search if no Exif headers were found                       |
| PHOTOPRISM_DETECT_NSFW            | --detect-nsfw            |         | automatically flag photos as private that MAY be offensive (requires TensorFlow)        |
| PHOTOPRISM_UPLOAD_NSFW            | --upload-nsfw            |         | allow uploads that MAY be offensive (no effect without TensorFlow)                      |

### Customization ###

|        Environment        |     CLI Flag     |  Default   |                               Description                                |
|---------------------------|------------------|------------|--------------------------------------------------------------------------|
| PHOTOPRISM_DEFAULT_LOCALE | --default-locale | en         | standard user interface language `CODE`                                  |
| PHOTOPRISM_DEFAULT_THEME  | --default-theme  |            | standard user interface theme `NAME`                                     |
| PHOTOPRISM_APP_NAME       | --app-name       |            | progressive web app `NAME` when installed on a device                    |
| PHOTOPRISM_APP_MODE       | --app-mode       | standalone | progressive web app `MODE` (fullscreen, standalone, minimal-ui, browser) |
| PHOTOPRISM_APP_ICON       | --app-icon       |            | home screen `ICON` (logo, app, crisp, mint, bold, square)                |
| PHOTOPRISM_APP_COLOR      | --app-color      | #000000    | splash screen `COLOR` code                                               |
| PHOTOPRISM_LEGAL_INFO     | --legal-info     |            | legal information `TEXT`, displayed in the page footer                   |
| PHOTOPRISM_LEGAL_URL      | --legal-url      |            | legal information `URL`                                                  |
| PHOTOPRISM_WALLPAPER_URI  | --wallpaper-uri  |            | login screen background image `URI`                                      |

### Site Information ###

|         Environment         |      CLI Flag      |        Default         |             Description              |
|-----------------------------|--------------------|------------------------|--------------------------------------|
| PHOTOPRISM_CDN_URL          | --cdn-url          |                        | content delivery network `URL`       |
| PHOTOPRISM_CDN_VIDEO        | --cdn-video        |                        | stream videos over the specified CDN |
| PHOTOPRISM_SITE_URL         | --site-url         | http://localhost:2342/ | public site `URL`                    |
| PHOTOPRISM_SITE_AUTHOR      | --site-author      |                        | site `OWNER`, copyright, or artist   |
| PHOTOPRISM_SITE_TITLE       | --site-title       |                        | site `TITLE`                         |
| PHOTOPRISM_SITE_CAPTION     | --site-caption     | AI-Powered Photos App  | site `CAPTION`                       |
| PHOTOPRISM_SITE_DESCRIPTION | --site-description |                        | site `DESCRIPTION` *optional*        |
| PHOTOPRISM_SITE_PREVIEW     | --site-preview     |                        | sharing preview image `URL`          |

### Proxy Servers ###

|           Environment           |        CLI Flag        |      Default      |                                               Description                                               |
|---------------------------------|------------------------|-------------------|---------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_HTTPS_PROXY          | --https-proxy          |                   | proxy server `URL` to be used for outgoing connections *optional*                                       |
| PHOTOPRISM_HTTPS_PROXY_INSECURE | --https-proxy-insecure |                   | ignore invalid HTTPS certificates when using a proxy                                                    |
| PHOTOPRISM_TRUSTED_PROXY        | --trusted-proxy        | 172.16.0.0/12     | `CIDR` ranges or IPv4/v6 addresses from which reverse proxy headers can be trusted, separated by commas |
| PHOTOPRISM_PROXY_PROTO_HEADER   | --proxy-proto-header   | X-Forwarded-Proto | proxy protocol header `NAME`                                                                            |
| PHOTOPRISM_PROXY_PROTO_HTTPS    | --proxy-proto-https    | https             | forwarded HTTPS protocol `NAME`                                                                         |

### Web Server ###

|           Environment           |        CLI Flag        |    Default    | Description                                                                                             |
|---------------------------------|------------------------|---------------|---------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_DISABLE_TLS          | --disable-tls          |               | disable HTTPS/TLS even if the site URL starts with https:// and a certificate is available              |
| PHOTOPRISM_DEFAULT_TLS          | --default-tls          |               | default to a self-signed HTTPS/TLS certificate if no other certificate is available                     |
| PHOTOPRISM_TLS_CERT             | --tls-cert             |               | public HTTPS certificate `FILE` (.crt), ignored for Unix domain sockets                                 |
| PHOTOPRISM_TLS_KEY              | --tls-key              |               | private HTTPS key `FILE` (.key), ignored for Unix domain sockets                                        |
| PHOTOPRISM_DISABLE_STS          | --disable-sts          |               | disable HTTP Strict-Transport-Security (STS) header                                                     |
| PHOTOPRISM_STS_SECONDS          | --sts-seconds          |      31536000 | `TIME` for the browser to remember that the site is to be accessed only via HTTPS (0 to disable) *plus* |
| PHOTOPRISM_STS_SUBDOMAINS       | --sts-subdomains       |               | rule applies to all subdomains as well *plus*                                                           |
| PHOTOPRISM_STS_PRELOAD          | --sts-preload          |               | submit to Google's HSTS preload service *plus*                                                          |
| PHOTOPRISM_LOGIN_LIMIT          | --login-limit          |            10 | maximum number of consecutive failed LOGIN `ATTEMPTS` from a single IP *plus*                           |
| PHOTOPRISM_LOGIN_INTERVAL       | --login-interval       | 1m0s          | average `DURATION` between failed LOGIN attempts from a single IP (0-86400s) *plus*                     |
| PHOTOPRISM_IPS_LIMIT            | --ips-limit            |             3 | maximum number of malicious request `ATTEMPTS` before a client IP is blocked (-1 to disable) *plus*     |
| PHOTOPRISM_IPS_INTERVAL         | --ips-interval         | 1h0m0s        | average `DURATION` between malicious request attempts from a single IP (0-86400s) *plus*                |
| PHOTOPRISM_HTTP_CSP             | --http-csp             |               | HTTP Content-Security-Policy (CSP) `HEADER` *plus*                                                      |
| PHOTOPRISM_HTTP_CTO             | --http-cto             | nosniff       | HTTP X-Content-Type-Options `HEADER` *plus*                                                             |
| PHOTOPRISM_HTTP_COOP            | --http-coop            | same-origin   | HTTP Cross-Origin-Opener-Policy (COOP) `HEADER` *plus*                                                  |
| PHOTOPRISM_HTTP_REFERRER_POLICY | --http-referrer-policy | same-origin   | HTTP Referrer-Policy `HEADER` *plus*                                                                    |
| PHOTOPRISM_HTTP_FRAME_OPTIONS   | --http-frame-options   | DENY          | HTTP X-Frame-Options `HEADER` *plus*                                                                    |
| PHOTOPRISM_HTTP_XSS_PROTECTION  | --http-xss-protection  | 1; mode=block | HTTP X-XSS-Protection `HEADER` *plus*                                                                   |
| PHOTOPRISM_HTTP_MODE            | --http-mode            |               | Web server `MODE` (debug, release, test)                                                                |
| PHOTOPRISM_HTTP_COMPRESSION     | --http-compression     |               | Web server compression `METHOD` (gzip, none)                                                            |
| PHOTOPRISM_HTTP_CACHE_MAXAGE    | --http-cache-maxage    |       2592000 | time in `SECONDS` until cached content expires                                                          |
| PHOTOPRISM_HTTP_VIDEO_MAXAGE    | --http-video-maxage    |         21600 | time in `SECONDS` until cached videos expire                                                            |
| PHOTOPRISM_HTTP_CACHE_PUBLIC    | --http-cache-public    |               | allow static content to be cached by a CDN or caching proxy                                             |
| PHOTOPRISM_HTTP_HOST            | --http-host            | 0.0.0.0       | Web server `IP` address or Unix domain socket, e.g. unix:/var/run/photoprism.sock                       |
| PHOTOPRISM_HTTP_PORT            | --http-port            |          2342 | Web server port `NUMBER`, ignored for Unix domain sockets                                               |
| PHOTOPRISM_HTTP_HOSTNAME        | --http-hostname        |               | serve requests for this `HOSTNAME` only *plus*                                                          |

### Database Connection ###

|          Environment           |       CLI Flag        |  Default   |                           Description                           |
|--------------------------------|-----------------------|------------|-----------------------------------------------------------------|
| PHOTOPRISM_DATABASE_DRIVER     | --database-driver     | sqlite     | database `DRIVER` (sqlite, mysql)                               |
| PHOTOPRISM_DATABASE_DSN        | --database-dsn        |            | database connection `DSN` (sqlite file, optional for mysql)     |
| PHOTOPRISM_DATABASE_NAME       | --database-name       | photoprism | database schema `NAME`                                          |
| PHOTOPRISM_DATABASE_SERVER     | --database-server     |            | database `HOST` incl. port e.g. "mariadb:3306" (or socket path) |
| PHOTOPRISM_DATABASE_USER       | --database-user       | photoprism | database user `NAME`                                            |
| PHOTOPRISM_DATABASE_PASSWORD   | --database-password   |            | database user `PASSWORD`                                        |
| PHOTOPRISM_DATABASE_CONNS      | --database-conns      |          0 | maximum `NUMBER` of open database connections                   |
| PHOTOPRISM_DATABASE_CONNS_IDLE | --database-conns-idle |          0 | maximum `NUMBER` of idle database connections                   |

### File Converters ###

| Environment                      | CLI Flag                | Default                        | Description                                                           |
|----------------------------------|-------------------------|--------------------------------|-----------------------------------------------------------------------|
| PHOTOPRISM_SIPS_BIN              | --sips-bin              | sips                           | Sips `COMMAND` for media file conversion *macOS only*                 |
| PHOTOPRISM_SIPS_BLACKLIST        | --sips-blacklist        | avif,avifs                     | do not use Sips to convert files with these `EXTENSIONS` *macOS only* |
| PHOTOPRISM_FFMPEG_BIN            | --ffmpeg-bin            | ffmpeg                         | FFmpeg `COMMAND` for video transcoding and thumbnail extraction       |
| PHOTOPRISM_FFMPEG_ENCODER        | --ffmpeg-encoder        | libx264                        | FFmpeg AVC encoder `NAME`                                             |
| PHOTOPRISM_FFMPEG_SIZE           | --ffmpeg-size           | 3840                           | maximum video size in `PIXELS` (720-7680)                             |
| PHOTOPRISM_FFMPEG_BITRATE        | --ffmpeg-bitrate        | 50                             | maximum video `BITRATE` in Mbit/s                                     |
| PHOTOPRISM_FFMPEG_MAP_VIDEO      | --ffmpeg-map-video      | `0:v:0`                        | video `STREAMS` that should be transcoded                             |
| PHOTOPRISM_FFMPEG_MAP_AUDIO      | --ffmpeg-map-audio      | `0:a:0?`                       | audio `STREAMS` that should be transcoded                             |
| PHOTOPRISM_EXIFTOOL_BIN          | --exiftool-bin          | exiftool                       | ExifTool `COMMAND` for extracting metadata                            |
| PHOTOPRISM_DARKTABLE_BIN         | --darktable-bin         | darktable-cli                  | Darktable CLI `COMMAND` for RAW to JPEG conversion                    |
| PHOTOPRISM_DARKTABLE_BLACKLIST   | --darktable-blacklist   |                                | do not use Darktable to convert files with these `EXTENSIONS`         |
| PHOTOPRISM_DARKTABLE_CACHE_PATH  | --darktable-cache-path  |                                | custom Darktable cache `PATH`                                         |
| PHOTOPRISM_DARKTABLE_CONFIG_PATH | --darktable-config-path |                                | custom Darktable config `PATH`                                        |
| PHOTOPRISM_RAWTHERAPEE_BIN       | --rawtherapee-bin       | rawtherapee-cli                | RawTherapee CLI `COMMAND` for RAW to JPEG conversion                  |
| PHOTOPRISM_RAWTHERAPEE_BLACKLIST | --rawtherapee-blacklist | dng                            | do not use RawTherapee to convert files with these `EXTENSIONS`       |
| PHOTOPRISM_IMAGEMAGICK_BIN       | --imagemagick-bin       | convert                        | ImageMagick CLI `COMMAND` for image file conversion                   |
| PHOTOPRISM_IMAGEMAGICK_BLACKLIST | --imagemagick-blacklist | heif,heic,heics,avif,avifs,jxl | do not use ImageMagick to convert files with these `EXTENSIONS`       |
| PHOTOPRISM_HEIFCONVERT_BIN       | --heifconvert-bin       | heif-convert                   | libheif HEIC image conversion `COMMAND`                               |
| PHOTOPRISM_RSVGCONVERT_BIN       | --rsvgconvert-bin       | rsvg-convert                   | librsvg SVG graphics conversion `COMMAND` *plus*                      |

### Security Tokens ###

|        Environment        |     CLI Flag     | Default |                                    Description                                     |
|---------------------------|------------------|---------|------------------------------------------------------------------------------------|
| PHOTOPRISM_DOWNLOAD_TOKEN | --download-token |         | `DEFAULT` download URL token for originals (leave empty for a random value)        |
| PHOTOPRISM_PREVIEW_TOKEN  | --preview-token  |         | `DEFAULT` thumbnail and video streaming URL token (leave empty for a random value) |

### Image Quality ###

|          Environment           |       CLI Flag        | Default |                                         Description                                         |
|--------------------------------|-----------------------|---------|---------------------------------------------------------------------------------------------|
| PHOTOPRISM_THUMB_COLOR         | --thumb-color         | sRGB    | standard color `PROFILE` for thumbnails (leave blank to disable)                            |
| PHOTOPRISM_THUMB_FILTER        | --thumb-filter        | lanczos | image downscaling filter `NAME` (best to worst: blackman, lanczos, cubic, linear)           |
| PHOTOPRISM_THUMB_SIZE          | --thumb-size          |    2048 | maximum size of thumbnails created during indexing in `PIXELS` (720-7680)                   |
| PHOTOPRISM_THUMB_SIZE_UNCACHED | --thumb-size-uncached |    7680 | maximum size of missing thumbnails created on demand in `PIXELS` (720-7680)                 |
| PHOTOPRISM_THUMB_UNCACHED      | --thumb-uncached      |         | enable on-demand creation of missing thumbnails (high memory and cpu usage)                 |
| PHOTOPRISM_JPEG_QUALITY        | --jpeg-quality        |      85 | a higher value increases the `QUALITY` and file size of JPEG images and thumbnails (25-100) |
| PHOTOPRISM_JPEG_SIZE           | --jpeg-size           |    7680 | maximum size of created JPEG sidecar files in `PIXELS` (720-30000)                          |
| PHOTOPRISM_PNG_SIZE            | --png-size            |    7680 | maximum size of created PNG sidecar files in `PIXELS` (720-30000)                           |

### Face Recognition ###

!!! info ""
    To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism first extracts crops from your images using a [library](https://github.com/esimov/pigo) based on [pixel intensity comparisons](https://dl.photoprism.app/pdf/20140820-Pixel_Intensity_Comparisons.pdf). These are then fed into TensorFlow to compute [512-dimensional vectors](https://dl.photoprism.app/pdf/20150101-FaceNet.pdf) for characterization. In the final step, the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) attempts to cluster these so-called face embeddings, so they can be matched to persons with just a few clicks. A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher value being more aggressive and leading to larger clusters with more false positives. To cluster a smaller number of faces, you can reduce the core to 3 or 2 similar faces.

We recommend that only advanced users change these parameters:

|          Environment          |       CLI Flag       | Default  |                               Description                               |
|-------------------------------|----------------------|----------|-------------------------------------------------------------------------|
| PHOTOPRISM_FACE_SIZE          | --face-size          |       50 | minimum size of faces in `PIXELS` (20-10000)                            |
| PHOTOPRISM_FACE_SCORE         | --face-score         | 9.000000 | minimum face `QUALITY` score (1-100)                                    |
| PHOTOPRISM_FACE_OVERLAP       | --face-overlap       |       42 | face area overlap threshold in `PERCENT` (1-100)                        |
| PHOTOPRISM_FACE_CLUSTER_SIZE  | --face-cluster-size  |       80 | minimum size of automatically clustered faces in `PIXELS` (20-10000)    |
| PHOTOPRISM_FACE_CLUSTER_SCORE | --face-cluster-score |       15 | minimum `QUALITY` score of automatically clustered faces (1-100)        |
| PHOTOPRISM_FACE_CLUSTER_CORE  | --face-cluster-core  |        4 | `NUMBER` of faces forming a cluster core (1-100)                        |
| PHOTOPRISM_FACE_CLUSTER_DIST  | --face-cluster-dist  | 0.640000 | similarity `DISTANCE` of faces forming a cluster core (0.1-1.5)         |
| PHOTOPRISM_FACE_MATCH_DIST    | --face-match-dist    | 0.460000 | similarity `OFFSET` for matching faces with existing clusters (0.1-1.5) |

### Daemon Mode ###

If you start the server as a *daemon* in the background, you can additionally specify a filename for the log and the process ID:

|       Environment       |    CLI Flag    | Default |             Description              |
|-------------------------|----------------|---------|--------------------------------------|
| PHOTOPRISM_PID_FILENAME | --pid-filename |         | process id `FILE` *daemon-mode only* |
| PHOTOPRISM_LOG_FILENAME | --log-filename |         | server log `FILE` *daemon-mode only* |

### Docker Image ###

The following variables are used by our Docker images only and have no effect otherwise:

| Environment              | Default | Description                                                                                                                                                                                  |
|--------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_UID           | 0       | run as a non-root user after initialization (supported: 0, 33, 50-99, 500-600, 900-1250, and 2000-2100)                                                                                      |
| PHOTOPRISM_GID           | 0       | run with a specific group id after initialization, can optionally be used together with `PHOTOPRISM_UID` (supported: 0, 33, 44, 50-99, 105, 109, 115, 116, 500-600, 900-1250, and 2000-2100) |
| PHOTOPRISM_UMASK         | 0002    | [file-creation mode](https://linuxize.com/post/umask-command-in-linux/) (default: u=rwx,g=rwx,o=rx)                                                                                          |
| PHOTOPRISM_INIT          |         | run/install on first startup (options: update https gpu tensorflow davfs clitools clean)                                                                                                     |
| PHOTOPRISM_DISABLE_CHOWN | false   | disable updating storage permissions via chmod and chown on startup                                                                                                                          |
