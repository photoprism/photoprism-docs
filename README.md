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

#### Create .env File ####

If you have a personal access token for the MkDocs Material Insider edition,
add you GitHub access token to an .env file in the main project directory:

```env
GH_TOKEN=[YOUR TOKEN]
```

New GitHub access tokens can be generated on https://github.com/settings/tokens.

#### Installing MkDocs ####

When using a Debian, Ubuntu, or Mint Linux, run this command the first time you work with this repository on your computer so that the dependencies are installed:

```
make deps
```

Otherwise, install Python 3 and Pip manually and run the following command:

```
make install
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

### Deployment ###

When you merge the main/master branch to `deploy`, the live documentation is automatically created, uploaded and will be visible shortly.

Linux/Unix users can run `make merge` in a terminal. Otherwise, please use the tools provided by your development environment or editor.

### Contributor License Agreement (CLA) ###

After you submit your first pull request, you will be asked to accept our Contributor License Agreement (CLA). Visit [photoprism.app/cla](https://photoprism.app/cla) to learn more.

## Other Documentation ##

- [photoprism/photoprism-docs-de](https://github.com/photoprism/photoprism-docs-de) - User Guide (German)

## Related Repositories ##

- [photoprism/photoprism](https://github.com/photoprism/photoprism) - AI-Powered Photos App for the Decentralized Web 🌈💎✨
- [photoprism/photoprism-contrib](https://github.com/photoprism/photoprism-contrib) - Contributed Resources, Scripts, Tutorials and Examples

----

*PhotoPrism® is a [registered trademark](https://photoprism.app/trademark). By using the software and services we provide, you agree to our [Terms of Service](https://photoprism.app/terms), [Privacy Policy](https://photoprism.app/privacy), and [Code of Conduct](https://photoprism.app/code-of-conduct). Docs are [available](https://link.photoprism.app/github-docs) under the [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/); [additional terms](https://github.com/photoprism/photoprism/blob/develop/assets/README.md) may apply.*

[docs]: https://docs.photoprism.app/
[chat]: https://link.photoprism.app/chat
[ask]: https://link.photoprism.app/discussions
[twitter]: https://link.photoprism.app/twitter
