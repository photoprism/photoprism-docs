# Config Options #

!!! tldr ""
    Note that changes to the config options listed below **always require a restart** to take effect.[^1] Instead of using environment variables, you can alternatively use an ↪ [`options.yml`](config-files/index.md) file to configure your instance.

### Authentication ###

| Environment                                      | CLI Flag          | Default            | Description                                                                                         |
|--------------------------------------------------|-------------------|--------------------|-----------------------------------------------------------------------------------------------------|
| PHOTOPRISM_AUTH_MODE                             | --auth-mode       | password           | authentication `MODE` (public[^2], password)                                                        |
| PHOTOPRISM_ADMIN_USER, PHOTOPRISM_ADMIN_USERNAME | --admin-user      | admin              | `USERNAME` of the superadmin account that is created on first startup                               |
| PHOTOPRISM_ADMIN_PASSWORD                        | --admin-password  |                    | initial `PASSWORD` of the superadmin account (8-72 characters)                                      |
| PHOTOPRISM_PASSWORD_LENGTH                       | --password-length | 8                  | minimum password `LENGTH` in characters *plus*                                                      |
| PHOTOPRISM_OIDC_URI                              | --oidc-uri        |                    | issuer `URI` for single sign-on via OpenID Connect, e.g. https://accounts.google.com                |
| PHOTOPRISM_OIDC_CLIENT                           | --oidc-client     |                    | client `ID` for single sign-on via OpenID Connect                                                   |
| PHOTOPRISM_OIDC_SECRET                           | --oidc-secret     |                    | client `SECRET` for single sign-on via OpenID Connect                                               |
| PHOTOPRISM_OIDC_PROVIDER                         | --oidc-provider   |                    | custom identity provider `NAME`, e.g. Google                                                        |
| PHOTOPRISM_OIDC_ICON                             | --oidc-icon       |                    | custom identity provider icon `URI`                                                                 |
| PHOTOPRISM_OIDC_REDIRECT                         | --oidc-redirect   |                    | automatically redirect unauthenticated users to the configured identity provider                    |
| PHOTOPRISM_OIDC_REGISTER                         | --oidc-register   |                    | allow new users to create an account when they sign in with OpenID Connect                          |
| PHOTOPRISM_OIDC_USERNAME                         | --oidc-username   | preferred_username | preferred username `CLAIM` for new OpenID Connect users (preferred_username, name, nickname, email) |
| PHOTOPRISM_OIDC_WEBDAV                           | --oidc-webdav     |                    | allow new OpenID Connect users to use WebDAV when they have a role that allows it                   |
| PHOTOPRISM_DISABLE_OIDC                          | --disable-oidc    |                    | disable single sign-on via OpenID Connect, even if an identity provider has been configured         |
| PHOTOPRISM_SESSION_MAXAGE                        | --session-maxage  | 1209600            | session expiration time in `SECONDS`, doubled for accounts with 2FA (-1 to disable)                 |
| PHOTOPRISM_SESSION_TIMEOUT                       | --session-timeout | 604800             | session idle time in `SECONDS`, doubled for accounts with 2FA (-1 to disable)                       |
| PHOTOPRISM_SESSION_CACHE                         | --session-cache   | 900                | session cache duration in `SECONDS` (60-3600)                                                       |

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
| PHOTOPRISM_IMPORT_PATH      | --import-path      |                              | base `PATH` from which files can be imported to originals *optional*                                 |
| PHOTOPRISM_IMPORT_DEST      | --import-dest      |                              | relative originals `PATH` to which the files should be imported by default *optional*                |
| PHOTOPRISM_CACHE_PATH       | --cache-path       |                              | custom cache `PATH` for sessions and thumbnail files *optional*                                      |
| PHOTOPRISM_TEMP_PATH        | --temp-path        |                              | temporary file `PATH` *optional*                                                                     |
| PHOTOPRISM_ASSETS_PATH      | --assets-path      |                              | assets `PATH` containing static resources like icons, models, and translations                       |

