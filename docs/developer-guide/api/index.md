# Web Service API

For the currently implemented REST request endpoints, please refer to our backend API docs and the public source code repository:
 
- https://godoc.org/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

Responses are generally JSON encoded, except for binary data like images and videos.

Note that our REST API is not currently covered by an official deprecation policy, so some routes and request parameters MAY change as we add new features.
However, we avoid making breaking changes, especially to endpoints that we know other developers are using.

!!! tldr ""
    Any contributions that help improve our REST API docs and make them easier to use are greatly appreciated by our team and the developer community.

## Client Authentication

Authenticated requests require an `X-Auth-Token` or a standard *Bearer Authorization* header with a [valid access token](auth.md), for example:

```
curl -H "X-Auth-Token: 7dbfa37b5a3db2a9e9dd186479018bfe2e3ce5a71fc2f955" \
http://localhost:2342/api/v1/photos?count=10
```

In order to grant access, you can use the `photoprism auth add` command to [generate access tokens](auth.md), optionally also with a limited [scope](auth.md#authorization-scopes) and lifetime.

[Learn more ›](auth.md)

!!! note ""
    Besides using [app passwords](../../user-guide/settings/account.md#apps-and-devices) to create sessions through the `POST /api/v1/session` endpoint, developers can also use them as access tokens in the *Bearer Authorization* header without first creating a session access token.