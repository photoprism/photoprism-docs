# Introduction to YAML

[YAML](https://en.wikipedia.org/wiki/YAML) is a human-friendly format that we use for [metadata exports](../../user-guide/backups/export.md) and [configuration files](../../getting-started/config-files/index.md) because of its simplicity and widespread support. The name originally meant *Yet Another Markup Language*. Common file extensions are `.yml`and `.yaml`.

Values are represented in the form `key: value` with one entry per line:

```yaml
Type: image
Title: "La Tour Eiffel 🌈"
Year: 2014
# Key-Value Collection Example:
Details:
  Notes: "Bonjour\nla France!" 
  Keywords: 'paris, france' # Comment
```

## Basic Rules ##

- Keys are case-sensitive
- Related values start at the same indentation level
    - Tabs are not allowed for indentation
    - We recommend using 2 spaces, but any number will work as long as it is consistent
- You can generally use all [Unicode](https://home.unicode.org/basic-info/faq/) characters in YAML files, including [Emojis](https://home.unicode.org/emoji/about-emoji/)
    - To avoid ambiguity, it is recommended to enclose text strings in single `'` or double quotes `"`, especially if they contain spaces, a colon, or other special characters
    - The difference between single and double quotes is that double quotes support [escape sequences](https://symfony.com/doc/current/components/yaml/yaml_format.html#strings) like `\t` for a tab or `\n` for a new line
- Comments begin with the `#` sign, can start anywhere on a line, and continue until the end of the line

### Multiple Values ###

List are lines that start at the same indentation level and begin with a dash and a space as shown in the example below.
They are commonly used to define service dependencies, exposed network ports, or folders shared between host and
container in `docker-compose.yml` files:

```yaml
services:
  photoprism:
    depends_on:
      - mariadb
      - nextcloud
    ports:
      # "host:container"
      - "2342:2342"
    volumes:
      # "/host/folder:/container/folder"
      - "/photos:/photoprism/originals"
```

### Key-Value Pairs ###

Collections of key-value pairs are commonly used to set the names and values of environment variables in `docker-compose.yml` files (see below for [additional rules](#docker-compose)):

```yaml
services:
  mariadb:
    environment:
      MARIADB_AUTO_UPGRADE: "1"
      MARIADB_INITDB_SKIP_TZINFO: "1"
      MARIADB_ROOT_PASSWORD: "Y(&^UIk34"
      MARIADB_DATABASE: photoprism
      MARIADB_USER: photoprism
      MARIADB_PASSWORD: insecure
```

## Docker Compose ##

When using [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/), some additional rules apply, as `docker-compose.yml` files extend the YAML format with features such as [variable interpolation](https://docs.docker.com/compose/compose-file/12-interpolation/#interpolation).

### Dollar Signs ###

If a configuration value [in a `docker-compose.yml` file](../../getting-started/docker-compose.md) contains a literal `$` character, for example in a password, you must use `$$` (a double dollar sign) to escape it so that e.g. `"compo$e"` becomes `"compo$$e"`:

```yaml
services:
  mariadb:
    environment:
      # sets password to "compo$e"
      MARIADB_PASSWORD: "compo$$e" 
```

Values that contain a `$` are otherwise [interpreted as a variable](https://docs.docker.com/compose/compose-file/12-interpolation/#interpolation). In this case, both the `$VARIABLE` and the `${VARIABLE}` syntax are supported. Further details on the use of variables can be found in the [file format reference](https://docs.docker.com/compose/compose-file/12-interpolation/#interpolation).

### True / False ###

Boolean environment variable values like "true", "false", "yes", "no", "on", or "off" must be enclosed in quotes so that they are passed as intended:

```yaml
services:
  photoprism:
    environment:
      PHOTOPRISM_DEFAULT_TLS: "true"
      PHOTOPRISM_READONLY: "false"
```

If you otherwise specify `true` as a value without quotes, [Docker Compose](https://docs.docker.com/compose/compose-file/compose-file-v3/) will pass the host variable of the same name to the container instead of setting the value to "true" (results in an empty string if no environment variable with the same name is set on the host):

```yaml
services:
  photoprism:
    environment:
      # evaluated as "" (false)
      PHOTOPRISM_READONLY: true
```

*[Keys]: the names of values
*[tab]: a tab advances the cursor to the next tab stop
*[key-value]: a key-value pair consists of two related data elements
