# GitHub Issues

We use [GitHub issues](https://github.com/photoprism/photoprism/issues) for managing [bugs](https://github.com/photoprism/photoprism/labels/bug), [ideas](https://github.com/photoprism/photoprism/labels/idea), and [enhancements](https://github.com/photoprism/photoprism/labels/enhancement).
Issues labeled [help wanted](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) / [easy](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3Aeasy) can be good (first) contributions.
You are [welcome to email](https://www.photoprism.app/contact) us if you want to [work on something specific](https://github.com/photoprism/photoprism/issues), need [help with a pull request](pull-requests.md), or have something on your mind that you don't want to discuss publicly.

!!! example ""
    When [browsing issues](https://github.com/photoprism/photoprism/issues), please note that **our team and all issue subscribers receive an email notification** from GitHub whenever a new comment is added, so these should only be used for sharing important information and not for [discussions, questions](https://github.com/photoprism/photoprism/discussions), or [expressing personal opinions](https://www.photoprism.app/code-of-conduct).

### Writing User Stories ###

Start describing [new ideas](https://github.com/photoprism/photoprism/labels/idea) and [enhancements](https://github.com/photoprism/photoprism/labels/enhancement) with a [user story](https://en.wikipedia.org/wiki/User_story) similar to this one:

<tt>As a [type of person] I'd like to be able to [do something] so that I can [get some result].</tt>

This makes it easier for everyone to understand who wants what and why.

!!! example ""
    Reading between the lines consumes a lot of time that can be used [more effectively](code-quality.md#effectiveness-efficiency).
    Vague requirements become even more expensive when the wrong things are implemented, or they don't provide value
    in the way they were implemented.

### Creating Bug Reports ###

In order for us to process [new bug reports](https://www.photoprism.app/kb/reporting-bugs), they must include the steps to reproduce the problem, the software versions being used and information about the environment in which the problem occurred, such as [browser type, browser version, browser plug-ins](https://docs.photoprism.app/getting-started/troubleshooting/browsers/), operating system, [storage type](https://docs.photoprism.app/getting-started/troubleshooting/performance/#storage), [processor type](https://docs.photoprism.app/getting-started/troubleshooting/performance/#server-cpu), and [memory size](https://docs.photoprism.app/getting-started/troubleshooting/performance/#memory):

**<https://www.photoprism.app/kb/reporting-bugs>**

We kindly ask you not to report bugs via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.
Before reporting a bug, first use our [Troubleshooting Checklists](../getting-started/troubleshooting/index.md) to determine the cause of your problem. [Contact us](https://www.photoprism.app/contact) or [a community member](https://link.photoprism.app/discussions) if you need help, it could be a configuration problem, or a misunderstanding in how the software works.

This gives us the opportunity to [improve our documentation](https://docs.photoprism.app/getting-started/troubleshooting/) and provide best-in-class support instead of dealing with unclear/duplicate bug reports or triggering a flood of notifications by replying to comments. Thank you very much!

### Acceptance Criteria ###

Issues should include a list of *Acceptance Criteria* that clearly state what is expected.
We recommend using MAY, SHOULD, and MUST as keywords to indicate priorities.

Clickable [checkboxes](https://help.github.com/articles/about-task-lists/) for each item can be created via
[GitHub Markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/):

```
Acceptance Criteria:

- [ ] "Log In" button MUST be visible on /login page
- [ ] "Log In" button MAY be disabled if password field is empty
- [ ] Page SHOULD use existing Vuetify components
- [ ] Login MUST work in latest Firefox, Safari and Chrome
```
