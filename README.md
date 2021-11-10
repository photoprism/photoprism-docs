PhotoPrism Documentation
========================

[![GitHub contributors](https://img.shields.io/github/contributors/photoprism/photoprism-docs.svg)](https://github.com/photoprism/photoprism-docs/graphs/contributors/)
[![Documentation](https://img.shields.io/badge/read-the%20docs-4aa087.svg)][docs]
[![Community Chat](https://img.shields.io/badge/chat-on%20gitter-4aa087.svg)][chat]
[![GitHub Discussions](https://img.shields.io/badge/ask-%20on%20github-4d6a91.svg)][ask]
[![Twitter](https://img.shields.io/badge/follow-@photoprism_app-00acee.svg)][twitter]

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

First make sure you have Docker and common development tools like `make` installed on your computer.

Then use this command in the main project directory to download and run the latest version of
[mkdocs-material](https://github.com/squidfunk/mkdocs-material):

```sh
make pull watch
```

Now open http://localhost:8000/ in a Web browser to browse the docs.

### Editing existing pages

The top of every documentation page includes an 'Edit this page' link to the equivalent page on GitHub,
where you can make edits (and submit Pull Requests in a few clicks) without needing
any git knowledge or to run anything on your system.

To make more extensive changes, modify corresponding `.md` source files (or create new ones),
commit the changes, push them to your fork and submit a pull request.

## Other repositories on GitHub
  * [photoprism](https://github.com/photoprism/photoprism) - main source code repository
  * [photoprism.github.io](https://github.com/photoprism/photoprism.github.io) - public homepage hosted by GitHub Pages on [photoprism.org](https://photoprism.org)

## License

All the content of this repository is licensed under the Attribution-ShareAlike 4.0 International license ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)).

[paypal]: https://www.paypal.me/photoprism
[docs]: https://docs.photoprism.org/
[chat]: https://gitter.im/browseyourlife/community
[ask]: https://github.com/photoprism/photoprism/discussions
[twitter]: https://twitter.com/photoprism_app
