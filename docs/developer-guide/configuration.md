# Configuration

## Command-Line Interface ##

The `photoprism help` (or `photoprism --help`) command lists all supported subcommands and [config options](../getting-started/config-options.md) available in the current version:

```bash
./photoprism help
```

Run the following to display all global config options and their current values:

```bash
./photoprism show config
```

You can also use the `photoprism show` command to display supported search filters, file types, thumbnail sizes, and metadata tags:

```bash
./photoprism show --help
```

## Config Options ##

You can either use [environment variables](../getting-started/config-options.md) like `PHOTOPRISM_CACHE_PATH`, [config files](../getting-started/config-files/index.md) (in the `storage/config` directory) or command line parameters like `--cache-path` to change the value of config options.

[Learn more ›](../getting-started/config-options.md)

!!! note ""
    Changes to the [config options](../getting-started/config-options.md) always require a restart to take effect. For development purposes, you do not need to change any settings if you followed the steps described under [Build Setup](setup.md).