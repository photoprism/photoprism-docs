# How to contribute

We welcome contributions of any kind including bug reports, pull requests, ideas,
testing, writing documentation, tutorials and blog posts.

Issues labeled [help wanted](https://github.com/photoprism/photoprism/labels/help%20wanted) or
[good first issue](https://github.com/photoprism/photoprism/labels/good%20first%20issue) can be
good first contributions. Let us know if you need additional information or permissions on GitHub
to perform a task.

## Questions?

The most efficient way for asking questions is to write an email to hello@photoprism.org or join our `#photoprism` channel on [gophers.slack.com](https://gophers.slack.com).
If you don't have an account yet, you can create one on [invite.slack.golangbridge.org](https://invite.slack.golangbridge.org/). Please don't use the GitHub issue tracker to ask questions.

## Reporting issues

Please use the GitHub [issue tracker](https://github.com/photoprism/photoprism/issues) to report clearly identified bugs and impediments to us. If you're not sure, start by asking via email or chat.
When reporting an issue, please provide the version in use and information about your environment like browser, operating system, installed memory, and processor type.

## Submitting pull requests

We welcome all contributors and contributions regardless of skill or experience level. If you are interested in helping with the project, we will help you with your contribution.

###  Development environment

It is easiest to build and test the application inside a Docker container. See [Developer Guide](https://github.com/photoprism/photoprism/wiki).

### Code contribution guidelines

Because we want to create the best possible product for our users and the best contribution experience for our developers, we have a set of guidelines which ensure that all contributions are acceptable.
The guidelines are not intended as a filter or barrier to participation.
If you are unfamiliar with the contribution process, we will help you.

To make the contribution process as seamless as possible, we ask for the following:

#### Fork the repository and make your changes
  * If your commit references one or more GitHub issues, always end your commit message body with `see #1234` or `fixes #1234`.
    Replace 1234 with the GitHub issue ID. The last example will close the issue when the commit is merged into `master`.
  * Use a short and descriptive branch name, e.g. **NOT** "patch-1". It's very common but creates a naming conflict each time when a submission is pulled for a review.
#### When you’re ready to create a pull request
  * Sign the [Contributor License Agreement (CLA)](https://cla-assistant.io/photoprism/photoprism).
  * Have test cases for any new code. If you have questions about how to do this, please ask in your pull request.
  * Install [goimports](https://godoc.org/golang.org/x/tools/cmd/goimports) and run `make fmt`.
  * Add [documentation](https://github.com/photoprism/photoprism-docs) if you are adding new features or changing functionality. It is hosted on [docs.photoprism.org](https://docs.photoprism.org/en/latest/) and automatically updates whenever changes are pushed to the repository.

## Donations

Please leave a star on [GitHub](https://github.com/photoprism/photoprism) if you like this project, it provides enough motivation to keep going.
Thank you very much! <3