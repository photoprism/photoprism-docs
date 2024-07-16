# Web Service API

## REST API Endpoints

For the currently implemented REST request endpoints available under `/api/v1`, please refer to the automatically generated [backend API documentation](https://github.com/photoprism/photoprism/issues/2132#issuecomment-2227337416) as well as the [request forms](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form) and [entity models](https://pkg.go.dev/github.com/photoprism/photoprism/internal/entity) in our [public repository](https://github.com/photoprism/photoprism/tree/develop/internal):

- https://pkg.go.dev/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

API request bodies and responses are usually JSON-encoded, except for [binary data](thumbnails.md) and some of the [OAuth2 endpoints](oauth2.md#server-endpoints). Note that the [`Content-Type`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type) header must be set to `application/json` for this, as the request may otherwise fail with [error 400](https://github.com/photoprism/photoprism/issues/4354).

!!! example ""
    **We welcome any contributions that help improve our API docs and make them easier to use for developers.** To learn how to access the API while our [Swagger documentation](docs.md) is [not complete yet](https://github.com/photoprism/photoprism/issues/2132#issuecomment-2227337416), we recommend checking the requests in the [browser console](../../getting-started/troubleshooting/logs.md#__tabbed_1_2) that our JS frontend sends when you perform actions like creating an album - and then use the same method, URI, encoding, value names and types for sending requests with your own application.

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

[Learn more ›](auth.md)

!!! example ""
    [App passwords](../../user-guide/settings/account.md#apps-and-devices) can be used as [access tokens](auth.md#access-tokens) in the *Bearer Authorization* header without first creating a session access token, and to obtain short-lived session access tokens through the `POST /api/v1/session` endpoint.

## Service Discovery Endpoints

### OAuth2 Authorization Server

```
/.well-known/oauth-authorization-server
```

↪ <https://demo.photoprism.app/.well-known/oauth-authorization-server>

[Learn more ›](oauth2.md)

### OpenID Configuration

It is not yet possible to use PhotoPrism as an OpenID Connect (OIDC) [Identity Provider](oidc.md#identity-providers), since not all the required [endpoints](https://github.com/photoprism/photoprism/issues/4368) and [grant types](oauth2.md) have been fully implemented. However, querying the `/.well-known/openid-configuration` endpoint shows what has already been implemented, so the missing capabilities can be identified and added over time.

↪ <https://demo.photoprism.app/.well-known/openid-configuration>

[Learn more ›](oidc.md)

## Deprecation Policy

Our REST API endpoints are currently not covered by an official deprecation policy, so some routes and request parameters may change as we add new features in upcoming releases.

However, we avoid making breaking changes, especially to endpoints that we know other developers are using.
