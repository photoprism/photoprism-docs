# Diagnosing Frontend Issues

Problems with the user interface can be caused by a bug or an incompatible browser:

- some features [may not be supported](https://caniuse.com/) by non-standard browsers, as well as nightly, unofficial, or outdated versions
- not all [video and audio formats](https://caniuse.com/?search=video%20format) can be played with every browser, device, and operating system
- for example, [AAC](https://caniuse.com/aac "Advanced Audio Coding") - the default audio codec for [MPEG-4 AVC / H.264](https://caniuse.com/avc "Advanced Video Coding") - is supported natively in Chrome, Safari, and Edge, while it is only optionally supported by the OS in Firefox and Opera

!!! note ""
    If the user interface doesn't load at all, our [*App Not Loading*](index.md#app-not-loading) checklist helps you identify and resolve the cause.

## Try Another Browser ##

To test if you have a general problem that is not browser-specific, [open the Web UI](../docker-compose.md#step-2-start-the-server) in other browsers:

- if you are using [Firefox Nightly](https://www.mozilla.org/en-US/firefox/channel/desktop/), try the [stable version](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release) and [Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/getting-involved/download-chromium)
- if you have browser plugins installed, try disabling them to see if this makes a difference
- when the problem disappears, you know that the issue is browser-dependent or caused by a plugin
- otherwise, the issue may not be specific to the browser version
- make a note in which browsers the problem occurs, as this will be helpful when submitting a support request

!!! tldr ""
    The user interface works with most modern browsers, and runs best on [Chrome](https://www.google.com/chrome/), [Chromium](https://www.chromium.org/getting-involved/download-chromium), [Safari](https://www.apple.com/safari/), [Firefox](https://www.mozilla.org/en-US/firefox/all/#product-desktop-release), and [Edge](https://www.microsoft.com/en-us/edge).
    Opera and Samsung Internet have been reported to be compatible as well. Due to [limited resources](https://photoprism.app/membership), we can
    not test every release with all browser types and versions.

## Getting Error Details ##

If possible, please also include the error type, error message, and URL of the affected resource when
[submitting a support request](../../user-guide/index.md#getting-support). For this purpose, check the
browser console for warnings and errors as described below. It is perfectly fine to take screenshots
instead of writing down the details.

*In case you don't see any log messages, try reloading the page, as the problem may occur while the page is loading.*

=== "Chrome, Chromium, and Edge"
   
    - press ⌘+Option+J (Mac) or Ctrl+Shift+J (Windows, Linux, Chrome OS) to go directly to the Developer Tools
    - or, navigate to *More tools* > *Developer tools* in the browser menu and open the *Console* tab

=== "Firefox"

    - press ⌘+Option+K (Mac) or Ctrl+Shift+K (Windows) to go directly to the Firefox Web Console panel
    - or, navigate to *Web Development* > *Web Console* in the menu and open the *Console* panel

=== "Safari"

    Before you can access the console in Safari, you first need to enable the *Develop* menu:

    1. Choose Safari *Menu* > *Preferences* and select the *Advanced Tab*
    2. Select "Show Develop menu in menu bar"

    Once the *Develop* menu is enabled:

    - press Option+⌘+C to go directly to the *Javascript Console*
    - or, navigate to *Develop* > *Show Javascript Console* in the browser menu

!!! info ""
    **We kindly ask you not to report bugs via *GitHub Issues* unless you are certain to have found a fully reproducible and previously unreported issue that must be fixed directly in the app.**
    [Ask for technical support](../../user-guide/index.md#getting-support) if you need help, it could be a local
    configuration problem, or a misunderstanding in how the software works.

*[URL]: Web Address