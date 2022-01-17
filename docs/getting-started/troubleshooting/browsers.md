# Diagnosing Frontend Issues

!!! info ""
    You are welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to determine the cause of your problem.

Problems with the user interface can be caused by a bug or an incompatible browser:

- Some [features are not supported](https://caniuse.com/) by non-standard browsers, as well as nightly, test, and unofficial versions
- In particular, not [all video formats](https://caniuse.com/?search=video%20format) can be [played with every browser](https://github.com/photoprism/photoprism/issues/707)

!!! tldr ""
    We recommend going through our related [troubleshooting checklist](index.md#app-not-loading) in case the app doesn't load at all.

#### Try Another Browser ####

To test if you have a general problem that is not browser-specific, [open the Web UI](../docker-compose.md#step-2-start-the-server) in other browsers:

- If you are using [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/), try the [stable version](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release) and [Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/getting-involved/download-chromium)
- If you have browser plugins installed, try disabling them to see if this makes a difference
- When the problem disappears, you know that the issue is browser-dependent or caused by a plugin
- Otherwise, the issue may not be specific to the browser version
- Make a note in which browsers the problem occurs, as this will be helpful when submitting a support request

!!! tldr ""
    The user interface works with most modern browsers, and runs best on [Chrome](https://www.google.com/chrome/), [Chromium](https://www.chromium.org/getting-involved/download-chromium), [Safari](https://www.apple.com/safari/), [Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release), and [Edge](https://www.microsoft.com/en-us/edge).
    Opera and Samsung Internet have been reported to be compatible as well. Due to [limited resources](../../funding.md), we can
    not test every release with all browser types and versions.

#### Getting Error Details ####

If possible, please also include the error type, error message, and URL of the affected resource when
[submitting a support request](../../user-guide/index.md#getting-support). For this purpose, check the
browser console for warnings and errors as described below. It is perfectly fine to take screenshots
instead of writing down the details.

=== "Chrome, Chromium, and Edge"
   
    - Press ⌘+Option+J (Mac) or Ctrl+Shift+J (Windows, Linux, Chrome OS) to go directly to the Developer Tools
    - Or, navigate to *More tools* > *Developer tools* in the browser menu and open the *Console* tab

=== "Firefox"

    - Press ⌘+Option+K (Mac) or Ctrl+Shift+K (Windows) to go directly to the Firefox Web Console panel
    - Or, navigate to *Web Development* > *Web Console* in the menu and open the *Console* panel

=== "Safari"

    Before you can access the console in Safari, you first need to enable the *Develop* menu:

    1. Choose Safari *Menu* > *Preferences* and select the *Advanced Tab*
    2. Select "Show Develop menu in menu bar"

    Once the *Develop* menu is enabled:

    - Press Option+⌘+C to go directly to the *Javascript Console*
    - Or, navigate to *Develop* > *Show Javascript Console* in the browser menu

!!! tldr ""
    In case you don't see any log messages, try reloading the page, as the problem may occur while the page is loading.

*[UI]: User Interface
*[URL]: Web Address