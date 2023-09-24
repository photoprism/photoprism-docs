# `options.yml`

If you are unable to configure your instance using [environment variables or command flags](../config-options.md), for example because it was installed through an app store, you can alternatively set config values using an `options.yml` file in the *config* folder.

A custom *config* path can be specified with the variable `PHOTOPRISM_CONFIG_PATH` or the flag `--config-path`. If you use a third-party integration or package, you should find the exact location in the corresponding documentation. By default, it is a subdirectory of the [*storage* folder](../docker-compose.md#photoprismstorage).

!!! tldr ""
    All changes require a restart to take effect. Also note that config values changed in the [Advanced Settings](../../user-guide/settings/advanced.md) UI will be stored in the same file. We therefore recommend that you edit the file only while PhotoPrism is not running.

### Format

When [editing YAML files](../../developer-guide/technologies/yaml.md), it is important that related values start at the same indentation level and that spaces are used, since tabs are not allowed. You can use any text editor for this.

### Example

Since you only need to specify the values you want to change, an `options.yml` file doesn't have to contain all possible options and could look like this, for example:

```yaml
Debug: true
ReadOnly: false
JpegQuality: 83
SiteCaption: PhotoPrism
SiteUrl: "http://127.0.0.1:2342/"
```

### Values

To display all global config flags and variables, you can run `photoprism --help` in a [terminal](../docker-compose.md#command-line-interface). The corresponding config option names to use in the `options.yml` and [`defaults.yml`](defaults.md) files are listed below, grouped by purpose.

### Defaults

Default values, including the *config* path to use, may optionally be specified in a [`defaults.yml` file](defaults.md) located in `/etc/photoprism`. A custom default config filename can be set with the `PHOTOPRISM_DEFAULTS_YAML` variable or the `--defaults-yaml` flag.

## Config Options
### Authentication ###

|       Name       |  Type  |       CLI Flag       |
|------------------|--------|----------------------|
| AuthMode         | string | --auth-mode          |
| RegisterUri      | string | --register-uri       |
| PasswordLength   | int    | --password-length    |
| PasswordResetUri | string | --password-reset-uri |
| Public           | bool   | --public             |
| AdminUser        | string | --admin-user         |
| AdminPassword    | string | --admin-password     |
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

|        Name        |  Type  |        CLI Flag        |
|--------------------|--------|------------------------|
| CdnUrl             | string | --cdn-url              |
| CdnVideo           | bool   | --cdn-video            |
| SiteUrl            | string | --site-url             |
| SiteAuthor         | string | --site-author          |
| SiteTitle          | string | --site-title           |
| SiteCaption        | string | --site-caption         |
| SiteDescription    | string | --site-description     |
| SitePreview        | string | --site-preview         |
| HttpsProxy         | string | --https-proxy          |
| HttpsProxyInsecure | bool   | --https-proxy-insecure |

### Web Server ###

|       Name        |   Type   |       CLI Flag       |
|-------------------|----------|----------------------|
| TrustedProxies    | []string | --trusted-proxy      |
| ProxyProtoHeaders | []string | --proxy-proto-header |
| ProxyProtoHttps   | []string | --proxy-proto-https  |
| DisableTLS        | bool     | --disable-tls        |
| DefaultTLS        | bool     | --default-tls        |
| TLSEmail          | string   | --tls-email          |
| TLSCert           | string   | --tls-cert           |
| TLSKey            | string   | --tls-key            |
| HttpMode          | string   | --http-mode          |
| HttpCompression   | string   | --http-compression   |
| HttpCacheMaxAge   | int      | --http-cache-maxage  |
| HttpVideoMaxAge   | int      | --http-video-maxage  |
| HttpCachePublic   | bool     | --http-cache-public  |
| HttpHost          | string   | --http-host          |
| HttpPort          | int      | --http-port          |

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
| SipsBin           | string | --sips-bin            |
| SipsBlacklist     | string | --sips-blacklist      |
| FFmpegBin         | string | --ffmpeg-bin          |
| FFmpegEncoder     | string | --ffmpeg-encoder      |
| FFmpegSize        | int    | --ffmpeg-size         |
| FFmpegBitrate     | int    | --ffmpeg-bitrate      |
| FFmpegMapVideo    | string | --ffmpeg-map-video    |
| FFmpegMapAudio    | string | --ffmpeg-map-audio    |
| ExifToolBin       | string | --exiftool-bin        |

### File Converters ###

|         Name         |  Type  |        CLI Flag         |
|----------------------|--------|-------------------------|
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