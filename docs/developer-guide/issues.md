# Issues

We use GitHub issues for managing [bugs](https://github.com/photoprism/photoprism/labels/bug), 
[ideas](https://github.com/photoprism/photoprism/labels/idea),
and [todos](https://github.com/photoprism/photoprism/labels/todo).
Issues labeled [help wanted](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) / [easy](https://github.com/photoprism/photoprism/issues?q=is%3Aissue+is%3Aopen+label%3Aeasy) can be good (first) contributions.
Feel free to [contact us](../contact.md) if you are unsure or want to work on something specific.

!!! example ""
    Our vision is to provide the most user- and privacy-friendly solution to keep your pictures organized and accessible.

### How to Write User Stories ###

Start describing new ideas and tasks with a [user story](https://en.wikipedia.org/wiki/User_story) similar to this one:

<tt>As a [type of person] I'd like to be able to [do something] so that I can [get some result].</tt>

This makes it easier for everyone to understand who wants what and why.

!!! tldr ""
    Reading between the lines consumes a lot of time that can be used [more effectively](#effectiveness-efficiency).
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

### Effectiveness > Efficiency ###

Optimize for effectiveness before efficiency.

!!! note ""
    It is fundamentally the confusion between effectiveness and efficiency that stands between doing the right things and doing things right. There is surely nothing quite so useless as doing with great efficiency what should not be done at all. — <cite>[Peter Drucker](https://en.wikipedia.org/wiki/Peter_Drucker)</cite>

[![Feature Factory](https://dl.photoprism.app/img/diagrams/feature-factory.jpg)](https://twitter.com/johncutlefish/status/780102280162840576)

### Upcoming Features and Improvements ###

Our [public roadmap](https://github.com/photoprism/photoprism/projects/5) shows what tasks are in progress,
what needs testing, and which features are going to be implemented next.

You are welcome to submit specific feature requests via [GitHub Issues](https://github.com/photoprism/photoprism/issues)
if you have verified that no similar [idea](https://github.com/photoprism/photoprism/labels/idea) or
[todo](https://github.com/photoprism/photoprism/labels/todo) already exists. Give ideas you like a thumbs-up 👍  ,
so that we know what is most popular.
