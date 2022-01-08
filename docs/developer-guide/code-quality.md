# Code Quality

!!! example ""
    Code quality has a practical impact on both your agility and the cost of development. 
    You can’t change buggy code fast enough to be truly agile. Existing bugs can easily 
    increase dev costs (and time) by 10x. You can't afford not to fix them.
    — [Allen Holub](https://twitter.com/allenholub/status/1073738216140791808)

## Premature Optimization ##

Don't abstract if you don't have to. Premature optimization often causes pain, leads to bloated code, and fewer
developers understand what's going on. Instead, write tests so you can safely [refactor](https://martinfowler.com/bliki/DefinitionOfRefactoring.html)
when you really need to.

Maintaining small amounts of duplicate code is much easier and less burdensome than choosing the wrong abstraction.

!!! note ""
    Premature optimization is the root of all evil. — Donald Knuth

## Bottom-Up Development ##

Breaking a problem down into small, coherent fragments lends itself to organization. Start with the basic low-level
components and then proceed to higher-level abstractions.

Bottom-up development emphasizes coding and early testing, which can begin before having a detailed understanding 
of the final system - which in practice may never really happen as requirements are constantly evolving.

Advantages of the bottom-up approach are component reusability, agility, and testability.

!!! note ""
    I compared Mel's hand-optimized programs with the same code massaged by the optimizing assembler program, and Mel's always ran faster.
    That was because the “top-down” method of program design hadn't been invented yet, and Mel wouldn't have used it anyway. 
    He wrote the innermost parts of his program loops first. — [The Story of Mel](http://www.catb.org/jargon/html/story-of-mel.html)

## Be Careful with Caching ##

There are only two hard things in Computer Science: cache invalidation and naming things.

!!! note ""
    A cache is just a memory leak you haven't met yet. — Dave Cheney

## Opportunistic Refactoring ##

While we know this is difficult when working with a distributed team, branches, forks, and pull requests, we encourage
all contributors to refactor when they see a specific problem and are working on the same code anyway. This also helps
verify that the changes are helpful and avoids the need for additional refactoring iterations.

!!! note ""
    Ugly code is not a problem as long as there are tests, there are no [security issues](https://photoprism.app/security-policy),
    and it can be easily refactored later. Nobody needs beautiful code that doesn't work.

## Going Fast 🐰 ##

You have to go slow before you can go fast. Keep it simple. Done is better than perfect. Be pragmatic. Stay focused.

!!! note ""
    Feel free to think ahead, just don't code ahead. But also, don't feel the need to decide so many 
    details ahead. Learn enough to get started and build only what you need.
    — [J. B. Rainsberger](https://twitter.com/jbrains/status/1064212803542818816)

## Test Coverage ##

We strive for complete [test coverage](https://martinfowler.com/bliki/TestCoverage.html) as it is a useful tool for finding 
untested parts of our code base. Test coverage is of limited use as a numerical statement of how good our tests are.

!!! note ""
    Code that cannot be tested is flawed.

### Codecov [![Test Coverage](https://codecov.io/gh/photoprism/photoprism/branch/develop/graph/badge.svg)][codecov] ###

A coverage log file created by the Go test runner is automatically sent to [Codecov][codecov] every time our `develop` branch was successfully built and tested on [Travis CI](https://travis-ci.org/photoprism/photoprism). Codecov provides a beautiful UI for displaying coverage reports and renders a badge showing the current test coverage. Custom settings for our report are located in [codecov.yml](https://github.com/photoprism/photoprism/blob/develop/codecov.yml). For example, `range: 50..90` means the badge will be green if coverage is >= 90% and red if it is <= 50%.

## Quality Reports [![Code Quality](https://goreportcard.com/badge/github.com/photoprism/photoprism)][goreport] ##

[goreportcard.com][goreport] finds typical issues in Go source code

!!! note ""
    Not every problem reported by tools is really important and needs to be fixed immediately. Use the reports as
    inspiration when you need some.

[goreport]: https://goreportcard.com/report/github.com/photoprism/photoprism
[codacy]: https://www.codacy.com/project/lastzero/photoprism/dashboard
[codecov]: https://codecov.io/gh/photoprism/photoprism
