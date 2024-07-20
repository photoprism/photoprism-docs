# Swagger API Documentation

Our [interactive API documentation](https://docs.photoprism.dev/), publicly available at [docs.photoprism.dev](https://docs.photoprism.dev/), is automatically generated from the [source code annotations](https://github.com/swaggo/swag) in the [`/internal/api`](https://github.com/photoprism/photoprism/tree/develop/internal/api) package.

Running the following command in your local [development environment](https://docs.photoprism.app/developer-guide/setup/) will update the [`/internal/api/swagger.json`](https://github.com/photoprism/photoprism/blob/develop/internal/api/swagger.json) file, which contains the API endpoint documentation in machine-readable form:

```bash
make swag
```

You can view it as HTML by navigating to [/api/v1/docs/index.html](https://app.localssl.dev/api/v1/docs/index.html) after you have rebuilt and started `photoprism` with the commands `make build` and `./photoprism start`: 

![swagger-docs](img/swagger.jpg)

Any [help with adding annotations](https://github.com/photoprism/photoprism/issues/2132#issuecomment-2227337416) to improve our documentation is much appreciated!

!!! example ""
    The `/api/v1/docs` API documentation endpoint is disabled in production builds.
