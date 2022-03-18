# Restoring from backup

In order to fully restore your PhotoPrism instance you need the following:

* All content from your `originals` folder
* An index database SQL dump

(A backup based on [our documentation](../../getting-started/advanced/backups.md) will be enough)

After verifying that you have all you need, continue with the following restore-procedure:

1. Restore the contents in your `originals` folder
2. `photoprism restore -i [filename-to-your-sql-dump]`
3. [Re-index (Complete rescan)](../../user-guide/library/originals.md) your library, in order to re-generate thumbnails.


Helpful information can be found on [GitHub](https://github.com/photoprism/photoprism/discussions/772) as well.