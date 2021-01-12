# Documentation

## User Facing Documentation

User-facing documentation lives in the [photoprism-docs](https://github.com/photoprism/photoprism-docs/)
repository and can be browsed on [docs.photoprism.org](https://docs.photoprism.org/).

See the [README](https://github.com/photoprism/photoprism-docs/#readme) for how to easily edit the docs yourself.

## Package Documentation (GoDoc)

[Godoc parses Go source code](https://blog.golang.org/godoc-documenting-go-code) - including comments - and produces documentation as HTML or plain text. The end result is documentation tightly coupled with the code it documents:

+ [cmd/photoprism](https://godoc.org/github.com/photoprism/photoprism/cmd/photoprism) - main application
+ [internal/photoprism](https://godoc.org/github.com/photoprism/photoprism/internal/photoprism) - main library package
+ [internal/server](https://godoc.org/github.com/photoprism/photoprism/internal/server) - server initialization and routing
+ [internal/api](https://godoc.org/github.com/photoprism/photoprism/internal/api) - server api
+ [internal/commands](https://godoc.org/github.com/photoprism/photoprism/internal/commands) - command line interface
+ [internal/form](https://godoc.org/github.com/photoprism/photoprism/internal/form) - input validation (based on [gin](https://github.com/gin-gonic/gin#model-binding-and-validation))
+ [internal/entity](https://godoc.org/github.com/photoprism/photoprism/internal/entity) - models (based on [GORM](http://gorm.io/))
