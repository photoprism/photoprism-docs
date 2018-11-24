PhotoPrism Documentation
========================

This repository contains the source files of [PhotoPrism](https://photoprism.org)'s documentation in markdown.

They are meant to be parsed with the [Mkdocs](https://www.mkdocs.org/) documentation builder to build the HTML documentation on [docs.photoprism.org](https://docs.photoprism.org/).

## Contributing changes

**Pull Requests should use the `master` branch by default.**

Though arguably less convenient to edit than a wiki, this git repository is meant to receive pull requests to always improve the documentation, add new pages, etc. Having direct access to the source files in a revision control system is a big plus to ensure the quality of our documentation.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Building with Mkdocs

To build the HTML, you need to install [Mkdocs](https://www.mkdocs.org/).

Is is best installed using [pip](https://pip.pypa.io), Python's module installer. On a Mac you can run:

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

### Editing existing pages

To edit an existing page, locate its .md source file and open it in your favourite text editor. You can then commit the changes, push them to your fork and make a pull request.

## License

All the content of this repository is licensed under the Attribution-ShareAlike 4.0 International license ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).
