# Solving Windows-Specific Issues

## NTFS File System

If you experience poor performance when indexing large libraries stored on NTFS:

- [ ] The I/O bandwidth used to update the *Last Access Time* can be a significant percentage of the total I/O bandwidth on NTFS volumes with a large number of files or folders (disable updates).[^1]
- [ ] In folders with many files, file names may start to conflict after NTFS uses all of the 8.3 short file names that are similar to the long names. Repeated conflicts between new and existing short names cause NTFS to regenerate the short file name from 6 to 8 times (disable short file names and reduce the number of files per folder).[^2] [^3]
- [ ] [exFat](https://en.wikipedia.org/wiki/ExFAT) can be faster than NTFS, especially on external SSD drives with a lot of small files.
- [ ] Windows 10 and 11 allow physical disks formatted with the Linux ext4 file system to be mounted directly in WSL 2, which may be an option for some use cases.[^4]

## Connecting via WebDAV

If you [followed our step-by-step guide](../../user-guide/sync/webdav.md#__tabbed_1_2) and still have trouble connecting via WebDAV:

- [ ] You need to change the basic authentication level (see below)
- [ ] You do not have sufficient user rights (try as admin)
- [ ] You are experiencing a [general authentication problem](index.md#cannot-log-in)
- [ ] Your instance or reverse proxy uses an invalid HTTPS certificate
- [ ] You are trying to connect to the wrong network or server

To **change the basic authentication level** in the Windows registry:

1. Open the [Windows Registry Editor](https://support.microsoft.com/en-us/windows/how-to-open-registry-editor-in-windows-10-deab38e6-91d6-e0aa-4b7c-8878d9e07b11).
2. Locate the following registry directory: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters`
3. Locate the value `BasicAuthLevel`.
4. The value data box should be set to 2. If the value is not 2, right click it and then select *Modify*.
5. Change the value to 2.

## WebDAV File Size Limit

When uploading or downloading large files (more than 50 MB) on Windows, this error may occur:

```
Error 0x800700DF: The file size exceeds the limit allowed and cannot be saved
```

To allow larger files, you must increase the size limit in the Windows registry:[^5]

1. Open the [Windows Registry Editor](https://support.microsoft.com/en-us/windows/how-to-open-registry-editor-in-windows-10-deab38e6-91d6-e0aa-4b7c-8878d9e07b11).
2. Locate the following registry directory: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WebClient\Parameters`
3. Locate the value `FileSizeLimitInBytes`.
4. Set the value to 4294967295 (in Decimal). 
5. Restart your computer.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.

[^1]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#last-access-time>
[^2]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#how-ntfs-generates-short-file-names>
[^3]: <https://stackoverflow.com/a/9600126>
[^4]: <https://www.bleepingcomputer.com/news/microsoft/windows-10-now-lets-you-mount-linux-ext4-filesystems-in-wsl-2/>
[^5]: <https://docs.druva.com/Knowledge_Base/inSync/Troubleshooting/WebDAV_download_fails_with_file_size_exceeds__the_limit_error>
