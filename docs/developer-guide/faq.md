# Frequently Asked Questions

### Isn't it insecure that thumbnail URLs work even if you are not logged in? ###

Like most commercial image hosting services, we've chosen to use a **cookie-free thumbnail API** to minimize request latency and avoid unnecessary network traffic. If you were to copy private session cookies and use them in a different browser window, you would have a similar problem, except that they also work for other API endpoints, not just a single image.

Even if URLs were to become invalid every minute: Digital copies are as good as originals. Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back. Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

Visit [docs.photoprism.app/developer-guide/media/thumbnails/](https://docs.photoprism.app/developer-guide/media/thumbnails/) to learn more.

### Does your software depend on any external services?

As explained in detail in our [Privacy Policy](https://photoprism.app/privacy), reverse geocoding and interactive world maps depend on retrieving the necessary information from [us](https://photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.

Your use of these services is fully covered by us at the moment. Depending on your usage, this can save you thousands of dollars every month. Other providers typically charge usage-based fees and may also not allow you to cache the data they provide, compromising your privacy with unnecessary requests.

Should you still wish to operate one or both of these services on your own premises, [we can set up such a fully autonomous solution](https://photoprism.app/contact) for you, provided you are prepared to cover the [initial setup costs](https://photoprism.app/kb/compliance-faq#fully-autonomous-solution) as well as ongoing maintenance fees for content licenses and updates.

[View Privacy Policy ›](https://photoprism.app/privacy#section-7){ class="pr-3" } [View Compliance FAQ ›](https://photoprism.app/kb/compliance-faq#privacy)

### Why do I see connection errors when requesting API keys at startup?

As explained above, reverse geocoding and interactive world maps depend on retrieving the necessary information from external services. Please make sure that you allow requests to these API endpoints if you have a firewall installed, and verify that your Internet connection is working.

### Are the keys for using interactive world maps provided free of charge?

The API keys required to use the maps are unfortunately not free for us due to the number of users we have. Those costs are one of the reasons why we encourage all users to support our mission by [signing up as a sponsor](https://photoprism.app/membership) or purchasing a [commercial license](https://photoprism.app/teams).

While we could register several "non-commercial test accounts" instead, we don't think that would be fair and [Maptiler](https://www.maptiler.com/) might then stop offering them to those in need.