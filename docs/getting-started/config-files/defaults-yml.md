# `defaults.yml`

Default values, including the *config* path to use, may optionally be specified in a `defaults.yml` file located in `/etc/photoprism`. Write permissions are not required, since all changes will be stored in the `options.yml` file.

With the variable `PHOTOPRISM_DEFAULTS_YAML` or the flag `--defaults-yaml`, you can also specify a custom defaults file to be loaded when PhotoPrism starts.

The default values can be overridden by values in an [`options.yml`](index.md) file, command flags, and environment variables. As with all global [config options](../config-options.md), changes require a restart to take effect.

### Example

Since you only need to specify the values for which you want to set a default, a `defaults.yml` file does not need to contain all possible options and could look like this, for example:

```yaml
Debug: false
ReadOnly: true
JpegQuality: 85
TrustedProxies:
  - "172.16.0.0/12"
  - "10.0.0.0/8"
```

When editing YAML files, please note that related values must [start at the same indentation level](../../developer-guide/technologies/yaml.md) and that tabs are not allowed for indentation.

### Config Options

↪ see [`options.yml`](index.md#authentication)
