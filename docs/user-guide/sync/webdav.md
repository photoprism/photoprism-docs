# Connecting via WebDAV

WebDAV-compatible apps and clients such as [PhotoSync](mobile-devices.md), Microsoft's Windows Explorer,
and Apple's Finder can connect directly to PhotoPrism.

This mounts the *originals* and/or *import* folder as a network drive, allowing you to open, edit, and delete files from a remote device
as if they were local.

After files have been transferred, you can [index](../library/originals.md) or [import](../library/import.md) them as usual.
By default, indexing and importing start automatically after a safety delay when files have been uploaded using WebDAV.

It is also possible to [sync files with external WebDAV servers](../settings/sync.md) such as ownCloud or other PhotoPrism instances.

!!! tldr ""
    You can disable WebDAV by navigating to [Settings > Advanced](../settings/advanced.md) and selecting the corresponding option. As WebDAV access always requires authentication, the integrated server is automatically disabled if your instance is running in [public mode](../../getting-started/config-options.md#authentication).

!!! danger ""
    Do not use WebDAV [without HTTPS](../../getting-started/using-https.md) outside your local, private network as your password would be transmitted, in clear text, over the Internet. Backup tools and file sync apps like [FolderSync](https://foldersync.io/docs/faq/#https-connection-errors) may refuse to connect as well.

## Server URL

If your instance is connected to the public Internet, the WebDAV URL of the *originals* folder has the following format, where `example.com` must be replaced with the actual hostname and `admin` with the [actual username](#authentication):

```
https://admin@example.com/originals/
```

For users running a local instance on the default port 2342 *without HTTPS*, the URL of the *originals* folder is as follows (the default username for new instances is `admin`, unless you have [changed it](../../getting-started/config-options.md#authentication) in the configuration):

```
http://admin@localhost:2342/originals/
```

Please note that the slash at the end of the path must not be omitted and that the WebDAV URL in your client apps must be updated if the hostname or port of the server changes.

!!! note ""
    You can view the *originals* folder URL by navigating to [Settings > Account](../settings/account.md) and then clicking *Connect via WebDAV*. It is possible to connect to the *import* folder instead by replacing `originals/` with `import/` in the URL.

### Microsoft Windows

On Windows, you must instead [enter a resource string](#connect-to-a-webdav-server) in the following format to [configure WebDAV access](../../getting-started/troubleshooting/windows.md#connecting-via-webdav), where `example.com` must be replaced with the actual hostname of your instance:

```
\\example.com@SSL\originals\
```

If your server does not use the standard port 443 for [HTTPS](../../getting-started/using-https.md), Windows lets you specify a custom port such as 8443 directly after `@SSL`:

```
\\example.com@SSL@8443\originals\
```

For local installations running on the default port 2342 *without HTTPS*, you can enter the following resource in the connection dialog:

```
\\localhost:2342\originals\
```

Please note that the slash at the end must not be omitted and that the WebDAV resource in Windows needs to be updated when the hostname or port of the server changes.

!!! note ""
    You can view the *originals* folder resource by navigating to [Settings > Account](../settings/account.md) and then clicking *Connect via WebDAV*. It is possible to connect to the *import* folder instead by replacing `originals/` with `import/` in the URL.

## Credentials

To access your instance via WebDAV, you can use your username in combination with your account password or [an app password](../settings/account.md#apps-and-devices), e.g. if you have [2-Factor Authentication (2FA)](../users/2fa.md) enabled for your account or authenticate via [OpenID Connect (OIDC)](../../getting-started/advanced/openid-connect.md) as using your account password is not possible in this case.

If access is not possible even though the login credentials are correct, please check whether the account has a [role with WebDAV access](../users/roles.md) and whether [WebDAV is enabled](../users/cli.md#command-options) for the specific account.

[Learn more ›](../users/index.md)

## Connect to a WebDAV Server

=== "macOS"

     1. In the **Finder** on your Mac, choose Go > Connect to Server
     2. Enter the URL as shown above in the **Server Address** field
     3. Click **Connect**

    If you cannot connect to your instance via WebDAV using these instructions:

    - [ ] You do not have sufficient user rights (try as admin)
    - [ ] You are experiencing a [general authentication problem](../../getting-started/troubleshooting/index.md#cannot-log-in)
    - [ ] Your instance or reverse proxy uses an invalid [HTTPS](../../getting-started/using-https.md) certificate
    - [ ] You are trying to connect to the wrong network or server

=== "Windows"

     1. Open Windows **File Explorer**
     2. Right click **This PC**
     3. From the dropdown, select **Map network drive...**

        ![Screenshot](img/webdav-1.jpg){ class="shadow" }

     4. Enter the drive letter and folder you want to map your WebDAV connection to
     5. Check the boxes **Reconnect at sign-in** and **Connect using different credentials**
     6. Click the **Connect to a Web site that you can use to store your documents and pictures** link
     
        ![Screenshot](img/webdav-2.jpg){ class="shadow" }
     
     7. Click **Next**
     
        ![Screenshot](img/webdav-3.jpg){ class="shadow" }
     
     8. Click **Choose a custom network location** and then click **Next**
     
        ![Screenshot](img/webdav-4.jpg){ class="shadow" }     
     
     9. In the **Internet or network address** field, enter the URL as shown above and click **Next**
        
        ![Screenshot](img/webdav-5.jpg){ class="shadow" }
     
     10. Enter your username and password and click **Ok**
     
        ![Screenshot](img/webdav-6.jpg){ class="shadow" }
     
     11. Enter a name for the network location and click **Next**
    
        ![Screenshot](img/webdav-7.jpg){ class="shadow" }
    
     12. Click **Finish**
    
        ![Screenshot](img/webdav-8.jpg){ class="shadow" }
    
     The originals folder appears as a mapped drive in Windows Explorer, and you can immediately add,
     edit, or delete files and directories using the Windows File Explorer.
    
     ![Screenshot](img/webdav-9.jpg){ class="shadow" }

    If you [cannot connect to your instance via WebDAV](../../getting-started/troubleshooting/windows.md#connecting-via-webdav) using these instructions:

    - [ ] You may need to **[change the basic authentication level](../../getting-started/troubleshooting/windows.md#connecting-via-webdav)** in the registry
    - [ ] You do not have sufficient user rights (try as admin)
    - [ ] You are experiencing a [general authentication problem](../../getting-started/troubleshooting/index.md#cannot-log-in)
    - [ ] Your instance or reverse proxy uses an invalid [HTTPS](../../getting-started/using-https.md) certificate
    - [ ] You are trying to connect to the wrong network or server