### Sidecar Files ###

|       Environment       |    CLI Flag    | Default |                      Description                      |
|-------------------------|----------------|---------|-------------------------------------------------------|
| PHOTOPRISM_SIDECAR_PATH | --sidecar-path |         | custom relative or absolute sidecar `PATH` *optional* |
| PHOTOPRISM_SIDECAR_YAML | --sidecar-yaml | true    | create YAML sidecar files to back up picture metadata |

### Backup ###

|        Environment         |     CLI Flag      | Default |                                                  Description                                                  |
|----------------------------|-------------------|---------|---------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_BACKUP_PATH     | --backup-path     |         | custom base `PATH` for creating and restoring backups *optional*                                              |
| PHOTOPRISM_BACKUP_SCHEDULE | --backup-schedule | daily   | backup `SCHEDULE` in cron format (e.g. "0 12 \* \* \*" for daily at noon) or at a random time (daily, weekly) |
| PHOTOPRISM_BACKUP_RETAIN   | --backup-retain   |       3 | `NUMBER` of index backups to keep (-1 to keep all)                                                            |
| PHOTOPRISM_BACKUP_DATABASE | --backup-database | true    | create regular backups based on the configured schedule                                                       |
| PHOTOPRISM_BACKUP_ALBUMS   | --backup-albums   | true    | create YAML files to back up album metadata                                                                   |

### Indexing ###

|                 Environment                  |     CLI Flag      | Default |                                            Description                                            |
|----------------------------------------------|-------------------|---------|---------------------------------------------------------------------------------------------------|
| PHOTOPRISM_INDEX_WORKERS, PHOTOPRISM_WORKERS | --index-workers   |       4 | maximum `NUMBER` of indexing workers, default depends on the number of physical cores             |
| PHOTOPRISM_INDEX_SCHEDULE                    | --index-schedule  |         | indexing `SCHEDULE` in cron format (e.g. "@every 3h" for every 3 hours; "" to disable)            |
| PHOTOPRISM_WAKEUP_INTERVAL                   | --wakeup-interval | 15m0s   | `TIME` between facial recognition, file sync, and metadata worker runs (1-86400s)                 |
| PHOTOPRISM_AUTO_INDEX                        | --auto-index      |     300 | delay before automatically indexing files in `SECONDS` when uploading via WebDAV (-1 to disable)  |
| PHOTOPRISM_AUTO_IMPORT                       | --auto-import     |      -1 | delay before automatically importing files in `SECONDS` when uploading via WebDAV (-1 to disable) |

### Feature Flags ###

