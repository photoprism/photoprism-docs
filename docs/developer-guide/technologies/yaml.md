# Introduction to YAML

[YAML](https://en.wikipedia.org/wiki/YAML) is a human-readable markup language. PhotoPrism uses it for metadata 
backups and config files because of its simplicity and widespread support in other applications and tools 
like [Docker Compose](https://dl.photoprism.app/docker/docker-compose.yml).

Commonly used file extensions are `.yml` and `.yaml`, for example `docker-compose.yml`.

## Basics ##

Value names, which are referred to as keys, are always case-sensitive. If values contain more than letters and numbers,
they should be enclosed in single `'` or double quotes `"`. You can generally use all [Unicode](https://home.unicode.org/)
characters and [Emojis](https://home.unicode.org/emoji/about-emoji/).

The difference between single and double quotes is that double quotes support escape sequences like `\t` for a tab
or `\n` for a new line.

Related values start at the same indentation level. We recommend using 2 spaces, but any number of spaces will work 
as long as the indentation is consistent (tabs are not allowed).

Comments begin with the number sign `#`, can start anywhere on a line and continue until the end of the line.

```yaml
## EXAMPLE
Type: image
Title: "La Tour Eiffel ✨"
Year: 2014
Details:
  # Dictionaries are key/value pairs:
  Notes: "Hello\nWorld!" # contains a new line
  Keywords: 'paris, france'
```

## Simple Lists ##

List are lines that start at the same indentation level and begin with a `- ` (a dash and a space).
They are commonly used to define service dependencies, exposed network ports, or folders shared between 
host and container in `docker-compose.yml` files (volume mounts):

```yaml
services:
  photoprism:
    depends_on:
      - database
      - jobrunner
    ports:
      - "2342:2342"
    volumes:
      # Originals folder ("/host:/container")
      - "/mnt/photos:/photoprism/originals"
```

## Key-Value Pairs  ##

Dictionaries are collections of key/value pairs and often used to define environment variables in config files:

```yaml
services:
  mariadb:
    environment:
      MYSQL_ROOT_PASSWORD: "Y(&^UIk34"
      MYSQL_DATABASE: photoprism
      MYSQL_USER: photoprism
      MYSQL_PASSWORD: insecure
```