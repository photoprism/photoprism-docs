# GitHub Issues

We use [GitHub issues](https://github.com/photoprism/photoprism/issues) for managing [bugs](https://github.com/photoprism/photoprism/labels/bug), 
[ideas](https://github.com/photoprism/photoprism/labels/idea),
and [todos](https://github.com/photoprism/photoprism/labels/todo).
Issues labeled [help wanted](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) / [easy](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3Aeasy) can be good (first) contributions.
Don't hesitate to [contact us](https://www.photoprism.app/contact) if you want to work on something specific or need [help with a pull request](pull-requests.md). 

We kindly ask you not to [report bugs](index.md#creating-bug-reports) via GitHub Issues **unless you are certain to have found a fully reproducible and previously unreported issue** that must be fixed directly in the app.

Note that all issue **subscribers receive an email notification** from GitHub for each new comment, so these should only be used for sharing important information and not for personal discussions/questions.

### How to Write User Stories ###

Start describing new ideas and tasks with a [user story](https://en.wikipedia.org/wiki/User_story) similar to this one:

<tt>As a [type of person] I'd like to be able to [do something] so that I can [get some result].</tt>

This makes it easier for everyone to understand who wants what and why.

!!! example ""
    Reading between the lines consumes a lot of time that can be used [more effectively](code-quality.md#effectiveness-efficiency).
    Vague requirements become even more expensive when the wrong things are implemented, or they don't provide value
    in the way they were implemented.

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