|            Environment            |         CLI Flag         | Default |                                           Description                                            |
|-----------------------------------|--------------------------|---------|--------------------------------------------------------------------------------------------------|
| PHOTOPRISM_READONLY               | --read-only              |         | disable features that require write permission for the originals folder                          |
| PHOTOPRISM_EXPERIMENTAL           | --experimental           |         | enable new features currently under development                                                  |
| PHOTOPRISM_DISABLE_SETTINGS       | --disable-settings       |         | disable the settings user interface and server API, e.g. in combination with public mode         |
| PHOTOPRISM_DISABLE_BACKUPS        | --disable-backups        |         | prevent database and album backups as well as YAML sidecar files from being created              |
| PHOTOPRISM_DISABLE_RESTART        | --disable-restart        |         | prevent admins from restarting the server through the user interface                             |
| PHOTOPRISM_DISABLE_WEBDAV         | --disable-webdav         |         | prevent other apps from accessing PhotoPrism as a shared network drive                           |
| PHOTOPRISM_DISABLE_PLACES         | --disable-places         |         | disable interactive world maps and reverse geocoding                                             |
| PHOTOPRISM_DISABLE_TENSORFLOW     | --disable-tensorflow     |         | disable features depending on TensorFlow, e.g. image classification and face recognition         |
| PHOTOPRISM_DISABLE_FACES          | --disable-faces          |         | disable face detection and recognition (requires TensorFlow)                                     |
| PHOTOPRISM_DISABLE_CLASSIFICATION | --disable-classification |         | disable image classification (requires TensorFlow)                                               |
| PHOTOPRISM_DISABLE_FFMPEG         | --disable-ffmpeg         |         | disable video transcoding and thumbnail extraction with FFmpeg                                   |
| PHOTOPRISM_DISABLE_EXIFTOOL       | --disable-exiftool       |         | disable metadata extraction with ExifTool (required for full Video, Live Photo, and XMP support) |
| PHOTOPRISM_DISABLE_VIPS           | --disable-vips           |         | disable image processing and conversion with libvips                                             |
| PHOTOPRISM_DISABLE_SIPS           | --disable-sips           |         | disable file conversion using the sips command under macOS                                       |
| PHOTOPRISM_DISABLE_DARKTABLE      | --disable-darktable      |         | disable conversion of RAW images with Darktable                                                  |
| PHOTOPRISM_DISABLE_RAWTHERAPEE    | --disable-rawtherapee    |         | disable conversion of RAW images with RawTherapee                                                |
| PHOTOPRISM_DISABLE_IMAGEMAGICK    | --disable-imagemagick    |         | disable conversion of image files with ImageMagick                                               |
| PHOTOPRISM_DISABLE_HEIFCONVERT    | --disable-heifconvert    |         | disable conversion of HEIC images with libheif                                                   |
| PHOTOPRISM_DISABLE_RSVGCONVERT    | --disable-rsvgconvert    |         | disable conversion of SVG graphics with librsvg *plus*                                           |
| PHOTOPRISM_DISABLE_VECTORS        | --disable-vectors        |         | disable vector graphics support *plus*                                                           |
| PHOTOPRISM_DISABLE_JPEGXL         | --disable-jpegxl         |         | disable JPEG XL file format support                                                              |
| PHOTOPRISM_DISABLE_RAW            | --disable-raw            |         | disable indexing and conversion of RAW images                                                    |
| PHOTOPRISM_RAW_PRESETS            | --raw-presets            |         | enables applying user presets when converting RAW images (reduces performance)                   |
| PHOTOPRISM_EXIF_BRUTEFORCE        | --exif-bruteforce        |         | always perform a brute-force search if no Exif headers were found                                |
| PHOTOPRISM_DETECT_NSFW            | --detect-nsfw            |         | flag newly added pictures as private if they might be offensive (requires TensorFlow)            |
| PHOTOPRISM_UPLOAD_NSFW            | --upload-nsfw            |         | allow uploads that might be offensive (detecting unsafe content requires TensorFlow)             |

### Customization ###

|         Environment         |      CLI Flag      |  Default   |                               Description                                |
|-----------------------------|--------------------|------------|--------------------------------------------------------------------------|
| PHOTOPRISM_DEFAULT_LOCALE   | --default-locale   | en         | default user interface language `CODE`                                   |
| PHOTOPRISM_DEFAULT_TIMEZONE | --default-timezone | UTC        | default time zone `NAME`, e.g. for scheduling backups                    |
| PHOTOPRISM_DEFAULT_THEME    | --default-theme    |            | default user interface theme `NAME`                                      |
| PHOTOPRISM_APP_NAME         | --app-name         |            | progressive web app `NAME` when installed on a device                    |
| PHOTOPRISM_APP_MODE         | --app-mode         | standalone | progressive web app `MODE` (fullscreen, standalone, minimal-ui, browser) |
| PHOTOPRISM_APP_ICON         | --app-icon         |            | home screen `ICON` (logo, app, crisp, mint, bold, square)                |
| PHOTOPRISM_APP_COLOR        | --app-color        | #000000    | splash screen `COLOR` code                                               |
| PHOTOPRISM_LEGAL_INFO       | --legal-info       |            | legal information `TEXT`, displayed in the page footer                   |
| PHOTOPRISM_LEGAL_URL        | --legal-url        |            | legal information `URL`                                                  |
| PHOTOPRISM_WALLPAPER_URI    | --wallpaper-uri    |            | login screen background image `URI`                                      |

