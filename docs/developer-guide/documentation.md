# Documentation

## Package Documentation (GoDoc) ##

[Godoc parses Go source code](https://blog.golang.org/godoc-documenting-go-code) - including comments - and produces documentation as HTML or plain text. The end result is documentation tightly coupled with the code it documents:

+ [cmd/photoprism](https://godoc.org/github.com/photoprism/photoprism/cmd/photoprism) - main application
+ [internal/photoprism](https://godoc.org/github.com/photoprism/photoprism/internal/photoprism) - main library package
+ [internal/server](https://godoc.org/github.com/photoprism/photoprism/internal/server) - server initialization and routing
+ [internal/api](https://godoc.org/github.com/photoprism/photoprism/internal/api) - server api 
+ [internal/commands](https://godoc.org/github.com/photoprism/photoprism/internal/commands) - command line interface
+ [internal/form](https://godoc.org/github.com/photoprism/photoprism/internal/form) - input validation (based on [gin](https://github.com/gin-gonic/gin#model-binding-and-validation))
+ [internal/entity](https://godoc.org/github.com/photoprism/photoprism/internal/entity) - models (based on [GORM](http://gorm.io/))

## Wiki ##

In addition to this Developer Guide, we also use a [Wiki](https://github.com/photoprism/photoprism/wiki).
Pages are currently migrated and updated.

Our Wiki is open to editing by anyone, feel free to improve it without asking for permission as long as you don't rename or remove existing pages.

## User Guide on [docs.photoprism.org](https://docs.photoprism.org/en/latest/) ##

[github.com/photoprism/photoprism-docs](https://github.com/photoprism/photoprism-docs) contains the source files of our User Guide in [Markdown](https://www.mkdocs.org/user-guide/writing-your-docs/#writing-with-markdown).

They are meant to be parsed with the [Mkdocs](https://www.mkdocs.org/) documentation builder to build the HTML documentation on [docs.photoprism.org](https://docs.photoprism.org/).

### Contributing changes ###

**Pull Requests should use the `master` branch by default.**

Though less convenient to edit than a Wiki, our `photoprism-docs` repository is meant to receive pull requests to always improve the documentation, add new pages, etc. Having direct access to the source files in a revision control system is a big plus to ensure the quality of our end user documentation.

### Project layout ###

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

### Building with Mkdocs ###

To build the HTML, you need to install [Mkdocs](https://www.mkdocs.org/).

It is best installed using [pip](https://pip.pypa.io), Python's module installer. On a Mac you can run:

```sh
brew install python
pip3 install mkdocs
pip3 install mkdocs-material
```

You can then build the HTML documentation from the root folder of this repository with:

```sh
mkdocs build
```

or start a server that listens on http://127.0.0.1:8000

```sh
mkdocs server
```

#### Editing existing pages ####

To edit an existing page, locate its .md source file and open it in your favourite text editor. You can then commit the changes, push them to your fork and make a pull request.
