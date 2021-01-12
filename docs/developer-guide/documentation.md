# Documentation

## User Facing Documentation

User-facing documentation lives in the [photoprism-docs](https://github.com/photoprism/photoprism-docs/)
repository and can be browsed on [docs.photoprism.org](https://docs.photoprism.org/).

See the [README](https://github.com/photoprism/photoprism-docs/#readme) for how to easily edit the docs yourself.

## Package Documentation (GoDoc)

[Godoc](https://blog.golang.org/godoc-documenting-go-code) generates documentation automatically, so it's tightly coupled to the photoprism source code.

[View docs on pkg.go.dev](https://pkg.go.dev/github.com/photoprism/photoprism){: .md-button .md-button--primary }

Some highlights to explore:

+ [cmd/photoprism](https://pkg.go.dev/github.com/photoprism/photoprism/cmd/photoprism) - main application
+ [internal/photoprism](https://pkg.go.dev/github.com/photoprism/photoprism/internal/photoprism) - main library package
+ [internal/server](https://pkg.go.dev/github.com/photoprism/photoprism/internal/server) - server initialization and routing
+ [internal/api](https://pkg.go.dev/github.com/photoprism/photoprism/internal/api) - server api
+ [internal/commands](https://pkg.go.dev/github.com/photoprism/photoprism/internal/commands) - command line interface
+ [internal/form](https://pkg.go.dev/github.com/photoprism/photoprism/internal/form) - input validation (based on [gin](https://github.com/gin-gonic/gin#model-binding-and-validation))
+ [internal/entity](https://pkg.go.dev/github.com/photoprism/photoprism/internal/entity) - models (based on [GORM](http://gorm.io/))
