# Frequently Asked Questions

### Can your development environment be used under Windows?

Yes, this is possible if you have [Git](https://git-scm.com/) and [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) installed. However, you are likely to experience problems when [using our Makefile](https://github.com/photoprism/photoprism/blob/develop/Makefile) and other scripts directly on Windows, as they were developed and tested on Linux/Unix.

We therefore recommend not to use [Make](https://www.gnu.org/software/make/) for setting up your [development environment](setup.md) and to instead run the required commands manually from the [main project directory](https://github.com/photoprism/photoprism/tree/develop) (where the [`compose.yaml`](https://github.com/photoprism/photoprism/blob/develop/compose.yaml) file is located):

```bash
docker compose --profile=all pull --ignore-pull-failures
docker compose build
docker compose up
```

Once the services have been built and started as shown above, you can open a terminal session:

```bash
docker compose exec photoprism bash
```

In addition, you should disable the "autocrlf" option in Git under Windows to avoid problems with Linux/Unix line endings:

```bash
git config --global core.autocrlf false
```

That's it! Most of the other [Make](https://www.gnu.org/software/make/) targets are used from within the terminal session, i.e. not under Windows, so no compatibility issues or missing dependencies are to be expected.

[Learn more ›](setup.md#step-3-install-the-dependencies-and-start-developing)

### Why not use a more permissive public license so that, for example, developers at Google can contribute more easily?

Since we had hoped for a collaboration with Google and were aware of [their AGPL policy](https://opensource.google/documentation/reference/using/agpl-policy), PhotoPrism was initially licensed under Apache 2.0, which is much more permissive. However, no one seemed interested, although we did talk to quite a few personal acquaintances at Google. That made it easy for our community to convince us to use AGPL instead.

### Isn't it insecure that thumbnail URLs work even if you are not logged in?

Like most commercial image hosting services, we've chosen to use a **cookie-free thumbnail API** to minimize request latency and avoid unnecessary network traffic. If you were to copy private session cookies and use them in a different browser window, you would have a similar problem, except that they also work for other API endpoints, not just a single image.

Even if URLs were to become invalid every minute: Digital copies are as good as originals. Once shared and downloaded, such images should be considered "leaked" because they are cached and can be re-shared by the recipient at any time, with no sure way to get all copies back. Any form of protection we could provide would essentially be "snake oil", could be circumvented, and would have a negative impact on the user experience, such as disabling the browser cache or context menu.

For the highest level of protection, it is recommended to shield your private server from the public Internet. Always use **HTTPS, a VPN and/or ideally TLS client certificates** and make sure that only people you trust have access to your instance.

Visit [docs.photoprism.app/developer-guide/media/thumbnails/](https://docs.photoprism.app/developer-guide/media/thumbnails/) to learn more.

### Does your software depend on any external services?

As explained in our [Privacy Policy](https://www.photoprism.app/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](https://www.photoprism.app/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.

Your use of these services is [fully covered by us](../getting-started/faq.md#are-the-keys-for-using-interactive-world-maps-provided-free-of-charge). Depending on your usage, this can save you much more than the cost of a [PhotoPrism+ Membership](https://www.photoprism.app/membership), since other providers generally charge usage-based fees and often don't allow you to cache the data they provide, compromising performance and your privacy with unnecessary requests.

In order to use the maps and view location details in PhotoPrism, as well as successfully run our test suite as a developer, you must **allow requests to these API endpoints** if you have a firewall installed and make sure your Internet connection is working.

Should you wish to operate one or both of these services on your own premises, we can set up such a [fully autonomous solution](https://www.photoprism.app/kb/compliance-faq#fully-autonomous-solution) for you, provided you are prepared to cover the initial setup costs as well as ongoing maintenance fees for content licenses and updates.

[View Privacy Policy ›](https://www.photoprism.app/privacy#section-7){ class="pr-3 block-xs" } [View Compliance FAQ ›](https://www.photoprism.app/kb/compliance-faq#privacy)

*Other applications sometimes use the API that [OpenStreetMap](https://operations.osmfoundation.org/policies/tiles/) provides for development and testing. In this case, [their usage](https://operations.osmfoundation.org/policies/tiles/) and [privacy policies](https://wiki.osmfoundation.org/wiki/Privacy_Policy) apply, which means that your request data is stored and used to generate [publicly available reports](https://planet.openstreetmap.org/tile_logs/). This differs from our self-hosted service, which ensures [your privacy](https://www.photoprism.app/privacy) and provides a better user experience with faster loading times.*

### Why do I see connection errors when requesting API keys at startup?

Retrieving location data with [reverse geocoding](https://www.photoprism.app/privacy#section-7) and loading the [interactive world maps](https://www.photoprism.app/privacy#section-8) we provide requires a [connection to external services](#does-your-software-depend-on-any-external-services). Please make sure that [requests to these API endpoints are allowed](../getting-started/troubleshooting/firewall.md#outgoing-connections) if you have a firewall installed, and that your internet connection is working.

[Learn more ›](../getting-started/troubleshooting/firewall.md#outgoing-connections)

### Are the keys for using interactive world maps provided free of charge?

All users have access to a [high-resolution vector map](https://maps.photoprism.app/){:target="_blank"} that we host on [our own infrastructure](https://github.com/photoprism/photoprism/issues/2998){:target="_blank"}, so no commercial API key is required. It is based on [data published by OpenStreetMap](https://planet.openstreetmap.org/){:target="_blank"} (OSM).

In addition, we automatically provide [our members](https://www.photoprism.app/membership) and [business customers](https://www.photoprism.app/teams#compare) with an API key for MapTiler's commercial service, which includes [satellite, outdoor and 3D maps](https://www.photoprism.app/kb/personal#maps-and-places). You can test these on [our public demo](https://try.photoprism.app/library/places){:target="_blank"}.

[Learn more ›](https://www.photoprism.app/kb/personal#maps-and-places)

!!! example ""
    Although experienced users could alternatively register test accounts with a commercial provider to gain access to additional map styles instead of [signing up for a membership](https://www.photoprism.app/membership), we believe this would not be fair. Keep in mind that we have a much larger user base than others who might encourage their users to do so, and that providers might then stop offering free test accounts, which is something we don't want to be responsible for.

### Why don't you use the free map tile service provided by OpenStreetMap?

Other [free and open-source software](https://en.wikipedia.org/wiki/Free_and_open-source_software){:target="_blank"} sometimes uses the public maps that OpenStreetMap provides for development and testing. These are [not intended for end-user applications](https://operations.osmfoundation.org/policies/tiles/) like ours.

Using their service also means that [their usage](https://operations.osmfoundation.org/policies/tiles/) and [privacy policies](https://wiki.osmfoundation.org/wiki/Privacy_Policy) apply, as your request data is stored and used to generate [publicly available reports](https://planet.openstreetmap.org/tile_logs/). This differs from our services, which ensure [a high level of privacy](https://www.photoprism.app/privacy) and provide a better user experience with faster loading times.

*[OSM]: OpenStreetMap
*[OSS]: Open-Source Software
