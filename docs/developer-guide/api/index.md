Routes and parameters can be found in our API docs:
 
https://godoc.org/github.com/photoprism/photoprism/internal/api

## Examples

### Basic 
```
GET /api/v1/photos?count=10
```

!!! example ""
    Some routes and request parameters MAY change as we add new features. While the API is not covered by an official deprecation policy, we avoid making breaking changes, especially to APIs that we know other developers are using.

### With authentication

PhotoPrism [uses](https://github.com/photoprism/photoprism/blob/92df3aa/internal/api/session.go#L102) `X-Session-ID` HTTP header as authentication method:
```
curl -H "X-Session-ID: xyz" http://localhost:2342/api/v1/photos?count=10
```
Replace `xyz` by `session_id` value of your active browser session, which can be found inside local storage. 

## External Resources ##
- [Mat Ryer: How I write Go HTTP services after seven years](https://medium.com/statuscode/how-i-write-go-http-services-after-seven-years-37c208122831)
