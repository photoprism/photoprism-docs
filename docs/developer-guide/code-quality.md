# A Few Words About Code Quality

> Code quality has a practical impact on both your agility and the cost of development. You can’t change buggy code fast enough to be truly agile. Existing bugs can easily increase dev costs (and time) by 10x. You can't afford not to fix them.<br>— <cite>[Allen Holub](https://twitter.com/allenholub/status/1073738216140791808)</cite>

## Abstraction ##

> Premature optimization is the root of all evil.<br>— <cite>Donald Knuth</cite>

Don't abstract when you don't have to. Premature optimization often causes pain, 
results in bloated code, and fewer developers understand what is going on. 
Write tests instead so that you can safely 
[refactor](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) when really needed.

!!! tip
    Maintaining small amounts of duplicate code is cheaper and less work
    than choosing the wrong abstraction.

## Refactoring ##
While we expect this to be difficult when working with a distributed team and pull requests, we encourage all contributors to refactor whenever they see a specific issue and they are working on related code anyways (so that you can validate if your changes are helpful). This way, there is no need for extra refactoring tasks or epics. Let's experiment and see how far we get with this.

!!! tip
    Ugly code is not a problem as long as there are tests, 
    there are no security issues, and it can be easily refactored later. 
    Nobody needs beautiful code that doesn't work.

## Going Fast ##
> Feel free to think ahead, just don't code ahead. But also, don't feel the need to decide so many details ahead. Learn enough to get started and build only what you need.<br>— <cite>[J. B. Rainsberger](https://twitter.com/jbrains/status/1064212803542818816)</cite>

You have to go slow before you can go fast. Keep it simple. Done is better than perfect. Be pragmatic. Stay focused.

## Test Coverage [![Test Coverage](https://codecov.io/gh/photoprism/photoprism/branch/develop/graph/badge.svg)][codecov] ##
[Test coverage](https://martinfowler.com/bliki/TestCoverage.html) is a useful tool for finding untested parts of our codebase. Test coverage is of little use as a numeric statement of how good our tests are.

We strive for complete test coverage. Code that cannot be tested is flawed.

### Codecov ###

A coverage log file created by the Go test runner is automatically sent to [Codecov][codecov] every time our `develop` branch was successfully built and tested on [Travis CI](https://travis-ci.org/photoprism/photoprism). Codecov provides a beautiful UI for displaying coverage reports and renders a badge showing the current test coverage. Custom settings for our report are located in [codecov.yml](https://github.com/photoprism/photoprism/blob/develop/codecov.yml). For example, `range: 50..90` means the badge will be green if coverage is >= 90% and red if it is <= 50%.

## Quality Reports [![Code Quality](https://goreportcard.com/badge/github.com/photoprism/photoprism)][goreport] [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ea5b6b16814540469f384b8ff35ba511)][codacy] ##

[Go Report Card][goreport] finds typical issues in Go code while [Codacy][codacy] is a more general service that also reports issues found in Dockerfiles and other programming languages.

!!! tip
    Not every issue reported by tools is really important and needs to be fixed instantly. Use reports for inspiration when you need some.

[goreport]: https://goreportcard.com/report/github.com/photoprism/photoprism
[codacy]: https://www.codacy.com/project/lastzero/photoprism/dashboard
[codecov]: https://codecov.io/gh/photoprism/photoprism
