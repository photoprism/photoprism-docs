# Duplicate Detection #

Duplicates are detected and automatically skipped, so they only appear once in search results and albums. Viewing and deleting duplicate files via Web UI will be possible in a [future release](https://github.com/photoprism/photoprism/issues/1308).

↪ [Indexing Originals](originals.md)

When [importing](import.md), files are first copied or moved from a temporary folder to the *originals* folder. In the process, duplicates are automatically skipped. "Move" also deletes them in the source directory as if they were successfully moved.

↪ [Import to Originals](import.md)

## Related Files

In addition to exact duplicates, there may be similar pictures and related sidecar files (with the same filename) in your library, for example:

- raw + jpg + xmp
- jpg + json
- original + edited version
- original + compressed version
- live and timelapse photos

Depending on your library settings, such files may be automatically grouped into stacks:

↪ [File Stacks](../organize/stacks.md)

↪ [Library Settings](../settings/library.md)
