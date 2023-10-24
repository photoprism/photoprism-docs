# Web Service API

For the currently implemented REST request endpoints, please refer to our backend API docs and the public source code repository:
 
- https://godoc.org/github.com/photoprism/photoprism/internal/api
- https://github.com/photoprism/photoprism/tree/develop/internal/api

Our REST API is not currently covered by an official deprecation policy, so some routes and request parameters MAY change as we add new features.
However, we avoid making breaking changes, especially to endpoints that we know other developers are using.
 
!!! tldr ""
    Any contributions that help improve our REST API docs and make them easier to use are greatly appreciated by our team and the developer community.

## Request Examples

### Unauthenticated

```
GET /api/v1/photos?count=10
```

Responses are always JSON encoded, except for binary data like images and videos.

### With Authentication

Authenticated requests require an `X-Session-ID` header to be set along with a [valid session ID](https://github.com/photoprism/photoprism/blob/92df3aa/internal/api/session.go#L102):

```
curl -H "X-Session-ID: xyz" http://localhost:2342/api/v1/photos?count=10
```

For testing, you can use the ID of an active browser session. It is kept in local storage and can be viewed with the browser's web developer tools.

## External Resources ##

- [Mat Ryer: How I write Go HTTP services after seven years](https://medium.com/statuscode/how-i-write-go-http-services-after-seven-years-37c208122831)