### Site Information ###

|         Environment         |      CLI Flag      |                                        Default                                        |                                                         Description                                                          |
|-----------------------------|--------------------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_SITE_URL         | --site-url         | http://localhost:2342/                                                                | public site `URL`                                                                                                            |
| PHOTOPRISM_SITE_AUTHOR      | --site-author      |                                                                                       | site `OWNER`, copyright, or artist                                                                                           |
| PHOTOPRISM_SITE_TITLE       | --site-title       |                                                                                       | site `TITLE`                                                                                                                 |
| PHOTOPRISM_SITE_CAPTION     | --site-caption     | AI-Powered Photos App                                                                 | site `CAPTION`                                                                                                               |
| PHOTOPRISM_SITE_DESCRIPTION | --site-description |                                                                                       | site `DESCRIPTION` *optional*                                                                                                |
| PHOTOPRISM_SITE_PREVIEW     | --site-preview     |                                                                                       | sharing preview image `URL`                                                                                                  |
| PHOTOPRISM_CDN_URL          | --cdn-url          |                                                                                       | content delivery network `URL`                                                                                               |
| PHOTOPRISM_CDN_VIDEO        | --cdn-video        |                                                                                       | stream videos over the specified CDN                                                                                         |
| PHOTOPRISM_CORS_ORIGIN      | --cors-origin      |                                                                                       | origin `URL` from which browsers are allowed to perform cross-origin requests (leave blank to disable or use * to allow all) |
| PHOTOPRISM_CORS_HEADERS     | --cors-headers     | Accept, Accept-Ranges, Content-Disposition, Content-Encoding, Content-Range, Location | one or more `HEADERS` that browsers should see when performing a cross-origin request                                        |
| PHOTOPRISM_CORS_METHODS     | --cors-methods     | GET, HEAD, OPTIONS                                                                    | one or more `METHODS` that may be used when performing a cross-origin request                                                |

### Proxy Servers ###

|           Environment           |        CLI Flag        |      Default      |                                               Description                                               |
|---------------------------------|------------------------|-------------------|---------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_HTTPS_PROXY          | --https-proxy          |                   | proxy server `URL` to be used for outgoing connections *optional*                                       |
| PHOTOPRISM_HTTPS_PROXY_INSECURE | --https-proxy-insecure |                   | ignore invalid HTTPS certificates when using a proxy                                                    |
| PHOTOPRISM_TRUSTED_PROXY        | --trusted-proxy        | 172.16.0.0/12     | `CIDR` ranges or IPv4/v6 addresses from which reverse proxy headers can be trusted, separated by commas |
| PHOTOPRISM_PROXY_PROTO_HEADER   | --proxy-proto-header   | X-Forwarded-Proto | proxy protocol header `NAME`                                                                            |
| PHOTOPRISM_PROXY_PROTO_HTTPS    | --proxy-proto-https    | https             | forwarded HTTPS protocol `NAME`                                                                         |

### Web Server ###

