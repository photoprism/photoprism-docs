# Camera & Lens Commands

The `photoprism cameras` and `photoprism lenses` commands list, add, rename, and delete the camera and lens records that pictures can be assigned to. Both commands offer the same subcommands and flags, so the examples below use `cameras` and apply to `lenses` as well.

Cameras and lenses are normally created from the Exif data found while indexing. Adding one manually is useful for pictures without such metadata, e.g. scans of film photos or pictures taken with an adapted manual lens. Once added, it can be selected in the edit dialog after reloading the page. Cameras added this way are kept even if no picture references them yet.

Like all commands that change data, they follow the [CLI Conventions](../cli-conventions.md) for confirmation prompts and exit codes.

## List Cameras & Lenses

```bash
photoprism cameras ls [options] [query]
```

Lists discovered and added cameras with their ID, slug, name, make, model, and last update. The optional query limits the results to matching records.

| Command Flag  | Description                              |
|---------------|------------------------------------------|
| `--count, -n` | maximum number of results (default: 100) |
| `--offset`    | number of results to skip                |
| `--nomake`    | return only records without a make       |
| `--json, -j`  | print machine-readable JSON              |
| `--md, -m`    | print machine-readable Markdown          |
| `--csv, -c`   | print semicolon separated values         |
| `--tsv, -t`   | print tab separated values               |

## Add a Camera or Lens

```bash
photoprism cameras add --make=Leica --model="M6"
photoprism lenses add --make=Helios --model="44-2 58mm f/2"
```

Both `--make` and `--model` are required. If a record with the same make and model already exists, the command reports it and exits with code `0` without creating a duplicate. The added or existing record is printed afterwards, and the report flags listed above can be used to change the output format.

## Rename a Camera or Lens

```bash
photoprism cameras update --id=5 --make=Leica --model="M6 TTL"
```

Changes the make and model of the record with the specified ID. All three flags are required. The ID is shown by `photoprism cameras ls`. The unknown placeholder record cannot be changed.

## Delete a Camera or Lens

```bash
photoprism cameras rm --id=5
photoprism cameras rm --make=Leica --model="M6" --reassign --yes
```

Selects the record either by `--id` or by `--make` and `--model`. If several records have the same make and model, the command lists their IDs and asks you to pass `--id` instead.

| Command Flag | Description                                                      |
|--------------|------------------------------------------------------------------|
| `--id`       | ID of the camera or lens                                         |
| `--make`     | make of the camera or lens, combined with `--model`              |
| `--model`    | model of the camera or lens, combined with `--make`              |
| `--reassign` | assigns pictures that use it to the unknown camera or lens first |
| `--yes, -y`  | skips the confirmation prompt, e.g. when running in a script     |

A camera or lens that is still used by pictures is only deleted with `--reassign`, which assigns those pictures to the unknown camera or lens first. The unknown placeholder record cannot be deleted.

## Exit Codes

| Code | Meaning                                                                                                                                                         |
|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `0`  | Success, a declined confirmation, or a camera or lens that already exists                                                                                       |
| `1`  | Runtime failure, e.g. a database error                                                                                                                          |
| `2`  | Usage error, e.g. an empty make or model, conflicting flags, a record still in use without `--reassign`, or a confirmation that cannot be shown without `--yes` |
| `3`  | The camera or lens was not found                                                                                                                                |
