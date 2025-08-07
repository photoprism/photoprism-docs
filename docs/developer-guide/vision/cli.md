# Computer Vision Commands

## Save Model Configuration 

To write the model configuration to a `vision.yml` file you can run:

```bash
docker compose exec photoprism photoprism vision save
```

You can then configure the `vision.yml` file according to your specific needs.

## View Model Configuration

You can use the following terminal command, to inspect your current model configuration:

```bash
docker compose exec photoprism photoprism vision ls
```
### Command Options

You can combine it with these flags to change the output format:

| Command Flag | Description                            |
|--------------|----------------------------------------|
| `--md, -m`   | format as machine-readable Markdown    |
| `--csv, -c`  | export as semicolon separated values   |
| `--tsv, -t`  | export as tab separated values         |

## Run Vision Models

Once you have configured your preferred computer vision models and services in the `vision.yml` file, you can use the following command to run a model on a set of pictures, as specified by the search filter:

```bash
photoprism vision run [options] [filter]
```

### Command Options

| Command Flag                  | Description                                                                                                          |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------|
| `--models MODELS`, `-m MODELS`| computer vision MODELS to run, e.g. caption, labels, or nsfw (default: "caption")                                    |
| `--count value`, `-c value`   | maximum number of pictures to be processed (default: 100000)                                                         | 
| `--source TYPE`, `-s TYPE`    | custom data source TYPE, e.g. estimate, image, meta, or manual (default: "image")                                    |
| `--force`, `-f`               | force existing data to be updated if the source priority is equal to or higher than the current one (default: false) |

To generate captions for all photos in your library, you can run:

```bash
docker compose exec photoprism photoprism vision run --models=caption
```

Note: Processing time will vary based on your library size and hardware performance and may take a considerable amount of time for large collections.

If you have a model for labels configured in your `vision.yml` you can run the following to generate labels:

```bash
docker compose exec photoprism photoprism vision run --models=labels
```

To generate captions only for photos matching a specific search filter such as those in a particular album, use the following command:
```bash
docker compose exec photoprism photoprism vision run --models=caption album:Holidays
```

To re-generate captions for photos that already have some, add the --force flag to your command:

```bash
docker compose exec photoprism photoprism vision run --models=caption --force
```

This is especially useful when testing different models or prompts. Note that the configured source must have a equal or higher priority than the source of the existing captions for them to be replaced.