|           Environment           |        CLI Flag        |    Default    |                                               Description                                               |
|---------------------------------|------------------------|---------------|---------------------------------------------------------------------------------------------------------|
| PHOTOPRISM_DISABLE_TLS          | --disable-tls          |               | disable HTTPS/TLS even if the site URL starts with https:// and a certificate is available              |
| PHOTOPRISM_DEFAULT_TLS          | --default-tls          |               | default to a self-signed HTTPS/TLS certificate if no other certificate is available                     |
| PHOTOPRISM_TLS_CERT             | --tls-cert             |               | public HTTPS certificate `FILE` (.crt), ignored for Unix domain sockets                                 |
| PHOTOPRISM_TLS_KEY              | --tls-key              |               | private HTTPS key `FILE` (.key), ignored for Unix domain sockets                                        |
| PHOTOPRISM_DISABLE_STS          | --disable-sts          |               | disable HTTP Strict-Transport-Security (STS) header                                                     |
| PHOTOPRISM_STS_SECONDS          | --sts-seconds          |      31536000 | `TIME` for the browser to remember that the site is to be accessed only via HTTPS (0 to disable) *plus* |
| PHOTOPRISM_STS_SUBDOMAINS       | --sts-subdomains       |               | rule applies to all subdomains as well *plus*                                                           |
| PHOTOPRISM_STS_PRELOAD          | --sts-preload          |               | submit to Google's HSTS preload service *plus*                                                          |
| PHOTOPRISM_AUTH_LIMIT           | --auth-limit           |            60 | maximum number of consecutive invalid access `TOKENS` from a single IP *plus*                           |
| PHOTOPRISM_AUTH_INTERVAL        | --auth-interval        | 10s           | average `DURATION` between invalid access tokens from a single IP (0-86400s) *plus*                     |
| PHOTOPRISM_LOGIN_LIMIT          | --login-limit          |            10 | maximum number of consecutive failed `LOGINS` from a single IP *plus*                                   |
| PHOTOPRISM_LOGIN_INTERVAL       | --login-interval       | 1m0s          | average `DURATION` between failed logins from a single IP (0-86400s) *plus*                             |
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
| PHOTOPRISM_HTTP_CACHE_PUBLIC    | --http-cache-public    |               | allow static content to be cached by a CDN or caching proxy                                             |
| PHOTOPRISM_HTTP_CACHE_MAXAGE    | --http-cache-maxage    |       2592000 | time in `SECONDS` until cached content expires                                                          |
| PHOTOPRISM_HTTP_VIDEO_MAXAGE    | --http-video-maxage    |         21600 | time in `SECONDS` until cached videos expire                                                            |
| PHOTOPRISM_HTTP_HOST            | --http-host            | 0.0.0.0       | Web server `IP` address or Unix domain socket, e.g. unix:/var/run/photoprism.sock                       |
| PHOTOPRISM_HTTP_PORT            | --http-port            |          2342 | Web server port `NUMBER`, ignored for Unix domain sockets                                               |
| PHOTOPRISM_HTTP_HOSTNAME        | --http-hostname        |               | serve requests for this `HOSTNAME` only *plus*                                                          |

### Database Connection ###

|          Environment           |       CLI Flag        |  Default   |                            Description                             |
|--------------------------------|-----------------------|------------|--------------------------------------------------------------------|
| PHOTOPRISM_DATABASE_DRIVER     | --database-driver     | sqlite     | database `DRIVER` (sqlite, mysql)                                  |
| PHOTOPRISM_DATABASE_DSN        | --database-dsn        |            | database connection `DSN` (sqlite file, optional for mysql)        |
| PHOTOPRISM_DATABASE_NAME       | --database-name       | photoprism | database schema `NAME`                                             |
| PHOTOPRISM_DATABASE_SERVER     | --database-server     |            | database `HOST` incl. port e.g. "mariadb:3306" (or socket path)    |
| PHOTOPRISM_DATABASE_USER       | --database-user       | photoprism | database user `NAME`                                               |
| PHOTOPRISM_DATABASE_PASSWORD   | --database-password   |            | database user `PASSWORD`                                           |
| PHOTOPRISM_DATABASE_TIMEOUT    | --database-timeout    |         15 | timeout in `SECONDS` for establishing a database connection (1-60) |
| PHOTOPRISM_DATABASE_CONNS      | --database-conns      |          0 | maximum `NUMBER` of open database connections                      |
| PHOTOPRISM_DATABASE_CONNS_IDLE | --database-conns-idle |          0 | maximum `NUMBER` of idle database connections                      |

