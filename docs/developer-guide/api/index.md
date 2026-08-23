# Web Service API

## REST API Endpoints

For the currently implemented REST request endpoints available under `/api/v1`, please refer to our [Swagger API Documentation](docs.md), the generated [`swagger.json`](https://github.com/photoprism/photoprism/blob/develop/internal/api/swagger.json), and the [request forms](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form) and [entity models](https://pkg.go.dev/github.com/photoprism/photoprism/internal/entity) in our [public repository](https://github.com/photoprism/photoprism/tree/develop/internal):

- https://pkg.go.dev/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

API request bodies and responses are usually JSON-encoded, except for [binary data](thumbnails.md) and some of the [OAuth2 endpoints](oauth2.md#server-endpoints). Note that the [`Content-Type`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) header must be set to `application/json` for this, as the request may otherwise fail with [error 400](https://github.com/photoprism/photoprism/issues/4354).

!!! example ""
    **We welcome contributions that improve our API docs and make them easier to use.** If you need details that are not documented yet, inspect the requests in the [browser console](../../getting-started/troubleshooting/logs.md#__tabbed_1_2) while using the web app, and compare them with the handlers and forms in [`internal/api`](https://github.com/photoprism/photoprism/tree/develop/internal/api).

## Client Authentication

When clients have a valid [access token](auth.md#access-tokens), e.g. obtained through the `POST /api/v1/session` or `POST /api/v1/oauth/token` endpoint, they can use a standard *Bearer Authorization* header to authenticate their requests:

```
Authorization: Bearer <token>
```

Submitting the [access token](auth.md#access-tokens) with a custom `X-Auth-Token` header is supported as well:

```bash
curl -H "X-Auth-Token: 7dbfa37b5a3db2a9e9dd186479018bfe2e3ce5a71fc2f955" \
http://localhost:2342/api/v1/photos?count=10
```

Besides using the API endpoints provided for this, you can also generate valid [access tokens](auth.md#access-tokens) by running the `photoprism auth add` command in a terminal.

[Learn more ›](auth.md#access-tokens)

!!! example ""
    [App passwords](../../user-guide/settings/account.md#apps-and-devices) can be used as [access tokens](auth.md#access-tokens) in the *Bearer Authorization* header without first creating a session access token, and to obtain short-lived session access tokens through the `POST /api/v1/session` endpoint. Since they authenticate as the account they belong to, app passwords of accounts for which [login is disabled](../../user-guide/users/cli.md#command-options) are limited to [WebDAV](../../user-guide/sync/webdav.md); use a [client access token](../../user-guide/users/client-credentials.md#access-tokens) or [client credentials](../../user-guide/users/client-credentials.md#client-credentials) for API clients that are not tied to a user account.

## Service Discovery Endpoints

### OAuth2 Authorization Server

```
/.well-known/oauth-authorization-server
```

↪ <https://demo.photoprism.app/.well-known/oauth-authorization-server>

[Learn more ›](oauth2.md)

### OpenID Configuration

PhotoPrism publishes OpenID Connect discovery metadata, including a JWKS URI, but it is not yet a complete OIDC Identity Provider. In particular, the authorization and userinfo endpoints are still placeholders, and the discovery metadata currently advertises only the interoperable parts that are implemented today.

↪ <https://demo.photoprism.app/.well-known/openid-configuration>

[Learn more ›](oidc.md)

## Deprecation Policy

Our REST API endpoints are currently not covered by an official deprecation policy, so some routes and request parameters may change as we add new features in upcoming releases.

However, we avoid making breaking changes, especially to endpoints that we know other developers are using.
