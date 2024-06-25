# Web Service API

## REST API Endpoints

For the currently implemented REST request endpoints available under `/api/v1`, please refer to the automatically generated [backend API documentation](https://pkg.go.dev/github.com/photoprism/photoprism/internal/api) as well as the [request forms](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form) and [entity models](https://pkg.go.dev/github.com/photoprism/photoprism/internal/entity) in our [public repository](https://github.com/photoprism/photoprism/tree/develop/internal):

- https://pkg.go.dev/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

API responses are generally JSON-encoded, except for binary data such as images and videos. When sending requests, please make sure that the `Content-Type` request header is set to `application/json` - unless specified otherwise, e.g. for the [OAuth2 authorization endpoints](#oauth2-authorization-server) that expect form-encoded data. The [error code 400](https://github.com/photoprism/photoprism/issues/4354) in responses indicates that either a required field is missing, the value type of a field is incorrect, or the `Content-Type` header isn't properly set.

Note that our REST API is not currently covered by an official deprecation policy, so some routes and request parameters MAY change as we add new features.
However, we avoid making breaking changes, especially to endpoints that we know other developers are using.

!!! example ""
    **We welcome any contributions that help improve our API docs and make them easier to use for developers.** To learn how to access the API while no [interactive Swagger documentation](https://github.com/photoprism/photoprism/issues/2132) is available, we recommend checking the requests in the [browser console](../../getting-started/troubleshooting/logs.md#__tabbed_1_2) that our JS frontend sends when you perform actions like creating an album - and then use the same method, URI, encoding, value names and types for sending requests with your own application.

## Client Authentication

When clients have a valid access token, e.g. obtained through the `POST /api/v1/session` or `POST /api/v1/oauth/token` endpoint, they can use a standard *Bearer Authorization* header to authenticate their requests:

```
Authorization: Bearer <token>
```

Submitting the access token with a custom `X-Auth-Token` header is supported as well:

```bash
curl -H "X-Auth-Token: 7dbfa37b5a3db2a9e9dd186479018bfe2e3ce5a71fc2f955" \
http://localhost:2342/api/v1/photos?count=10
```

Besides using the API endpoints provided for this, you can also generate valid access tokens by running the `photoprism auth add` command in a terminal.

[Learn more ›](auth.md)

!!! example ""
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

!!! example ""
    Support for [OpenID Connect (OIDC)](https://github.com/photoprism/photoprism/issues/782) is planned for a future release and not yet available.