### File Conversion ###

|                           Environment                            |        CLI Flag         |                 Default                  |                           Description                           |
|------------------------------------------------------------------|-------------------------|------------------------------------------|-----------------------------------------------------------------|
| PHOTOPRISM_FFMPEG_BIN                                            | --ffmpeg-bin            | ffmpeg                                   | FFmpeg `COMMAND` for video transcoding and thumbnail extraction |
| PHOTOPRISM_FFMPEG_ENCODER                                        | --ffmpeg-encoder        | libx264                                  | FFmpeg AVC encoder `NAME`                                       |
| PHOTOPRISM_FFMPEG_SIZE                                           | --ffmpeg-size           |                                     4096 | maximum video size in `PIXELS` (720-7680)                       |
| PHOTOPRISM_FFMPEG_BITRATE                                        | --ffmpeg-bitrate        |                                       50 | maximum video `BITRATE` in Mbit/s                               |
| PHOTOPRISM_FFMPEG_MAP_VIDEO                                      | --ffmpeg-map-video      | `0:v:0`                                  | video `STREAMS` that should be transcoded                       |
| PHOTOPRISM_FFMPEG_MAP_AUDIO                                      | --ffmpeg-map-audio      | `0:a:0?`                                 | audio `STREAMS` that should be transcoded                       |
| PHOTOPRISM_EXIFTOOL_BIN                                          | --exiftool-bin          | exiftool                                 | ExifTool `COMMAND` for extracting metadata                      |
| PHOTOPRISM_SIPS_BIN                                              | --sips-bin              | sips                                     | Sips `COMMAND` for media file conversion *macOS only*           |
| PHOTOPRISM_SIPS_EXCLUDE, PHOTOPRISM_SIPS_BLACKLIST               | --sips-exclude          | avif, avifs, thm                         | file `EXTENSIONS` not to be used with Sips *macOS only*         |
| PHOTOPRISM_DARKTABLE_BIN                                         | --darktable-bin         | darktable-cli                            | Darktable CLI `COMMAND` for RAW to JPEG conversion              |
| PHOTOPRISM_DARKTABLE_EXCLUDE, PHOTOPRISM_DARKTABLE_BLACKLIST     | --darktable-exclude     | thm                                      | file `EXTENSIONS` not to be used with Darktable                 |
| PHOTOPRISM_DARKTABLE_CACHE_PATH                                  | --darktable-cache-path  |                                          | custom Darktable cache `PATH`                                   |
| PHOTOPRISM_DARKTABLE_CONFIG_PATH                                 | --darktable-config-path |                                          | custom Darktable config `PATH`                                  |
| PHOTOPRISM_RAWTHERAPEE_BIN                                       | --rawtherapee-bin       | rawtherapee-cli                          | RawTherapee CLI `COMMAND` for RAW to JPEG conversion            |
| PHOTOPRISM_RAWTHERAPEE_EXCLUDE, PHOTOPRISM_RAWTHERAPEE_BLACKLIST | --rawtherapee-exclude   | dng, thm                                 | file `EXTENSIONS` not to be used with RawTherapee               |
| PHOTOPRISM_IMAGEMAGICK_BIN                                       | --imagemagick-bin       | convert                                  | ImageMagick CLI `COMMAND` for image file conversion             |
| PHOTOPRISM_IMAGEMAGICK_EXCLUDE, PHOTOPRISM_IMAGEMAGICK_BLACKLIST | --imagemagick-exclude   | heif, heic, heics, avif, avifs, jxl, thm | file `EXTENSIONS` not to be used with ImageMagick               |
| PHOTOPRISM_HEIFCONVERT_BIN                                       | --heifconvert-bin       | heif-convert                             | libheif HEIC image conversion `COMMAND`                         |
| PHOTOPRISM_RSVGCONVERT_BIN                                       | --rsvgconvert-bin       | rsvg-convert                             | librsvg SVG graphics conversion `COMMAND` *plus*                |

