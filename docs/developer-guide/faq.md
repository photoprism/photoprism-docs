# Frequently Asked Questions

### Isn't it insecure that thumbnail URLs work even if you are not logged in? ###

Like most commercial image hosting services, we've chosen to use a **cookie-free thumbnail API** to minimize request latency and avoid unnecessary network traffic. If you were to copy private session cookies and use them in a different browser window, you would have a similar problem, except that they also work for other API endpoints, not just a single image.

Even if URLs were to become invalid every minute: Digital copies are as good as originals. Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back. Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

Visit [docs.photoprism.app/developer-guide/media/thumbnails/](https://docs.photoprism.app/developer-guide/media/thumbnails/) to learn more.
