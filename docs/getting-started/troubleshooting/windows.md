# Solving Windows-Specific Issues

## NTFS File System

If you experience poor performance when indexing large libraries stored on NTFS:

- [ ] The I/O bandwidth used to update the *Last Access Time* can be a significant percentage of the total I/O bandwidth on NTFS volumes with a large number of files or folders (disable updates).[^1]
- [ ] In folders with many files, file names may start to conflict after NTFS uses all of the 8.3 short file names that are similar to the long names. Repeated conflicts between new and existing short names cause NTFS to regenerate the short file name from 6 to 8 times (disable short file names and reduce the number of files per folder).[^2] [^3]
- [ ] [exFat](https://en.wikipedia.org/wiki/ExFAT) can be faster than NTFS, especially on external SSD drives with a lot of small files.
- [ ] Windows 10 and 11 allow physical disks formatted with the Linux ext4 file system to be mounted directly in WSL 2, which may be an option for some use cases.[^4]

## Mounting Volumes

When using the latest versions of [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install), you should be able to [mount folders from all drives](../docker-compose.md#volumes), including network shares, under `volumes` in your [`compose.yaml`](https://dl.photoprism.app/docker/windows/compose.yaml) file.

You should also be able to [mount additional directories](../advanced/docker-volumes.md#originals-folder) as subfolders of `/photoprism/originals`, as shown in the following example:

```yaml
services:
  photoprism:
    volumes:
      - "C:/Pictures:/photoprism/originals"
      - "D:/Shared/Family:/photoprism/originals/Family"
```

If drives other than `C:` cannot be used, or folders are created and mounted from `C:` instead:

- [ ] Make sure e.g. `D:/Shared/Family` already exists on `D:` *before* starting the container. If not, create it in [File Explorer](https://support.microsoft.com/en-us/windows/file-explorer-in-windows-ef370130-1cca-9dc5-e0df-2f7416fe1cb1), bearing in mind that directory names may be case-sensitive.
- [ ] Configure [Docker Desktop](https://www.docker.com/products/docker-desktop/) to use [**WSL2 Linux**](https://docs.docker.com/desktop/settings-and-maintenance/settings/#wsl-integration) containers, and ensure the **latest versions** of [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and [Docker Desktop](https://www.docker.com/products/docker-desktop/) are installed: https://docs.docker.com/desktop/features/wsl/
- [ ] Grant access to the folders in [Docker Desktop](https://www.docker.com/products/docker-desktop/) under [Settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/) > [Resources](https://docs.docker.com/desktop/settings-and-maintenance/settings/#resources) > [File Sharing](https://docs.docker.com/desktop/settings-and-maintenance/settings/#file-sharing). Note that these settings [may not be available when using WSL2](https://docs.docker.com/desktop/settings-and-maintenance/settings/#file-sharing). If you can see them, it could mean that you are using [Hyper-V instead of WSL2](https://docs.docker.com/desktop/setup/install/windows-install/#system-requirements).
- [ ] Manually test the `D:` mount using the `docker` command, for example in [PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows) as the user who runs [Docker Desktop](https://www.docker.com/products/docker-desktop/):
      ```powershell
      docker run --rm -it -v "D:/Shared/Family:/data" alpine ls -al /data
      ```

[Learn more ›](https://docs.docker.com/desktop/settings-and-maintenance/settings/#resources)

## Connecting via WebDAV

If you [followed our step-by-step guide](../../user-guide/sync/webdav.md#__tabbed_1_2) and still have trouble connecting via WebDAV:

- [ ] You need to change the basic authentication level (see below).
- [ ] You do not have sufficient user rights (try as admin).
- [ ] You are experiencing a [general authentication problem](index.md#cannot-log-in).
- [ ] Your instance or reverse proxy uses an invalid HTTPS certificate.
- [ ] You are trying to connect to the wrong network or server.

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
4. Set the value to `4294967295` (in Decimal).
5. Restart your computer.

!!! example ""
    **Help improve these docs!** You can contribute by clicking :material-file-edit-outline: to send a pull request with your changes.

[^1]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#last-access-time>
[^2]: <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc781134(v=ws.10)?redirectedfrom=MSDN#how-ntfs-generates-short-file-names>
[^3]: <https://stackoverflow.com/a/9600126>
[^4]: <https://www.bleepingcomputer.com/news/microsoft/windows-10-now-lets-you-mount-linux-ext4-filesystems-in-wsl-2/>
[^5]: <https://help.druva.com/en/articles/8513266-troubleshoot-legal-hold-issues-when-using-network-mapped-drives>