### Security Tokens ###

|        Environment        |     CLI Flag     | Default |                                    Description                                     |
|---------------------------|------------------|---------|------------------------------------------------------------------------------------|
| PHOTOPRISM_DOWNLOAD_TOKEN | --download-token |         | `DEFAULT` download URL token for originals (leave blank for a random value)        |
| PHOTOPRISM_PREVIEW_TOKEN  | --preview-token  |         | `DEFAULT` thumbnail and video streaming URL token (leave blank for a random value) |

### Preview Images ###

|          Environment           |       CLI Flag        | Default |                                         Description                                          |
|--------------------------------|-----------------------|---------|----------------------------------------------------------------------------------------------|
| PHOTOPRISM_THUMB_LIBRARY       | --thumb-library       | auto    | image processing `LIBRARY` to be used for generating thumbnails (auto, imaging, vips)        |
| PHOTOPRISM_THUMB_COLOR         | --thumb-color         | auto    | standard color `PROFILE` for thumbnails (auto, preserve, srgb, none)                         |
| PHOTOPRISM_THUMB_FILTER        | --thumb-filter        | auto    | downscaling filter `NAME` (imaging best to worst: blackman, lanczos, cubic, linear, nearest) |
| PHOTOPRISM_THUMB_SIZE          | --thumb-size          |    1920 | maximum size of pre-generated thumbnails in `PIXELS` (720-7680)                              |
| PHOTOPRISM_THUMB_SIZE_UNCACHED | --thumb-size-uncached |    7680 | maximum size of thumbnails generated on demand in `PIXELS` (720-7680)                        |
| PHOTOPRISM_THUMB_UNCACHED      | --thumb-uncached      |         | generate missing thumbnails on demand (high memory and cpu usage)                            |

### Image Quality ###

|       Environment       |    CLI Flag    | Default |                            Description                            |
|-------------------------|----------------|---------|-------------------------------------------------------------------|
| PHOTOPRISM_JPEG_QUALITY | --jpeg-quality |      83 | higher values increase the image `QUALITY` and file size (25-100) |
| PHOTOPRISM_JPEG_SIZE    | --jpeg-size    |    7680 | maximum size of generated JPEG images in `PIXELS` (720-30000)     |
| PHOTOPRISM_PNG_SIZE     | --png-size     |    7680 | maximum size of generated PNG images in `PIXELS` (720-30000)      |

### Face Recognition ###

!!! info ""
    To [recognize faces](https://docs.photoprism.app/user-guide/organize/people/), PhotoPrism first extracts crops from your images using a [library](https://github.com/esimov/pigo) based on [pixel intensity comparisons](https://dl.photoprism.app/pdf/publications/20140820-Pixel_Intensity_Comparisons.pdf). These are then fed into TensorFlow to compute [512-dimensional vectors](https://dl.photoprism.app/pdf/20150101-FaceNet.pdf) for characterization. In the final step, the [DBSCAN algorithm](https://en.wikipedia.org/wiki/DBSCAN) attempts to cluster these so-called face embeddings, so they can be matched to persons with just a few clicks. A reasonable range for the similarity distance between face embeddings is between 0.60 and 0.70, with a higher value being more aggressive and leading to larger clusters with more false positives. To cluster a smaller number of faces, you can reduce the core to 3 or 2 similar faces.

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
| PHOTOPRISM_INIT          |         | run/install on first startup (options: update https gpu ffmpeg tensorflow davfs clitools clean)                                                                                              |
| PHOTOPRISM_DISABLE_CHOWN | false   | disable updating storage permissions via chmod and chown on startup                                                                                                                          |

[^1]: If you are using [Docker Compose](docker-compose.md), you can open a terminal, run `docker compose stop`, and then run `docker compose up -d` to restart all services.
[^2]: Enabling public mode is not recommended for instances installed on a server outside your home network, as this allows others to access your pictures without authentication.
