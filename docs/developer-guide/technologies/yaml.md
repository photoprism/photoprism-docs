# Introduction to YAML

YAML is an indentation-based markup language designed to be easy to read and write even for non-developers.
PhotoPrism uses it for metadata backups and config files because of its simplicity and widespread support 
in other applications and tools like [Docker Compose](https://dl.photoprism.app/docker/docker-compose.yml).

## Keys and Values ##

Value names, which are referred to as keys, are always case-sensitive. If values contain more than letters and numbers,
they should be enclosed in single `'` or double quotes `"`. You can generally use all [Unicode](https://home.unicode.org/)
characters and [Emojis](https://home.unicode.org/emoji/about-emoji/).

The difference between single quotes and double quotes is that double quotes support escape sequences 
like `\t` for a tab or `\n` for a new line.

Related values start at the same indentation level. We recommend using 2 spaces, but e.g. 4 spaces are also
possible as long as the indentation is consistent in a file:

```yaml
Type: image
Title: "La Tour Eiffel ✨"
Year: 2014
Details:
  Notes: "Hello\nWorld!"
  Keywords: 'paris, france'
```

## Simple Lists ##

List are lines that start at the same indentation level and begin with a `- ` (a dash and a space):

```yaml
services:
  photoprism:
    depends_on:
      - database
      - jobrunner
    ports:
      - "2342:2342"
```

## Dictionaries ##

Dictionaries are collections of key/value pairs and are typically used to set environment variables:

```yaml
services:
  mariadb:
    environment:
      MYSQL_ROOT_PASSWORD: "Y(&^UIk34"
      MYSQL_DATABASE: photoprism
      MYSQL_USER: photoprism
      MYSQL_PASSWORD: insecure
```