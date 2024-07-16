# Swagger API Documentation

[Interactive Swagger API](https://docs.photoprism.dev/) docs are automatically generated from [source code annotations](https://github.com/swaggo/swag) in `/internal/api` when you run `make swag` from the project base path in your [development environment](https://docs.photoprism.app/developer-guide/setup/):

```bash
make swag
make build
./photoprism start
```

You can either browse them publicly at [docs.photoprism.dev](https://docs.photoprism.dev/) or locally by navigating to https://app.localssl.dev/api/v1/docs/index.html after building and starting `photoprism` as shown above: 

![swagger-docs](img/swagger.jpg)

Any [help with adding annotations](https://github.com/photoprism/photoprism/issues/2132#issuecomment-2227337416) to improve our documentation is much appreciated!

!!! example ""
    The `/api/v1/docs` API documentation endpoint is disabled in production builds.
