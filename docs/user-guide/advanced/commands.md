Photoprism provides commands to keep your instance clean or to update backups.
Some commands are executed in the background. Others can only be triggered manually.

## Cleanup
### What does it?

### When is it executed?

## Optimize
### What does it?
The optimize command checks all files with checked = false for metadata optimizations. 
Those include:

* Estimate locations 
* Use mod date as date if no other date is provided
* .....
* Set checked = true for all the files it checked

### When is it executed?
By default optimize is running every 15 minutes. 
This interval can be configured using: `PHOTOPRISM_WAKEUP_INTERVAL`.

After 7 days the files with checked = true will be reset to checked = false.

## Purge
### What does it?

### When is it executed?


## Reset db

## Restore

## How to migrate between different dbs


