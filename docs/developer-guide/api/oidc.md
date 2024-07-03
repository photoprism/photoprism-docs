# OpenID Connect

## Single Sign-On

[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/) extends [OAuth 2.0](oauth2.md) with [Single Sign-On (SSO)](https://developer.okta.com/docs/reference/api/oidc/#userinfo) functionality, allowing users to log in and optionally register via OIDC instead of manually entering a username and password:

![oidc-login](https://github.com/photoprism/photoprism/assets/301686/58e89668-2404-4973-8f6a-e228be389e6c)

### Authentication Flow

![oidc-sso-flow](img/oidc-sso-flow.jpg)

[Learn more ›](https://dl.photoprism.app/pdf/20220113-Volkmann_OpenID_Connect_Thesis.pdf)

### Config Options

| Environment              | CLI Flag        | Default            | Description                                                                                        |
|--------------------------|-----------------|--------------------|----------------------------------------------------------------------------------------------------|
| PHOTOPRISM_OIDC_URI      | --oidc-uri      |                    | identity provider `URI` for single sign-on via OpenID Connect, e.g. "https://accounts.google.com/" |
| PHOTOPRISM_OIDC_CLIENT   | --oidc-client   |                    | client `ID` for single sign-on via OpenID Connect                                                  |
| PHOTOPRISM_OIDC_SECRET   | --oidc-secret   |                    | client `SECRET` for single sign-on via OpenID Connect                                              |
| PHOTOPRISM_OIDC_PROVIDER | --oidc-provider |                    | custom identity provider `NAME`, e.g. "Google"                                                     |
| PHOTOPRISM_OIDC_ICON     | --oidc-icon     |                    | custom identity provider icon `URI`                                                                |
| PHOTOPRISM_OIDC_REDIRECT | --oidc-redirect |                    | automatically redirect unauthenticated users to the configured identity provider                   |
| PHOTOPRISM_OIDC_REGISTER | --oidc-register |                    | allow new users to create an account when they sign in with OpenID Connect                         |
| PHOTOPRISM_OIDC_USERNAME | --oidc-username | preferred_username | username `CLAIM` for OpenID Connect users (preferred_username, email)                              |
| PHOTOPRISM_OIDC_WEBDAV   | --oidc-webdav   |                    | enable WebDAV for new OpenID Connect users if their role allows it                                 |
| PHOTOPRISM_DISABLE_OIDC  | --disable-oidc  |                    | disable single sign-on via OpenID Connect, even if an identity provider has been configured        |


!!! example ""
    Note that your PhotoPrism instance and the OpenID Connect Identity Provider must use HTTPS, otherwise single sign-on via OIDC cannot be enabled.

## Service Discovery

### Client Configuration

Single Sign-On via OpenID Connect can be configured automatically if Identity Providers offer a standardized `/.well-known/openid-configuration` endpoint for [service discovery](https://developer.okta.com/docs/reference/api/oidc/#well-known-oauth-authorization-server):

- <https://accounts.google.com/.well-known/openid-configuration>
- <https://keycloak.localssl.dev/realms/master/.well-known/openid-configuration>

### Server Endpoint

It is not yet possible to use PhotoPrism as an OIDC Identity Provider, since not all the required standards and grant types have been fully implemented. However, querying the `/.well-known/openid-configuration` endpoint will show what is already in place, so the remaining functionality can be identified and added over time as needed:

- <https://demo.photoprism.app/.well-known/openid-configuration>

## Related Issues

- [Auth: Add Support for Single Sign-On via OpenID Connect (OIDC) #782](https://github.com/photoprism/photoprism/issues/782)
- [API: Add `userinfo` endpoint to return information about the logged in user #4369](https://github.com/photoprism/photoprism/issues/4369)
- [API: Add `authorize` endpoint to support the OAuth2 Authorization Code Grant flow #4368](https://github.com/photoprism/photoprism/issues/4368)

## Software Libraries

- https://github.com/zitadel/oidc by https://zitadel.com/
- https://github.com/indigo-dc/oidc-agent
- https://github.com/coreos/go-oidc
- https://github.com/panva/node-oidc-provider
- https://github.com/pulsejet/nextcloud-oidc-login

## Protocol References

- https://openid.net/developers/how-connect-works/
- https://dl.photoprism.app/pdf/20220113-Volkmann_OpenID_Connect_Thesis.pdf
- https://oauth.net/openid-for-verifiable-credentials/
- https://developers.google.com/identity/openid-connect/openid-connect
- https://www.ory.sh/docs/oauth2-oidc/authorization-code-flow
- https://developer.okta.com/docs/concepts/oauth-openid/
- https://developer.okta.com/docs/reference/api/oidc/
- https://developer.okta.com/docs/reference/api/oauth-clients/
- https://auth0.com/docs/authenticate/protocols/openid-connect-protocol
- https://learn.microsoft.com/en-us/entra/identity-platform/scopes-oidc#openid-connect-scopes
- https://owncloud.dev/clients/rclone/webdav-sync-oidc/
- https://blog.cubieserver.de/2022/complete-guide-to-nextcloud-oidc-authentication-with-authentik/
- https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery
- https://connect2id.com/products/server/docs/api/authorization
- https://www.authlete.com/developers/definitive_guide/authorization_endpoint_spec/
