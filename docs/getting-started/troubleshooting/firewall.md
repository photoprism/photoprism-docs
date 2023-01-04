# Configuring Your Firewall

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://photoprism.app/membership) receive direct [technical support](https://photoprism.app/contact) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), try to [determine the cause of your problem](index.md).

## Incoming Requests

Unless you have changed the default configuration, the application is accessible via port 2342 on all network devices. If you are using a firewall, please make sure that the port is accessible from other computers on your network or your app instance is reachable [through a reverse proxy](../proxies/traefik.md):

![](https://dl.photoprism.app/img/diagrams/proxy-cdn.png)

## Outgoing Connections

As explained in our [Privacy Policy](/privacy#section-7), reverse geocoding and interactive world maps depend on retrieving the necessary information [from us](/contact) and [MapTiler AG](https://www.maptiler.com/contacts/), headquartered in Switzerland. Both services are provided with a very high level of privacy and confidentiality.

In order to successfully set up your installation and view location details in PhotoPrism, you must **allow requests to these API endpoints** if you have a firewall installed and make sure your Internet connection is working:

- [ ] dl.photoprism.app
- [ ] cdn.photoprism.app
- [ ] hub.photoprism.app
- [ ] setup.photoprism.app
- [ ] places.photoprism.app
- [ ] places.photoprism.xyz

In addition, the following domains should be whitelisted so that Docker can pull public images, e.g. for MariaDB:

- [ ] auth.docker.io
- [ ] registry-1.docker.io
- [ ] index.docker.io
- [ ] dseasb33srnrn.cloudfront.net
- [ ] production.cloudflare.docker.com

<a href="/privacy#section-7" class="mr-2 hide-print">View Privacy Policy <i class="material-icons">chevron_right</i></a>
<a href="/privacy/gdpr" class="hide-print">View GDPR Statement <i class="material-icons">chevron_right</i></a>
