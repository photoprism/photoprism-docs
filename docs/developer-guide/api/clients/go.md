# Go API Client

The Go client linked below is a third-party project and not part of the core PhotoPrism repository:

- https://github.com/krisnova/photoprism-client-go

Before using it in production, verify that the endpoints, request formats, and authentication flow still match the current server version. Our own source of truth for API behavior remains the generated [Swagger API Documentation](../docs.md) together with [`internal/api/swagger.json`](https://github.com/photoprism/photoprism/blob/develop/internal/api/swagger.json).

If you are building a new Go integration, start with:

- `golang.org/x/oauth2` for token handling
- the generated Swagger/OpenAPI description in `internal/api/swagger.json`
- the handlers and request forms under [`internal/api`](https://github.com/photoprism/photoprism/tree/develop/internal/api) and [`internal/form`](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form)
