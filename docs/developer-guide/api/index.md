# Web Service API

## REST API Endpoints

For the currently implemented REST request endpoints available under `/api/v1`, please refer to our automatically generated [backend API documentation](https://godoc.org/github.com/photoprism/photoprism/internal/api) and [public repository](https://github.com/photoprism/photoprism):
 
- https://godoc.org/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

Responses are generally JSON encoded, except for binary data like images and videos.

Note that our REST API is not currently covered by an official deprecation policy, so some routes and request parameters MAY change as we add new features.
However, we avoid making breaking changes, especially to endpoints that we know other developers are using.

!!! tldr ""
    Any contributions that help improve our REST API docs and make them easier to use are greatly appreciated by our team and the developer community.

## Client Authentication

When clients have a valid access token, e.g. obtained through the `POST /api/v1/session` or `POST /api/v1/oauth/token` endpoint, they can use a standard *Bearer Authorization* header to authenticate their requests:

```
Authorization: Bearer <access token>
```

Submitting the access token with a custom `X-Auth-Token` header is supported as well:

```bash
curl -H "X-Auth-Token: 7dbfa37b5a3db2a9e9dd186479018bfe2e3ce5a71fc2f955" \
http://localhost:2342/api/v1/photos?count=10
```

Besides using the API endpoints provided for this, you can also generate valid access tokens by running the `photoprism auth add` command in a terminal.

[Learn more ›](auth.md)

!!! note ""
    [App passwords](../../user-guide/settings/account.md#apps-and-devices) can be used as access tokens in the *Bearer Authorization* header without first creating a session access token, and to obtain short-lived session access tokens through the `POST /api/v1/session` endpoint.

## Service Discovery Endpoints

### OAuth2 Authorization Server

```
/.well-known/oauth-authorization-server
```

↪ <https://demo.photoprism.app/.well-known/oauth-authorization-server>

[Learn more ›](oauth2.md)

### OpenID Configuration

```
/.well-known/openid-configuration
```

↪ <https://demo.photoprism.app/.well-known/openid-configuration>

!!! note ""
    Support for [OpenID Connect (OIDC)](https://github.com/photoprism/photoprism/issues/782) is planned for a future release and not yet available.