# Diagnosing Frontend Issues

!!! info ""
    You are welcome to ask for help in our [community chat](https://gitter.im/browseyourlife/community).
    [Sponsors](../../funding.md) receive direct [technical support](https://photoprism.app/contact) via email.
    Before reporting a bug, try to determine the cause of your problem.

!!! note ""
    We recommend going through the related [troubleshooting checklist](index.md#app-not-loading) if you only see the
    logo and nothing else happens, even if you wait a moment.

### Try Another Browser ###

If you have a frontend problem, it may be due to a bug or because your browser is incompatible.
In particular, nightly, unstable, and patent-free browser builds may not support certain
features, standards, and [video formats](https://github.com/photoprism/photoprism/issues/707).

To test if you have a general problem that is not browser-specific, open the Web UI in other browsers:

- If you are using [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/), try the [stable version](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release) and [Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/getting-involved/download-chromium)
- If you have browser plugins installed, try disabling them to see if this makes a difference
- When the problem disappears, you know that the issue is browser-dependent or caused by a plugin
- Otherwise, the issue may not be specific to the browser version
- Make a note in which browsers the problem occurs, as this will be helpful when submitting a support request

!!! tldr ""
    The user interface works with most modern browsers, and runs best on Chrome, Chromium, Safari, Firefox, and Edge.
    Opera and Samsung Internet have been reported to be compatible as well. Due to limited resources, we can
    not test every release with all browser types and versions.

### Getting Error Details ###

If possible, please also include the error type, error message, and URL of the affected resource when submitting a
support request. You may find this information in the **browser console**. It is perfectly fine to take screenshots
instead of writing the details down.

#### Chrome, Chromium, and Edge ####

- Press Command+Option+J (Mac) or Ctrl+Shift+J (Windows, Linux, Chrome OS) to go directly to the Developer Tools
- Or, navigate to *More tools* > *Developer tools* in the browser menu and open the *Console* tab

#### Firefox ####

- Press Command+Option+K (Mac) or Ctrl+Shift+K (Windows) to go directly to the Firefox Web Console panel
- Or, navigate to *Web Development* > *Web Console* in the menu and open the *Console* panel

!!! note ""
    If you don't see any errors, try reloading the page, as the error may occur while the page is loading.

*[UI]: User Interface
*[URL]: Web Address