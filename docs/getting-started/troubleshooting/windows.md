# Solving Windows-Specific Issues

## NTFS File System

If you experience poor performance when indexing large libraries stored on NTFS:

- [ ] The I/O bandwidth used to update the *Last Access Time* can be a significant percentage of the total I/O bandwidth on NTFS volumes with a large number of files or folders (disable updates).[^1]
- [ ] In folders with many files, file names may start to conflict after NTFS uses all of the 8.3 short file names that are similar to the long names. Repeated conflicts between new and existing short names cause NTFS to regenerate the short file name from 6 to 8 times (disable short file names and reduce the number of files per folder).[^2] [^3]
- [ ] [exFat](https://en.wikipedia.org/wiki/ExFAT) can be faster than NTFS, especially on external SSD drives with a lot of small files.
- [ ] Windows 10 allows physical disks formatted with the Linux ext4 file system to be mounted directly in WSL 2, which may be an option for some use cases.[^4]

[^1]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#last-access-time>
[^2]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#how-ntfs-generates-short-file-names>
[^3]: <https://stackoverflow.com/a/9600126>
[^4]: <https://www.bleepingcomputer.com/news/microsoft/windows-10-now-lets-you-mount-linux-ext4-filesystems-in-wsl-2/>

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-pencil: to send a pull request with your changes.
