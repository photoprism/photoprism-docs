# `options.yml`

If you are unable to configure your instance using [environment variables or command flags](../config-options.md), for example because it was installed through an app store, you can alternatively set config values using an `options.yml` file in the *config path*.

You can specify a custom *config path* by adding the `ConfigPath` option to a ↪ [`defaults.yml`](defaults.md) file in the `/etc/photoprism` directory (requires root privileges). It is also possible to use the command flag `--config-path` or the environment variable `PHOTOPRISM_CONFIG_PATH` for this. By default, it is a subdirectory of the [*storage path*](../docker-compose.md#photoprismstorage).

If you use a third-party integration or package, you should find the exact location of the configuration files in the corresponding documentation.

!!! tldr ""
    Changes to the [config options](#config-options) always require a restart to take effect. Also note that config values changed in the [Advanced Settings](../../user-guide/settings/advanced.md) UI are stored in the `options.yml` file. We therefore recommend that you only change it manually while your instance is stopped.

### File Format ###

You can use any text editor to [create or modify YAML config files](../../developer-guide/technologies/yaml.md). When specifying values, make sure that [their data type matches the documentation](index.md#config-options), e.g. *bool* values must be either `true` or `false` (without quotes, unlike [in `docker-compose.yml` files](../../developer-guide/technologies/yaml.md#true-false)) and *int* values must be whole numbers, as shown in [this example](https://dl.photoprism.app/pkg/linux/defaults.yml):

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

To avoid ambiguity, it is recommended to enclose text strings in `"` (double quotes), especially if they contain spaces, a colon, or other special characters.

!!! note ""
    File and directory paths may be specified using `~` as a placeholder for the home directory of the current user, e.g. `~/Pictures`. Relative paths can also be specified via `./pathname`.
    If no explicit [*originals*](../docker-compose.md#photoprismoriginals), [*import*](../docker-compose.md#photoprismimport) and/or *assets* path has been configured, a list of [default directory paths](https://github.com/photoprism/photoprism/blob/develop/pkg/fs/dirs.go) will be searched and the first existing directory will be used for the respective path.

### Global Defaults

Global [configuration defaults](defaults.md), including the storage paths to be used, can optionally be specified in a ↪ [`defaults.yml`](defaults.md) file.

### Current Values

Run `photoprism --help` in [a terminal](../docker-compose.md#command-line-interface) to get an [overview of the command flags and environment variables](config-options.md) available for configuration. Their current values can be displayed with the `photoprism config` command.

Below are the corresponding names of the config options that you can use in the `options.yml` and [`defaults.yml`](defaults.md) files, grouped by purpose.

## Config Options
### Authentication ###
|       Name       |  Type  |       CLI Flag       |
|------------------|--------|----------------------|
| AuthMode         | string | --auth-mode          |
| Public           | bool   | --public             |
| AdminUser        | string | --admin-user         |
| AdminPassword    | string | --admin-password     |
| PasswordLength   | int    | --password-length    |
| SessionMaxAge    | int64  | --session-maxage     |
| SessionTimeout   | int64  | --session-timeout    |

### Logging ###

|   Name   |  Type  |  CLI Flag   |
|----------|--------|-------------|
| LogLevel | string | --log-level |
| Prod     | bool   | --prod      |
| Debug    | bool   | --debug     |
| Trace    | bool   | --trace     |

### Storage ###

|      Name       |  Type  |      CLI Flag      |
|-----------------|--------|--------------------|
| ConfigPath      | string | --config-path      |
| OriginalsPath   | string | --originals-path   |
| OriginalsLimit  | int    | --originals-limit  |
| ResolutionLimit | int    | --resolution-limit |
| UsersPath       | string | --users-path       |
| StoragePath     | string | --storage-path     |
| SidecarPath     | string | --sidecar-path     |
| BackupPath      | string | --backup-path      |
| CachePath       | string | --cache-path       |
| ImportPath      | string | --import-path      |
| ImportDest      | string | --import-dest      |
| AssetsPath      | string | --assets-path      |
| TempPath        | string | --temp-path        |

### Index Workers ###

|      Name      |     Type      |     CLI Flag      |
|----------------|---------------|-------------------|
| Workers        | int           | --workers         |
| WakeupInterval | time.Duration | --wakeup-interval |
| AutoIndex      | int           | --auto-index      |
| AutoImport     | int           | --auto-import     |

### Feature Flags ###

|         Name          | Type |         CLI Flag         |
|-----------------------|------|--------------------------|
| ReadOnly              | bool | --read-only              |
| Experimental          | bool | --experimental           |
| DisableSettings       | bool | --disable-settings       |
| DisableRestart        | bool | --disable-restart        |
| DisableBackups        | bool | --disable-backups        |
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
| DetectNSFW            | bool | --detect-nsfw            |
| UploadNSFW            | bool | --upload-nsfw            |

### Customization ###

|     Name      |  Type  |     CLI Flag     |
|---------------|--------|------------------|
| DefaultTheme  | string | --default-theme  |
| DefaultLocale | string | --default-locale |
| AppName       | string | --app-name       |
| AppMode       | string | --app-mode       |
| AppIcon       | string | --app-icon       |
| AppColor      | string | --app-color      |
| LegalInfo     | string | --legal-info     |
| LegalUrl      | string | --legal-url      |
| WallpaperUri  | string | --wallpaper-uri  |

### Site Information ###

|      Name       |  Type  |      CLI Flag      |
|-----------------|--------|--------------------|
| CdnUrl          | string | --cdn-url          |
| CdnVideo        | bool   | --cdn-video        |
| SiteUrl         | string | --site-url         |
| SiteAuthor      | string | --site-author      |
| SiteTitle       | string | --site-title       |
| SiteCaption     | string | --site-caption     |
| SiteDescription | string | --site-description |
| SitePreview     | string | --site-preview     |

### Web Server ###

|        Name        |   Type   |        CLI Flag        |
|--------------------|----------|------------------------|
| HttpsProxy         | string   | --https-proxy          |
| HttpsProxyInsecure | bool     | --https-proxy-insecure |
| TrustedProxies     | []string | --trusted-proxy        |
| ProxyProtoHeaders  | []string | --proxy-proto-header   |
| ProxyProtoHttps    | []string | --proxy-proto-https    |
| DisableTLS         | bool     | --disable-tls          |
| DefaultTLS         | bool     | --default-tls          |
| TLSEmail           | string   | --tls-email            |
| TLSCert            | string   | --tls-cert             |
| TLSKey             | string   | --tls-key              |
| HttpMode           | string   | --http-mode            |
| HttpCompression    | string   | --http-compression     |
| HttpCachePublic    | bool     | --http-cache-public    |
| HttpCacheMaxAge    | int      | --http-cache-maxage    |
| HttpVideoMaxAge    | int      | --http-video-maxage    |
| HttpHost           | string   | --http-host            |
| HttpPort           | int      | --http-port            |

### Database Connection ###

|       Name        |  Type  |       CLI Flag        |
|-------------------|--------|-----------------------|
| DatabaseDriver    | string | --database-driver     |
| DatabaseDsn       | string | --database-dsn        |
| DatabaseName      | string | --database-name       |
| DatabaseServer    | string | --database-server     |
| DatabaseUser      | string | --database-user       |
| DatabasePassword  | string | --database-password   |
| DatabaseConns     | int    | --database-conns      |
| DatabaseConnsIdle | int    | --database-conns-idle |

### File Converters ###

|         Name         |  Type  |        CLI Flag         |
|----------------------|--------|-------------------------|
| SipsBin              | string | --sips-bin              |
| SipsBlacklist        | string | --sips-blacklist        |
| FFmpegBin            | string | --ffmpeg-bin            |
| FFmpegEncoder        | string | --ffmpeg-encoder        |
| FFmpegSize           | int    | --ffmpeg-size           |
| FFmpegBitrate        | int    | --ffmpeg-bitrate        |
| FFmpegMapVideo       | string | --ffmpeg-map-video      |
| FFmpegMapAudio       | string | --ffmpeg-map-audio      |
| ExifToolBin          | string | --exiftool-bin          |
| DarktableBin         | string | --darktable-bin         |
| DarktableCachePath   | string | --darktable-cache-path  |
| DarktableConfigPath  | string | --darktable-config-path |
| DarktableBlacklist   | string | --darktable-blacklist   |
| RawTherapeeBin       | string | --rawtherapee-bin       |
| RawTherapeeBlacklist | string | --rawtherapee-blacklist |
| ImageMagickBin       | string | --imagemagick-bin       |
| ImageMagickBlacklist | string | --imagemagick-blacklist |
| HeifConvertBin       | string | --heifconvert-bin       |
| RsvgConvertBin       | string | --rsvgconvert-bin       |

### Security Tokens ###

|     Name      |  Type  |     CLI Flag     |
|---------------|--------|------------------|
| DownloadToken | string | --download-token |
| PreviewToken  | string | --preview-token  |

### Image Quality ###

|       Name        |  Type  |       CLI Flag        |
|-------------------|--------|-----------------------|
| ThumbColor        | string | --thumb-color         |
| ThumbFilter       | string | --thumb-filter        |
| ThumbSize         | int    | --thumb-size          |
| ThumbSizeUncached | int    | --thumb-size-uncached |
| ThumbUncached     | bool   | --thumb-uncached      |
| JpegQuality       | string | --jpeg-quality        |
| JpegSize          | int    | --jpeg-size           |
| PngSize           | int    | --png-size            |

### Daemon Mode ###

If you start the server as a *daemon* in the background, you can additionally specify a filename for the log and the process ID:

|     Name     |  Type  |    CLI Flag     |
|--------------|--------|-----------------|
| PIDFilename  | string | --pid-filename  |
| LogFilename  | string | --log-filename  |
| DetachServer | bool   | --detach-server |