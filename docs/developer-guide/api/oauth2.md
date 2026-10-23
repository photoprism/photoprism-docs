# OAuth2 Grant Types

The OAuth 2.0 specification is an authorization framework that contains a set of methods, or grants, that a client application can use to obtain an access token. Each grant type is designed for a specific use case:

- [Authorization Code with PKCE](#authorization-code-flow): lets users connect apps and remote [MCP clients](mcp.md) to their account after signing in and confirming access
- [Refresh Token](#refreshing-access-tokens): renews the access tokens of connected apps
- [Client Credentials](auth.md#client-credentials): for services and scripts that are not bound to a user account
- [Password Grant](auth.md#app-passwords): PhotoPrism-specific `password` and `session` grants for creating access tokens

The access token can then be passed to an API endpoint, which checks it to determine validity and [authorization scope](auth.md#authorization-scopes).

The flow for [connecting apps](#connecting-apps) follows [OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1), which consolidates OAuth 2.0 with its current security best practices and is required by the [MCP authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization). The other grants are OAuth 2.0 grants; the password grant is not part of OAuth 2.1.

## Server Endpoints

| Resource                                                              | Endpoint                  | Methods |
|-----------------------------------------------------------------------|---------------------------|---------|
| [Authorization](https://github.com/photoprism/photoprism/issues/4368) | `/api/v1/oauth/authorize` | `GET`   |
| [Token](https://github.com/photoprism/photoprism/issues/3943)         | `/api/v1/oauth/token`     | `POST`  |
| [UserInfo](https://github.com/photoprism/photoprism/issues/4369)      | `/api/v1/oauth/userinfo`  | `GET`   |
| [Revocation](https://github.com/photoprism/photoprism/issues/3943)    | `/api/v1/oauth/revoke`    | `POST`  |
| Registration                                                          | not implemented           |         |
| Introspection                                                         | not implemented           |         |
| End Session                                                           | not implemented           |         |
| Device Authorization                                                  | not implemented           |         |

Clients can query the `/.well-known/oauth-authorization-server` and `/.well-known/openid-configuration` endpoints for automatic service discovery:

- <https://demo.photoprism.app/.well-known/oauth-authorization-server>
- <https://demo.photoprism.app/.well-known/openid-configuration>

!!! example ""
    The token endpoint accepts `authorization_code` and `refresh_token` requests from [app clients](#connecting-apps), `client_credentials` requests, and the PhotoPrism-specific `password` and `session` grants. The userinfo endpoint is currently a placeholder that returns `405 Method Not Allowed`, and the discovery metadata only advertises what the instance supports with its current configuration. For example, the `code` response type, the `authorization_code` and `refresh_token` grants, and the `S256` code challenge method are not listed when connecting apps is disabled.

## Connecting Apps

Users can connect apps and remote [MCP clients](mcp.md) to their account with the [OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1) Authorization Code flow and [PKCE](https://datatracker.ietf.org/doc/html/rfc7636). The app sends them to the instance, where they sign in if needed and confirm the access it requests. The app then receives an access token for the [MCP endpoint](mcp.md) and a refresh token, so users do not have to create and copy an [access token](auth.md#access-tokens) themselves.

App clients are public clients: they authenticate with their `client_id` only and have no client secret. An app can be known to the instance in two ways:

- **Registered Clients:** the administrator registers the app with its redirect URIs, see [Registering App Clients](auth.md#app-clients).
- **Client ID Metadata Documents:** the `client_id` is an HTTPS URL at which the app publishes its [client metadata](https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/) as JSON, so that it can connect without being registered first. These are only accepted if the `--oauth-apps` option allows the origin of the URL, see [Configuration](#configuration).

### Configuration

The `PHOTOPRISM_OAUTH_APPS` environment variable, the `--oauth-apps` command flag, or the `OAuthApps` setting in [`options.yml`](../../getting-started/config-files/index.md) controls which apps users can connect:

| Value                         | Apps That Users Can Connect                                                                  |
|-------------------------------|----------------------------------------------------------------------------------------------|
| `registered` (default)        | Only apps registered with `photoprism clients add`                                           |
| `https://a.example,https://…` | Registered apps and apps whose client metadata documents are published at one of the origins |
| `any`                         | Registered apps and apps whose client metadata documents are published on any public host    |
| `none`                        | None; the Authorization Code flow is disabled                                                |

Connecting apps is not available in [public mode](../../getting-started/config-options.md#authentication), and the [MCP endpoint](mcp.md) must not be disabled with `PHOTOPRISM_DISABLE_MCP` for the access tokens to be usable.

### Authorization Code Flow

1. The app creates a random `code_verifier` and its `S256` `code_challenge`, as described in [RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636#section-4).
2. It opens the authorization endpoint in a browser:

    ```
    GET /api/v1/oauth/authorize?response_type=code&client_id=<client-id>&redirect_uri=<redirect-uri>&scope=mcp&state=<state>&code_challenge=<code-challenge>&code_challenge_method=S256&resource=<site-url>api/v1/mcp
    ```

3. The user signs in if needed and confirms the requested access on the consent page. Only accounts whose role may use the [MCP endpoint](mcp.md#authorization), and for which MCP is not turned off, can allow access. Apps that call a [library tool](mcp.md#library-tools) later ask the user to approve access to that part of the library.
4. The instance redirects the browser to the redirect URI with `code`, `state` and `iss` query parameters. If the user denies access, the redirect URI receives an `error` parameter instead, for example `access_denied`.
5. The app redeems the code within one minute:

    ```bash
    curl -X POST https://photos.example.com/api/v1/oauth/token \
      -d grant_type=authorization_code \
      -d client_id=<client-id> \
      -d code=<code> \
      -d redirect_uri=<redirect-uri> \
      -d code_verifier=<code-verifier>
    ```

6. The response contains the `access_token`, `token_type`, `expires_in` (one hour), `refresh_token`, and the granted `scope`.

Request parameters:

| Parameter               | Description                                                                                                                                                                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `response_type`         | Must be `code`                                                                                                                                                                                                                                |
| `client_id`             | ID of a registered app client, or the URL of a client metadata document                                                                                                                                                                       |
| `redirect_uri`          | One of the redirect URIs of the client, which must match exactly; for loopback addresses, the port may differ                                                                                                                                 |
| `scope`                 | Space-separated scopes; `mcp` is always included, and apps may also request the library resources `photos`, `videos`, `albums`, `favorites`, `moments`, `calendar`, `folders`, `places`, `labels`, `people`, `cameras`, `lenses`, and `files` |
| `state`                 | Value that the app uses to match the response to its request (recommended)                                                                                                                                                                    |
| `code_challenge`        | Base64url-encoded SHA-256 hash of the code verifier (43 characters)                                                                                                                                                                           |
| `code_challenge_method` | Must be `S256`                                                                                                                                                                                                                                |
| `resource`              | Optional; if specified, it must be the URL of the [MCP endpoint](mcp.md), e.g. `https://photos.example.com/api/v1/mcp`                                                                                                                        |

Redirect URIs must be HTTPS URLs, HTTP URLs on a loopback address such as `http://127.0.0.1:8765/callback`, with any port, or private-use URI schemes for native apps such as `app.example:/callback` ([RFC 8252](https://datatracker.ietf.org/doc/html/rfc8252#section-7.1)). Each parameter may only be specified once.

### Refreshing Access Tokens

Access tokens of connected apps are valid for one hour. To get a new one, the app sends its refresh token to the token endpoint:

```bash
curl -X POST https://photos.example.com/api/v1/oauth/token \
  -d grant_type=refresh_token \
  -d client_id=<client-id> \
  -d refresh_token=<refresh-token>
```

Each response contains a new refresh token, which replaces the previous one. Apps should store it and use each refresh token only once, since presenting a refresh token that was already replaced disconnects the app. The connection also ends after 90 days without use, when the user disconnects the app, or when the account password changes.

### Disconnecting Apps

Users can see and disconnect the apps connected to their account under *Settings > Account > Connected Apps*. Apps can disconnect themselves by sending their refresh token to the revocation endpoint:

```bash
curl -X POST https://photos.example.com/api/v1/oauth/revoke \
  -d client_id=<client-id> \
  -d token=<refresh-token> \
  -d token_type_hint=refresh_token
```

| Endpoint                             | Method   | Description                                   |
|--------------------------------------|----------|-----------------------------------------------|
| `/api/v1/users/{uid}/grants`         | `GET`    | Lists the apps connected to the account       |
| `/api/v1/users/{uid}/grants/{grant}` | `DELETE` | Disconnects an app and ends its access tokens |

The `photoprism auth reset`, `photoprism clients reset`, and `photoprism users reset` commands also remove all app connections.

## Access Tokens

When clients have a valid [access token](auth.md#access-tokens), e.g. obtained through the `POST /api/v1/oauth/token` endpoint, they can use a standard *Bearer Authorization* header to authenticate their requests:

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
    Access tokens issued to [connected apps](#connecting-apps) can only be used with the [MCP endpoint](mcp.md). [App passwords](../../user-guide/settings/account.md#apps-and-devices) can be used as [access tokens](auth.md#access-tokens) in the *Bearer Authorization* header without first creating a session access token, and to obtain short-lived session access tokens through the `POST /api/v1/session` endpoint.

## Related Issues

- [API: Expose Prometheus-style metrics endpoint #3730](https://github.com/photoprism/photoprism/pull/3730)
- [Monitoring: Add a Prometheus-compatible API endpoint #213](https://github.com/photoprism/photoprism/issues/213)
- [Account: Add Support for 2-Factor Authentication #808](https://github.com/photoprism/photoprism/issues/808)
- [Account: Add Support for OpenID Connect (OIDC) #782](https://github.com/photoprism/photoprism/issues/782)
- [Multi-User Photo Gallery with private and shared photos/albums #98](https://github.com/photoprism/photoprism/issues/98)

## Protocol References

- https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- https://datatracker.ietf.org/doc/html/rfc7636
- https://datatracker.ietf.org/doc/html/rfc8252
- https://datatracker.ietf.org/doc/html/rfc8707
- https://datatracker.ietf.org/doc/html/rfc9207
- https://datatracker.ietf.org/doc/html/rfc9728
- https://datatracker.ietf.org/doc/draft-ietf-oauth-client-id-metadata-document/
- https://datatracker.ietf.org/doc/html/rfc8693
- https://prometheus.io/docs/prometheus/latest/configuration/configuration/#oauth2
- https://www.scottbrady91.com/oauth/client-authentication#:~:text=OAuth%20client%20secrets
- https://www.scottbrady91.com/oauth/oauth-is-not-user-authorization
- https://www.oauth.com/oauth2-servers/access-tokens/refreshing-access-tokens/
- https://www.oauth.com/oauth2-servers/access-tokens/access-token-lifetime/
- https://www.oauth.com/oauth2-servers/access-tokens/access-token-response/
- https://www.oauth.com/oauth2-servers/client-registration/client-id-secret/
- https://www.oauth.com/oauth2-servers/authorization/the-authorization-request/
- https://www.oauth.com/oauth2-servers/authorization/requiring-user-login/
- https://www.oauth.com/oauth2-servers/authorization/the-authorization-interface/
- https://www.oauth.com/oauth2-servers/authorization/the-authorization-response/
- https://learn.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens
- https://oauth.net/2/grant-types/client-credentials/
- https://oauth.net/2/scope/
- https://datatracker.ietf.org/doc/html/rfc6749#section-4.4
- https://auth0.com/docs/get-started/authentication-and-authorization-flow/call-your-api-using-the-client-credentials-flow#example-post-to-token-url
- https://auth0.com/intro-to-iam/what-is-oauth-2
- https://auth0.com/docs/authenticate/protocols/oauth
- https://auth0.com/docs/secure/tokens/id-tokens/id-token-structure
- https://auth0.com/docs/authenticate/protocols/openid-connect-protocol
- https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2#grant-type-client-credentials
- https://aaronparecki.com/oauth-2-simplified/
- https://rclone.org/webdav/
- https://owncloud.dev/clients/rclone/webdav-sync-oidc/
- https://www.webdavsystem.com/server/documentation/choosing_authentication/
- http://www.webdav.org/specs/rfc2617.html#rfc.section.4.1
- https://frontegg.com/blog/oauth-grant-types

## Authentication Libraries

- https://github.com/zitadel/oidc
- https://pkg.go.dev/golang.org/x/oauth2
- https://pkg.go.dev/golang.org/x/oauth2/jwt
- https://github.com/go-oauth2/oauth2
- https://github.com/pquerna/otp

## Documentation Examples

- https://learn.microsoft.com/en-us/machine-learning-server/operationalize/how-to-manage-access-tokens
- https://api.stackexchange.com/docs/authentication
- https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/
- https://cloudentity.com/developers/basics/oauth-client-authentication/client-secret-authentication/
- https://developer.okta.com/docs/reference/api/oidc/#get-started
- https://www.authelia.com/integration/openid-connect/introduction/
- https://integrations.goauthentik.io/sources/oauth/
- https://developers.google.com/identity/openid-connect/openid-connect
- https://connect2id.com/products/server/docs/api
- https://connect2id.com/products/server/docs/api/discovery
- https://connect2id.com/products/server/docs/api/authorization
- https://connect2id.com/products/server/docs/api/token
- https://www.zoho.com/accounts/protocol/oauth/token-limits.html
- https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods
- https://help.akana.com/content/current/cm/api_oauth/oauth_oauth20/m_oauth20_getTokenPOST.htm
- https://help.akana.com/content/current/cm/api_oauth/aaref/Ref_Values.htm#values_oauthgranttypes
