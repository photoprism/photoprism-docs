# `defaults.yml`

Default values, including the *config* path to use, may optionally be specified in a `defaults.yml` file located in `/etc/photoprism`, unless you have set a custom filename with the `--defaults-yaml` flag.

These defaults can be overridden by values in the `options.yml` file, command flags, and environment variables. While the `options.yml` file should be writable, the `defaults.yml` file may be read-only.

!!! tldr ""
    Note that that all changes require a restart to take effect.

## Example

Since you only need to specify the values for which you want to set a default, a `defaults.yml` file does not need to contain all possible options and could look like this, for example:

```yaml
Debug: false
ReadOnly: true
JpegQuality: 85
TrustedProxies:
  - "172.16.0.0/12"
  - "10.0.0.0/8"
```

When editing YAML files, please note that related values must [start at the same indentation level](../../developer-guide/technologies/yaml.md) and that tabs are not allowed for indentation. We recommend using 2 spaces when specifying a list of values e.g. of type `[]string` in the options overview below. You can use any text editor for this.

## Config Options

↪ see [`options.yml`](index.md)
