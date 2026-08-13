# Preview & Download Tokens

Besides the credentials that authenticate a client (see [Client Authentication](auth.md)), two
short-lived tokens authorize access to media resources. They behave differently on purpose, and the
difference matters if you build URLs yourself or cache them.

|                       | Preview token                                                      | Download token                                               |
|-----------------------|--------------------------------------------------------------------|--------------------------------------------------------------|
| Authorizes            | thumbnails and video streams                                       | originals                                                    |
| Delivered as          | `X-Preview-Token` response header, and in the client config        | `X-Download-Token` response header, and in the client config |
| Appears in the URL as | a **path segment** — `/api/v1/t/{hash}/{token}/{size}`             | a **query parameter** — `/api/v1/dl/{hash}?t={token}`        |
| Scoped to             | a user account, or a single session for link visitors              | a single session                                             |
| Value changes when    | the account's password changes, or the configured value is changed | every time it is issued                                      |

**Do not hardcode a token's format or length.** Both are opaque values, and the download token's
format in particular is expected to change; read the current value from the response header or the
client config on every request rather than storing one.

## Why They Differ

A preview token sits in the **path**, so it is part of the URL and therefore part of the browser and
CDN cache key. If its value changed frequently, every change would produce a new URL for the same
picture and invalidate every cached copy — so a preview token is deliberately stable, and changes
only when an account's password or the configured value does.

Tying the preview token to the account rather than to the session matters for the same reason:
thumbnails already held in the browser cache stay usable after signing out and back in on the same
computer, whereas a per-session value would discard them at every login. Where a CDN or caching proxy
is involved, a configured shared token serves the equivalent purpose one layer up.

A download token is a **query parameter** on a one-shot transfer that is not meant to be cached, so
it can carry a short expiry and be reissued freely. Each one is signed and bound to the session it
was issued to, which is why a fresh value appears on every request.

This is also why the two tokens are not interchangeable, even though a download token is accepted for
previews as well: it is the higher-value credential, since it authorizes originals.

## Configured Tokens

`PHOTOPRISM_PREVIEW_TOKEN` and `PHOTOPRISM_DOWNLOAD_TOKEN` pin a value that the instance accepts in
addition to the ones it issues, so that URLs you construct yourself keep working across restarts. See
[Config Options](../../getting-started/config-options.md#authentication).

- The **preview** token has a value whether or not you set one: when the option is blank, a stable
  value is derived from the instance secret. Setting the option only pins it. Signed-in accounts are
  still served their own token, so setting it does not by itself make their URLs identical.
- The **download** token has no value unless you set one, so an instance that never configured it
  accepts only the session-bound tokens it issues.

Changing a configured value invalidates the URLs that carry it, which also clears the corresponding
browser and CDN caches — see [Security Considerations](thumbnails.md#security-considerations) before
relying on that as a revocation mechanism.

## Public Mode

With [public mode](../../getting-started/config-options.md#authentication) enabled, no token is
validated and the literal string `public` may be used wherever a token is expected.
