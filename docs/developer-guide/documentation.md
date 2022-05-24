# Documentation

## User Facing Documentation

User-facing documentation lives in the [photoprism-docs](https://github.com/photoprism/photoprism-docs/)
repository and can be browsed on [docs.photoprism.app](https://docs.photoprism.app/).

See the [README](https://github.com/photoprism/photoprism-docs/#readme) for how to easily edit the docs yourself.

## Package Documentation (GoDoc)

[Godoc](https://blog.golang.org/godoc-documenting-go-code) generates documentation automatically, so it's tightly coupled to the photoprism source code.

<p class="action-buttons">
    <a class="action-button bold" href="https://pkg.go.dev/github.com/photoprism/photoprism" target="_blank">View Package Docs</a>
</p>

Some highlights to explore:

+ [cmd/photoprism](https://pkg.go.dev/github.com/photoprism/photoprism/cmd/photoprism) - main application
+ [internal/photoprism](https://pkg.go.dev/github.com/photoprism/photoprism/internal/photoprism) - main library package
+ [internal/server](https://pkg.go.dev/github.com/photoprism/photoprism/internal/server) - server initialization and routing
+ [internal/api](https://pkg.go.dev/github.com/photoprism/photoprism/internal/api) - server api
+ [internal/commands](https://pkg.go.dev/github.com/photoprism/photoprism/internal/commands) - command line interface
+ [internal/form](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form) - input validation (based on [gin](https://github.com/gin-gonic/gin#model-binding-and-validation))
+ [internal/entity](https://pkg.go.dev/github.com/photoprism/photoprism/internal/entity) - models (based on [GORM](http://gorm.io/))
