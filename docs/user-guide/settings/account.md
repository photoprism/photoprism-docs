# Account Settings #

!!! tldr ""
    For security reasons, changing account-related settings through the user interface requires password authentication, so these settings will not be available to you when [public mode](../../getting-started/config-options.md#authentication) is enabled.

![Screenshot](img/settings-account-light.jpg){ class="shadow" }

## Change Password ##

1. Go to *Settings*
2. Open *Account* tab
3. Click *Change Password*
4. Enter your current password
5. Enter your new password twice
6. Click *Change*

![Screenshot](img/change-password-light.jpg){ class="shadow" }

## 2-Factor Authentication

Two-factor authentication (2FA) can add an extra layer of security to your account in case someone gains access to your password. If enabled, you will need a randomly generated verification code in addition to your password to log in.

[Learn more ›](../users/2fa.md)

## Apps and Devices

If 2FA is enabled for your account, other apps and services will no longer be able to use your password as they do not have access to the verification codes.

You can therefore generate app-specific passwords for them by navigating to *Settings > Account* and then clicking the *Apps and Devices* button. We also recommend using app-specific passwords in case 2FA is not enabled for your account.

Example for generating an app password that you can use with [WebDAV-compatible](../sync/webdav.md) file synchronization apps like [PhotoSync](../sync/mobile-devices.md):

![Screenshot](../users/img/app-password.jpg){ class="shadow" }

!!! tldr ""
    By selecting the *WebDAV* scope, you ensure that the app password cannot be used to log in through the regular user interface or for other actions. Apps will also not be able to change your password or manage user accounts, even if you grant them *Full Access*.

## Connect via WebDAV ##

To open a dialog that shows you the URLs required to connect an app or computer via WebDAV:

1. Go to *Settings*
2. Open *Account* tab
3. Click *Connect via WebDAV*

![Screenshot](img/show-webdav-light.jpg){ class="shadow" }