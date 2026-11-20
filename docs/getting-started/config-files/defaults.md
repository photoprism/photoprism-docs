# `defaults.yml`

Global config defaults, including the *config* and *storage* paths to be used, can be defined [with a `defaults.yml` file](https://dl.photoprism.app/pkg/linux/defaults.yml). PhotoPrism automatically checks for `/etc/photoprism/defaults.yml` (or `.yaml`) first and, when the system file is missing or empty, falls back to `<config-path>/defaults.yml` (also `.yaml`) under `PHOTOPRISM_CONFIG_PATH`, which is useful in containerized environments and for non-root installations. You can override the lookup entirely by pointing the environment variable `PHOTOPRISM_DEFAULTS_YAML` or the command flag `--defaults-yaml` to another file.

PhotoPrism resolves these files in the following order:

1. `PHOTOPRISM_DEFAULTS_YAML` / `--defaults-yaml` (only if the referenced file exists and is readable)
2. `/etc/photoprism/defaults.yml` or `/etc/photoprism/defaults.yaml`
3. `<config-path>/defaults.yml` or `<config-path>/defaults.yaml` (the config path defaults to `storage/config`)

Keep in mind that any changes to the config options, either [through the UI](../../user-guide/settings/advanced.md), [config files](index.md), or by [setting environment variables](../config-options.md), always require a restart to take effect.

!!! tldr ""
    A `defaults.yml` file affects all users and should only contain options for which you want to set a global default.

The example below is intended for users of our [installation packages](https://dl.photoprism.app/pkg/linux/README.html). When running PhotoPrism in a container, e.g. with [Docker Compose](../docker-compose.md) or Podman, we recommend [configuring it with environment variables](../config-options.md) instead.

### YAML File Format ###

You can use any text editor to [create or modify YAML config files](../../developer-guide/technologies/yaml.md). When specifying values, make sure that [their data type matches the documentation](index.md#config-options), e.g. *bool* values must be either `true` or `false` (without quotes, unlike [in `compose.yaml` files](../../developer-guide/technologies/yaml.md#true-false)) and *int* values must be whole numbers, as shown in [this example](https://dl.photoprism.app/pkg/linux/defaults.yml):

```yaml
ConfigPath: "~/.config/photoprism"
StoragePath: "~/.photoprism"
OriginalsPath: "~/Pictures"
ImportPath: "/media"
AdminUser: "admin"
AdminPassword: "insecure"
AuthMode: "password"
DatabaseDriver: "sqlite"
HttpHost: "127.0.0.1"
HttpPort: 2342
HttpCompression: "gzip"
DisableTLS: false
DefaultTLS: true
Experimental: false
DisableWebDAV: false
DisableSettings: false
DisableTensorFlow: false
DisableFaces: false
DisableClassification: false
DisableVectors: false
DisableRaw: false
RawPresets: false
JpegQuality: 85
DetectNSFW: false
UploadNSFW: true
```

!!! danger ""
    The `AdminPassword` value only serves as the initial password of the admin account and should be changed after the first login. Since a `defaults.yml` file may be shared by multiple users on a server, a password set there is not considered secure. Instance-specific settings such as passwords belong in an [`options.yml`](index.md) file that only the user running PhotoPrism can read, e.g. with `chmod 600 options.yml`.

To avoid ambiguity, it is recommended to enclose text strings in `"` (double quotes), especially if they contain spaces, a colon, or other special characters.

!!! note ""
    File and directory paths may be specified using `~` as a placeholder for the home directory of the current user, e.g. `~/Pictures`. Relative paths can also be specified via `./pathname`.
    If no explicit [*originals*](../docker-compose.md#photoprismoriginals), [*import*](../docker-compose.md#photoprismimport) and/or *assets* path has been configured, a list of [default directory paths](https://github.com/photoprism/photoprism/blob/develop/pkg/fs/directories.go) will be searched and the first existing directory will be used for the respective path.

### Supported Options ###

↪ see [`options.yml`](index.md#config-options)

### Overriding Defaults ###

Defaults can be overridden by values in [an `options.yml` file](index.md) as well as by [command flags and environment variables](../config-options.md). PhotoPrism evaluates settings in this order, with each step overriding the previous one when a key is present: built-in defaults → the resolved `defaults.yml` file → environment variables → `options.yml` → CLI flags. Changes made through the web UI are persisted back to `options.yml`, so they follow the same precedence.

To override values with an `options.yml` file, you can specify its path (without the file name) by adding the `ConfigPath` option to your `defaults.yml`. Alternatively, you can use the command flag `--config-path` or the environment variable `PHOTOPRISM_CONFIG_PATH`. By default, it is located in the *config* subdirectory of the [*storage path*](../docker-compose.md#photoprismstorage).

The values in an `options.yml` file are not global by default and can be used to customize individual instances.
In both files you can set any of the [supported options](index.md#config-options).
