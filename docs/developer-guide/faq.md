# Frequently Asked Questions

### Why not use a more permissive public license so that, for example, developers at Google can contribute more easily? ###

Since we had hoped for a collaboration with Google and were aware of [their AGPL policy](https://opensource.google/documentation/reference/using/agpl-policy), PhotoPrism was initially licensed under Apache 2.0, which is much more permissive. However, no one seemed interested, although we did talk to quite a few personal acquaintances at Google. That made it easy for our community to convince us to use AGPL instead.

### Isn't it insecure that thumbnail URLs work even if you are not logged in? ###

Like most commercial image hosting services, we've chosen to use a **cookie-free thumbnail API** to minimize request latency and avoid unnecessary network traffic. If you were to copy private session cookies and use them in a different browser window, you would have a similar problem, except that they also work for other API endpoints, not just a single image.

Even if URLs were to become invalid every minute: Digital copies are as good as originals. Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back. Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

Visit [docs.photoprism.app/developer-guide/media/thumbnails/](https://docs.photoprism.app/developer-guide/media/thumbnails/) to learn more.

### Does your software depend on any external services?

As explained in our [Privacy Policy](https://www.photoprism.app/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](https://www.photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.

Your use of these services is [fully covered by us](../getting-started/faq.md#are-the-keys-for-using-interactive-world-maps-provided-free-of-charge). Depending on your usage, this can save you much more than the cost of a [PhotoPrism+ Membership](https://www.photoprism.app/membership), since other providers generally charge usage-based fees and often don't allow you to cache the data they provide, compromising performance and your privacy with unnecessary requests.

You might also come across other apps that use the free map tile service [offered by openstreetmap.org](https://operations.osmfoundation.org/policies/tiles/). In this case, [their usage](https://operations.osmfoundation.org/policies/tiles/) and [privacy policies](https://wiki.osmfoundation.org/wiki/Privacy_Policy) apply, meaning that your request data is stored and used to create [publicly available reports](https://planet.openstreetmap.org/tile_logs/). This is a major difference from our approach, which [focuses on your privacy](https://www.photoprism.app/privacy) and user experience.

In order to use the maps and view location details in PhotoPrism, as well as successfully run our test suite as a developer, you must **allow requests to these API endpoints** if you have a firewall installed and make sure your Internet connection is working.

Should you wish to operate one or both of these services on your own premises, we can set up such a [fully autonomous solution](https://www.photoprism.app/kb/compliance-faq#fully-autonomous-solution) for you, provided you are prepared to cover the initial setup costs as well as ongoing maintenance fees for content licenses and updates.

[View Privacy Policy ›](https://www.photoprism.app/privacy#section-7){ class="pr-3 block-xs" } [View Compliance FAQ ›](https://www.photoprism.app/kb/compliance-faq#privacy)

### Why do I see connection errors when requesting API keys at startup?

As explained above, reverse geocoding and interactive world maps depend on retrieving the necessary information from external services. Please make sure that you allow requests to these API endpoints if you have a firewall installed, and verify that your Internet connection is working.

### Are the keys for using interactive world maps provided free of charge?

The API keys required to use the maps are unfortunately not free for us due to the number of users we have. Those costs are one of the reasons why we encourage all users to support our mission by [signing up as a member](https://www.photoprism.app/membership) or purchasing a [commercial license](https://www.photoprism.app/teams#compare).

To improve the situation for those who don't want to or cannot [sign up](https://www.photoprism.app/editions#compare), more details such as cities and lakes have been added to the freely available basic maps:

- [Places: Improve the level of detail of the basic world map](https://github.com/photoprism/photoprism/issues/2998)

!!! tldr ""
    We are aware that advanced users could register "non-commercial test accounts" instead, but we think that would not be completely fair and [MapTiler](https://www.maptiler.com/) could then no longer offer them to those in need. Keep in mind that we have many more users than other open source projects that might encourage their users to do this. Likewise, using the OpenSteetMap development API is discouraged for consumer applications like ours, although some projects do it anyway.
