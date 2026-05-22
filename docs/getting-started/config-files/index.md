# `options.yml`

As an alternative to [configuring your instance with environment variables](../config-options.md), it may be more convenient to use an `options.yml` file located in your *config path*, for example if PhotoPrism was installed [through an app store](../nas/asustor.md) or with the [installation packages we provide](https://dl.photoprism.app/pkg/linux/README.html).

By default, the *config path* is a subdirectory of the [*storage path*](../docker-compose.md#photoprismstorage). You can specify a custom configuration path by setting a `ConfigPath` value in your ↪ [`defaults.yml`](defaults.md) file. You can also use the command flag `--config-path` or the [environment variable](../config-options.md#storage) `PHOTOPRISM_CONFIG_PATH` to specify a custom configuration directory.

Custom [config defaults](defaults.md) are automatically loaded from `/etc/photoprism/defaults.yml`. If that file is missing or empty, they are loaded from `<config-path>/defaults.yml` (or `.yaml`) instead. This allows you to set defaults in the regular config directory without modifying or mounting `/etc/photoprism`, which is useful in containerized environments and for non-root installations.

If you use a third-party integration or package, you should find the exact location of the configuration files in the corresponding documentation.

!!! tldr ""
    Note that changes to the `options.yml` file require a restart to take effect and
    that [config values changed through the web interface](../../user-guide/settings/advanced.md) will also be saved to this
    file. We therefore recommend that you only edit it manually while your instance is stopped.

### YAML File Format ###

You can use any text editor to [create or modify YAML config files](../../developer-guide/technologies/yaml.md). When
specifying values, make sure that [their data type matches the documentation](index.md#config-options), e.g. *bool*
values must be either `true` or `false` (without quotes,
unlike [in `compose.yaml` files](../../developer-guide/technologies/yaml.md#true-false)) and *int* values must be
whole numbers, as shown in [this example](https://dl.photoprism.app/pkg/linux/defaults.yml):

```yaml
Debug: false
AdminUser: "admin"
AdminPassword: "insecure"
DatabaseUser: "photoprism"
DatabasePassword: "insecure"
DatabaseName: "photoprism"
DatabaseDriver: "mysql"
DatabaseServer: "localhost:3306"
HttpPort: 2342
SiteCaption: "AI-Powered Photos App"
SiteDescription: ""
SiteAuthor: ""
SiteUrl: "http://localhost:2342/"
```

To avoid ambiguity, it is recommended to enclose text strings in `"` (double quotes), especially if they contain spaces,
a colon, or other special characters.

!!! note ""
    File and directory paths may be specified using `~` as a placeholder for the home directory of the current user, e.g. `~/Pictures`. Relative paths can also be specified via `./pathname`.
    If no explicit [*originals*](../docker-compose.md#photoprismoriginals), [*import*](../docker-compose.md#photoprismimport) and/or *assets* path has been configured, a list of [default directory paths](https://github.com/photoprism/photoprism/blob/develop/pkg/fs/directories.go) will be searched and the first existing directory will be used for the respective path.

## Sources and Precedence

PhotoPrism loads configuration values in the following order:

1. **Built-in defaults** defined in the [`internal/config`](https://github.com/photoprism/photoprism/blob/develop/internal/config) package.
2. **`defaults.yml`** — [configuration defaults](defaults.md) located in `/etc/photoprism` or the *config path*.
3. **Environment variables** prefixed with ↪ [`PHOTOPRISM_…`](../config-options.md). This is the primary override mechanism in Docker/Kubernetes container environments.
4. **`options.yml`** — [user-level configuration](#config-options) loaded from `<config-path>/options.yml`. Values here override both [configuration defaults](defaults.md) and [environment variables](../config-options.md).
5. **Command-line flags** (for example `photoprism --cache-path=/tmp/cache`). Flags always win when a conflict exists.

### Inspect Before Editing

Before changing [environment variables](../config-options.md#environment-variables) or YAML files, run `photoprism config | grep -i <flag>` to confirm the current values, such as for `password-length`:

```bash
photoprism config | grep -i password-length
```

## Config Options

Below are the names of the config options that you can set in the `options.yml` and ↪ [`defaults.yml`](defaults.md) configuration files, grouped by purpose.

### Authentication

| Name           | Type   | CLI Flag          |
|:---------------|:-------|:------------------|
| AuthMode       | string | --auth-mode       |
| Public         | bool   | --public          |
| AdminUser      | string | --admin-user      |
| AdminPassword  | string | --admin-password  |
| PasswordLength | int    | --password-length |
| OIDCUri        | string | --oidc-uri        |
| OIDCClient     | string | --oidc-client     |
| OIDCSecret     | string | --oidc-secret     |
| OIDCScopes     | string | --oidc-scopes     |
| OIDCProvider   | string | --oidc-provider   |
| OIDCIcon       | string | --oidc-icon       |
| OIDCRedirect   | bool   | --oidc-redirect   |
| OIDCRegister   | bool   | --oidc-register   |
| OIDCUsername   | string | --oidc-username   |
| OIDCWebDAV     | bool   | --oidc-webdav     |
| DisableOIDC    | bool   | --disable-oidc    |
| SessionMaxAge  | int64  | --session-maxage  |
| SessionTimeout | int64  | --session-timeout |
| SessionCache   | int64  | --session-cache   |

### Logging

| Name     | Type   | CLI Flag    |
|:---------|:-------|:------------|
| LogLevel | string | --log-level |
| Prod     | bool   | --prod      |
| Debug    | bool   | --debug     |
| Trace    | bool   | --trace     |

### Storage

| Name            | Type   | CLI Flag           |
|:----------------|:-------|:-------------------|
| ConfigPath      | string | --config-path      |
| OriginalsPath   | string | --originals-path   |
| OriginalsLimit  | int    | --originals-limit  |
| ResolutionLimit | int    | --resolution-limit |
| UsersPath       | string | --users-path       |
| StoragePath     | string | --storage-path     |
| ImportPath      | string | --import-path      |
| ImportDest      | string | --import-dest      |
| ImportAllow     | string | --import-allow     |
| UploadNSFW      | bool   | --upload-nsfw      |
| UploadAllow     | string | --upload-allow     |
| UploadArchives  | bool   | --upload-archives  |
| UploadLimit     | int    | --upload-limit     |
| CachePath       | string | --cache-path       |
| TempPath        | string | --temp-path        |
| AssetsPath      | string | --assets-path      |
| ModelsPath      | string | --models-path      |

### Sidecar Files

| Name        | Type   | CLI Flag       |
|:------------|:-------|:---------------|
| SidecarPath | string | --sidecar-path |
| SidecarYaml | bool   | --sidecar-yaml |

### Usage

| Name       | Type   | CLI Flag      |
|:-----------|:-------|:--------------|
| UsageInfo  | bool   | --usage-info  |
| FilesQuota | uint64 | --files-quota |

### Backup

| Name           | Type   | CLI Flag          |
|:---------------|:-------|:------------------|
| BackupPath     | string | --backup-path     |
| BackupSchedule | string | --backup-schedule |
| BackupRetain   | int    | --backup-retain   |
| BackupDatabase | bool   | --backup-database |
| BackupAlbums   | bool   | --backup-albums   |

### Indexing

| Name           | Type          | CLI Flag          |
|:---------------|:--------------|:------------------|
| IndexWorkers   | int           | --index-workers   |
| IndexSchedule  | string        | --index-schedule  |
| WakeupInterval | time.Duration | --wakeup-interval |
| AutoIndex      | int           | --auto-index      |
| AutoImport     | int           | --auto-import     |

### Feature Flags

| Name                  | Type | CLI Flag                 |
|:----------------------|:-----|:-------------------------|
| ReadOnly              | bool | --read-only              |
| Experimental          | bool | --experimental           |
| DisableFrontend       | bool | --disable-frontend       |
| DisableSettings       | bool | --disable-settings       |
| DisableBackups        | bool | --disable-backups        |
| DisableRestart        | bool | --disable-restart        |
| DisableWebDAV         | bool | --disable-webdav         |
| DisablePlaces         | bool | --disable-places         |
| DisableTensorFlow     | bool | --disable-tensorflow     |
| DisableFaces          | bool | --disable-faces          |
| DisableClassification | bool | --disable-classification |
| DisableFFmpeg         | bool | --disable-ffmpeg         |
| DisableExifTool       | bool | --disable-exiftool       |
| DisableSips           | bool | --disable-sips           |
| DisableDarktable      | bool | --disable-darktable      |
| DisableRawTherapee    | bool | --disable-rawtherapee    |
| DisableImageMagick    | bool | --disable-imagemagick    |
| DisableHeifConvert    | bool | --disable-heifconvert    |
| DisableVectors        | bool | --disable-vectors        |
| DisableJpegXL         | bool | --disable-jpegxl         |
| DisableRaw            | bool | --disable-raw            |
| RawPresets            | bool | --raw-presets            |
| ExifBruteForce        | bool | --exif-bruteforce        |

### Customization

| Name            | Type   | CLI Flag           |
|:----------------|:-------|:-------------------|
| DefaultLocale   | string | --default-locale   |
| DefaultTimezone | string | --default-timezone |
| DefaultTheme    | string | --default-theme    |
| PlacesLocale    | string | --places-locale    |
| AppName         | string | --app-name         |
| AppMode         | string | --app-mode         |
| AppIcon         | string | --app-icon         |
| AppColor        | string | --app-color        |
| LegalInfo       | string | --legal-info       |
| LegalUrl        | string | --legal-url        |
| WallpaperUri    | string | --wallpaper-uri    |

### Site Information

| Name            | Type   | CLI Flag           |
|:----------------|:-------|:-------------------|
| SiteUrl         | string | --site-url         |
| SiteAuthor      | string | --site-author      |
| SiteTitle       | string | --site-title       |
| SiteCaption     | string | --site-caption     |
| SiteDescription | string | --site-description |
| SiteFavicon     | string | --site-favicon     |
| SitePreview     | string | --site-preview     |
| CdnUrl          | string | --cdn-url          |
| CdnVideo        | bool   | --cdn-video        |
| CORSOrigin      | string | --cors-origin      |
| CORSHeaders     | string | --cors-headers     |
| CORSMethods     | string | --cors-methods     |

### Networking

| Name               | Type     | CLI Flag               |
|:-------------------|:---------|:-----------------------|
| HttpsProxy         | string   | --https-proxy          |
| HttpsProxyInsecure | bool     | --https-proxy-insecure |
| TrustedPlatform    | string   | --trusted-platform     |
| TrustedProxies     | []string | --trusted-proxy        |
| ProxyClientHeaders | []string | --proxy-client-header  |
| ProxyProtoHeaders  | []string | --proxy-proto-header   |
| ProxyProtoHttps    | []string | --proxy-proto-https    |
| ServicesCIDR       | string   | --services-cidr        |

### Web Server

| Name              | Type          | CLI Flag              |
|:------------------|:--------------|:----------------------|
| DisableTLS        | bool          | --disable-tls         |
| DefaultTLS        | bool          | --default-tls         |
| TLSEmail          | string        | --tls-email           |
| TLSCert           | string        | --tls-cert            |
| TLSKey            | string        | --tls-key             |
| HttpMode          | string        | --http-mode           |
| HttpCompression   | string        | --http-compression    |
| HttpHeaderTimeout | time.Duration | --http-header-timeout |
| HttpHeaderBytes   | int           | --http-header-bytes   |
| HttpIdleTimeout   | time.Duration | --http-idle-timeout   |
| HttpCachePublic   | bool          | --http-cache-public   |
| HttpCacheMaxAge   | int           | --http-cache-maxage   |
| HttpVideoMaxAge   | int           | --http-video-maxage   |
| HttpHost          | string        | --http-host           |
| HttpPort          | int           | --http-port           |

### Database Connection

| Name                      | Type   | CLI Flag                       |
|:--------------------------|:-------|:-------------------------------|
| DatabaseDriver            | string | --database-driver              |
| DatabaseDSN               | string | --database-dsn                 |
| DatabaseName              | string | --database-name                |
| DatabaseServer            | string | --database-server              |
| DatabaseUser              | string | --database-user                |
| DatabasePassword          | string | --database-password            |
| DatabaseTimeout           | int    | --database-timeout             |
| DatabaseConns             | int    | --database-conns               |
| DatabaseConnsIdle         | int    | --database-conns-idle          |
| DatabaseProvisionDriver   | string | --database-provision-driver    |
| DatabaseProvisionPrefix   | string | --database-provision-prefix    |
| DatabaseProvisionDSN      | string | --database-provision-dsn       |
| DatabaseProvisionProxyDSN | string | --database-provision-proxy-dsn |

### File Conversion

| Name                   | Type   | CLI Flag                  |
|:-----------------------|:-------|:--------------------------|
| FFmpegBin              | string | --ffmpeg-bin              |
| FFmpegEncoder          | string | --ffmpeg-encoder          |
| FFmpegSize             | int    | --ffmpeg-size             |
| FFmpegQuality          | int    | --ffmpeg-quality          |
| FFmpegBitrate          | int    | --ffmpeg-bitrate          |
| FFmpegPreset           | string | --ffmpeg-preset           |
| FFmpegDevice           | string | --ffmpeg-device           |
| FFmpegMapVideo         | string | --ffmpeg-map-video        |
| FFmpegMapAudio         | string | --ffmpeg-map-audio        |
| ExifToolBin            | string | --exiftool-bin            |
| SipsBin                | string | --sips-bin                |
| SipsExclude            | string | --sips-exclude            |
| DarktableBin           | string | --darktable-bin           |
| DarktableCachePath     | string | --darktable-cache-path    |
| DarktableConfigPath    | string | --darktable-config-path   |
| DarktableExclude       | string | --darktable-exclude       |
| RawTherapeeBin         | string | --rawtherapee-bin         |
| RawTherapeeExclude     | string | --rawtherapee-exclude     |
| ImageMagickBin         | string | --imagemagick-bin         |
| ImageMagickExclude     | string | --imagemagick-exclude     |
| HeifConvertBin         | string | --heifconvert-bin         |
| HeifConvertOrientation | string | --heifconvert-orientation |
| RsvgConvertBin         | string | --rsvgconvert-bin         |

### Security Tokens

| Name          | Type   | CLI Flag         |
|:--------------|:-------|:-----------------|
| DownloadToken | string | --download-token |
| PreviewToken  | string | --preview-token  |

### Preview Images

| Name              | Type   | CLI Flag              |
|:------------------|:-------|:----------------------|
| ThumbLibrary      | string | --thumb-library       |
| ThumbColor        | string | --thumb-color         |
| ThumbSize         | int    | --thumb-size          |
| ThumbSizeUncached | int    | --thumb-size-uncached |
| ThumbUncached     | bool   | --thumb-uncached      |

### Image Quality

| Name        | Type | CLI Flag       |
|:------------|:-----|:---------------|
| JpegQuality | int  | --jpeg-quality |
| JpegSize    | int  | --jpeg-size    |
| PngSize     | int  | --png-size     |

### Computer Vision

| Name           | Type   | CLI Flag          |
|:---------------|:-------|:------------------|
| VisionYaml     | string | --vision-yaml     |
| VisionApi      | bool   | --vision-api      |
| VisionUri      | string | --vision-uri      |
| VisionKey      | string | --vision-key      |
| VisionSchedule | string | --vision-schedule |
| VisionFilter   | string | --vision-filter   |
| DetectNSFW     | bool   | --detect-nsfw     |

### Face Recognition

| Name              | Type   | CLI Flag              |
|:------------------|:-------|:----------------------|
| FaceEngine        | string | --face-engine         |
| FaceEngineThreads | int    | --face-engine-threads |

### Daemon Mode

If you start the server as a *daemon* in the background, you can additionally specify a filename for the log and the process ID:

| Name         | Type   | CLI Flag        |
|:-------------|:-------|:----------------|
| PIDFilename  | string | --pid-filename  |
| LogFilename  | string | --log-filename  |
| DetachServer | bool   | --detach-server |
