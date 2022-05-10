# PhotoPrism: Official Documentation (English) #

[![GitHub contributors](https://img.shields.io/github/contributors/photoprism/photoprism-docs.svg)](https://github.com/photoprism/photoprism-docs/graphs/contributors/)
[![Documentation](https://img.shields.io/badge/read-the%20docs-4aa087.svg)][docs]
[![Community Chat](https://img.shields.io/badge/chat-on%20gitter-4aa087.svg)][chat]
[![GitHub Discussions](https://img.shields.io/badge/ask-%20on%20github-4d6a91.svg)][ask]
[![Twitter](https://img.shields.io/badge/follow-@photoprism_app-00acee.svg)][twitter]

This repository contains the source files of [PhotoPrism's](https://photoprism.app/) documentation for editing in human-friendly Markdown files.
They are intended to be parsed with the [Mkdocs documentation builder](https://www.mkdocs.org/) to generate the final HTML pages available at [docs.photoprism.app](https://docs.photoprism.app/).

Although arguably less convenient to work with than a Wiki, this Git repository enables us to easily merge pull requests and constantly improve our documentation in a transparent way.
Direct access to the source files in a revision control system is a big plus to ensure the quality of our documentation.

## Editing Content ##

At the top of each generated page is an *edit this page* link to the corresponding page on GitHub, where you can make changes (and submit pull requests with a few clicks) without needing to know Git or run anything on your system.

To make more extensive changes, fork this repository, modify the corresponding `.md` source files (or create new ones), commit the changes, push them back to your fork, and then submit a pull request to our `master` branch.

### Project Layout ###

```text
mkdocs.yml    # The configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
```

### Build Setup ###

#### Installing MkDocs ####

Run this command the first time you work with this repository on your computer so that the dependencies are installed:

```
make deps
```

#### Fixing Permissions ####

In case files in the project directory have bad permissions and mkdocs cannot read or write them:

```
make fix
```

### Using MkDocs ###

First make sure you have Docker and common development tools like `make` installed on your computer.

Then use this command in the main project directory to download and run the latest version of
[mkdocs-material](https://github.com/squidfunk/mkdocs-material):

```sh
make watch
```

Now open [http://localhost:8000/](http://localhost:8000/) in a browser to view the rendered documentation.

**The content will be updated automatically when changes are detected.**

### Contributor License Agreement (CLA) ###

After submitting your first pull request, you will automatically be asked to [accept our CLA](https://link.photoprism.app/cla):

- this gives us the ability to [(re-)license all code and documentation](https://en.wikipedia.org/wiki/Software_relicensing) at any time, *almost* as if we had created it ourselves (you retain the rights to your own work, which may be different for other CLAs)
- otherwise, we cannot accept pull requests, as this would mean that we are not able to change the license of our software and documentation at a later time, even though most of it was developed and written by us
- this may be necessary, for example, if the license is incompatible with a larger combined work, we want to remove some restrictions on the AGPL/Creative Commons license, or it turns out that someone is abusing the existing license in a way we don't yet know about
- the lack of a formal contract [would also lead to legal uncertainty](https://en.wikipedia.org/wiki/SCO%E2%80%93Linux_disputes) for us and all users, as some contributors could later claim that they did not intend to license their code in any way and that it was stolen

## Related Repositories ##

- [photoprism/photoprism-docs-de](https://github.com/photoprism/photoprism-docs-de) - User Guide (German)
- [photoprism/photoprism](https://github.com/photoprism/photoprism) - Application Source Code

----

*PhotoPrism® is a [registered trademark](https://photoprism.app/trademark). Docs are available under the [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/); additional terms may apply. By using our software, you agree to our [terms of service](https://photoprism.app/terms).*

[docs]: https://docs.photoprism.app/
[chat]: https://link.photoprism.app/chat
[ask]: https://link.photoprism.app/discussions
[twitter]: https://link.photoprism.app/twitter
