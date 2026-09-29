# Using a Reverse Proxy

A reverse proxy sits in front of PhotoPrism to terminate TLS, serve your public hostname, and apply
its own request filtering. Pick your server from the list for a working configuration:
[Traefik](traefik.md), [Caddy 2](caddy-2.md), [NGINX](nginx.md), [Apache 2.4](apache-2.md),
[SWAG](swag.md), or [HAProxy](haproxy.md).

The settings below apply whichever one you use, so they are worth getting right before you start on
a specific configuration.

!!! danger "Getting Support"
    Reverse proxies are easy to misconfigure, and we cannot
    [provide individual support](https://www.photoprism.app/kb/getting-support/) for proxy-related
    problems such as failed uploads, connection errors, broken thumbnails, or video playback issues.
    Please ask your proxy's community for help, or consider [Traefik](traefik.md) if you prefer a
    simpler setup.

## Public Site URL

Set [the public Site URL](../config-options.md#site-information) to the external `https://` address
your users open, so that links, shared albums, and redirects point at the right host. A Site URL
that still refers to an internal address or port is the most common cause of links that work for
you and not for anyone else.

## TLS Termination

Let the proxy manage certificates and keep PhotoPrism's own TLS disabled with
[`PHOTOPRISM_DISABLE_TLS`](../config-options.md#web-server), so the two do not both try to serve
HTTPS. Expose only ports 80 and 443 to the internet and keep PhotoPrism's own port, 2342 by default,
private.

## Client Addresses

When a proxy forwards a request, PhotoPrism sees the connection coming from the proxy rather than
from the browser. [`PHOTOPRISM_TRUSTED_PROXY`](../config-options.md#networking) determines which
hosts it accepts forwarded client information from, so that rate limits and logs are attributed to
the browser that sent the request.

The default covers the address range Docker uses for its internal networks, which is where a proxy
running alongside PhotoPrism normally connects from. If yours connects from a different address,
set this to that address or range, for example:

- a proxy on another host: its IP address, e.g. `192.168.1.10`;
- a proxy on the same host while PhotoPrism runs without Docker or with host networking, so the
  proxy connects to `localhost`: `127.0.0.1, ::1`.

Keep a value configured whenever a proxy is in front of PhotoPrism: with none, every request appears
to come from the proxy, so a rate limit reached by one person can affect everyone behind it.

### Forwarding Headers

The proxy must add the address it received the request from to the `X-Forwarded-For` header, and
PhotoPrism reads that header only from the addresses listed above:

- Traefik and Caddy add it automatically.
- NGINX: `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`, as in [our example](nginx.md).
  Setting only `X-Real-IP` is not enough.
- HAProxy: `option forwardfor`, as in [our example](haproxy.md).
- Apache adds it by default; do not set `ProxyAddHeaders Off`.

Only list addresses whose connections all pass through such a proxy. Tools that forward connections
without adding the header, such as TCP tunnels, port forwarders, and TLS passthrough routers, should
not connect from a listed address. If one runs on the same host or in the same Docker network as
your proxy, set `PHOTOPRISM_TRUSTED_PROXY` to the proxy's own address only.

### Without a Proxy

If clients connect to PhotoPrism directly, no forwarded headers are needed. Set
`PHOTOPRISM_TRUSTED_PROXY: ""` so that none are accepted, and PhotoPrism uses the address of each
connection.

If PhotoPrism runs in Docker and is reachable over IPv6 without a proxy, also
[enable IPv6 on its Docker network](https://docs.docker.com/engine/daemon/ipv6/) (`enable_ipv6: true`),
so that it sees the client's real IPv6 address. Docker then publishes the port over IPv6 with its own
firewall rules, as it already does for IPv4, so check which ports your host firewall and router
expose afterwards.

## WebSocket Connections

PhotoPrism uses a WebSocket to push live updates to the user interface, such as indexing and import
progress. Your proxy must forward the `Upgrade` and `Connection` headers for that connection to
succeed. Without it the app still loads, but it stops reflecting what the server is doing until the
page is reloaded.

## Uploads & Timeouts

Proxies usually cap the size of a request body and the time a response may take, and both defaults
are lower than a photo library needs. Raise the body-size limit so large uploads are not rejected,
and the read timeout so long-running requests are not cut off mid-operation. The exact directives
differ per server and are covered in each guide.
