# Creating Backups

A full backup of your PhotoPrism instance includes:

1. All photo, video, and sidecar files in your `originals` folder
2. An index database SQL dump

The best way to create an index backup is to run this command in a terminal:

```
photoprism backup -a -i [filename]
 ```

Use `-` as filename to write the backup to stdout. If you leave it empty, the backup
will be written to the default backup folder configured via `PHOTOPRISM_BACKUP_PATH`.

Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.