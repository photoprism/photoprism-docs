# Code Quality

**The quality of code has a practical impact on both your agility and the cost of development:**[^1]

- you can't change buggy and/or bloated code fast enough to be truly agile
- existing bugs can easily increase development costs (and time) by 10x
- the mess eventually becomes so big and so deep that you cannot clean it up anymore[^2]

<figure markdown>
  ![Productivity vs Time](img/productivity-vs-time.jpg){ width="500" }
  <figcaption>Productivity vs Time</figcaption>
</figure>

## Simple Is Beautiful ##

!!! example ""
    Simple, elegant solutions are [more effective](issues.md#effectiveness-efficiency), but they are harder to find than complex ones, and they require more
    time, which we too often believe to be unaffordable. — <cite>Niklaus Wirth, Feb 1985</cite>

## Caching Is Hard ##

There are only two hard things in Computer Science: [cache invalidation](https://msol.io/blog/tech/youre-probably-wrong-about-caching/) and naming things.

!!! example ""
    A cache is just a memory leak you haven't met yet. — <cite>Dave Cheney</cite>

## Bottom-Up Development ##

Breaking a problem down into small, coherent fragments lends itself to organization. Start with the basic low-level
components and then proceed to higher-level abstractions.

Bottom-up development emphasizes coding and early testing, which can begin before having a detailed understanding of the final system. In practice, this may never be the case as requirements are constantly evolving.

Advantages of the bottom-up approach are component reusability, agility, and testability.

!!! example ""
    I compared Mel's hand-optimized programs with the same code massaged by the optimizing assembler program, and Mel's always ran faster.
    That was because the “top-down” method of program design hadn't been invented yet, and Mel wouldn't have used it anyway. 
    He wrote the innermost parts of his program loops first. — <cite>[The Story of Mel](http://www.catb.org/jargon/html/story-of-mel.html)</cite>

## Premature Optimization ##

One of the hardest parts of software development is knowing what to work on.
Don't get carried away implementing unnecessary abstractions and focusing on scalability optimization before you've even validated the functionality of a new feature or improvement.

Instead of spending a lot of time on something you may not need, focus on user needs and [test automation](#code-that-cannot-be-tested-is-flawed).
That way, you'll make sure you're developing the right functionality, and you can [refactor it later](https://martinfowler.com/bliki/DefinitionOfRefactoring.html) for scalability and other non-functional features without breaking anything.

Also keep in mind that it's much easier and less effort to maintain small amounts of duplicate code than to choose the wrong abstraction.

!!! example ""
    Premature optimization is the root of all evil. — <cite>Donald Knuth</cite>

## Opportunistic Refactoring ##

We encourage developers to refactor code when they see a specific problem, although this may seem difficult when working with a distributed team, branches, and pull requests due to potential merge conflicts and delayed feedback.

It is best to do this while you are working on the same code anyway, for example to implement a feature or enhancement. This way you can easily check if the proposed changes make sense.

Releasing imperfect code is not a problem as long as it is [accompanied by automated tests](#code-that-cannot-be-tested-is-flawed). This makes it easy to refactor later without breaking anything or requiring detailed knowledge of the requirements and a lot of time for manual testing. Be pragmatic. Done is better than perfect.

Potential security issues are an important exception. These should never be ignored. If you find a problem, please [report it to us](https://photoprism.app/security-policy) immediately so we can fix it.

!!! example ""
    Feel free to think ahead, just don't code ahead. But also, don't feel the need to decide so many
    details ahead. Learn enough to get started and build only what you need.
    — <cite>[J. B. Rainsberger](https://twitter.com/jbrains/status/1064212803542818816)</cite>

## Go Slow Before You Go Fast 🐰 ##

Read the docs, understand the context, and talk to others to gather missing information before you start coding. Write tests. Stay focused.

Don't worry that this will take too long. Take your time. It's the fastest and only sustainable way to get things done. You have to go slow before you can go fast.

!!! example ""
    All developers with more than a few years experience know that previous messes slow them down. And yet all
    developers feel the pressure to make messes in order to meet deadlines. In short, they don’t take the time
    to go fast! You will not make the deadline by making a mess. Indeed, the mess will slow you down instantly, and
    will force you to miss the deadline. — <cite>Robert C. Martin[^2]</cite>

## Code That Cannot Be Tested Is Flawed ##

We strive for [complete test coverage](https://martinfowler.com/bliki/TestCoverage.html) as it is a useful tool for finding 
untested parts of our code base. Test coverage is of limited use as a numerical statement of how good our tests are.

The *F.I.R.S.T.* principle includes five rules that good tests should follow:[^2]

**Fast:** If tests are slow, you won't run them frequently, which makes them much less useful and increases the cost of development.<br>
**Independent:** You should be able to run each test independently and run the tests in any order you like. When tests depend on each other, then the first one to fail causes a cascade of downstream failures, making diagnosis difficult and hiding downstream defects.<br>
**Repeatable:** If your tests aren’t repeatable in any environment, then you’ll always have an excuse for why they fail. You’ll also find yourself unable to run the tests when the environment isn’t available.<br>
**Self-Validating:** You should not have to read through a log file to tell whether the tests pass. If the tests aren’t
self-validating, then failure can become subjective and running the tests can require a long manual evaluation.<br>
**Timely:** If you write tests after the production code, then you may find the production code to be hard to test. You may decide that some production code is too hard to test. You may not design the production code to be testable.

<!--
### Codecov [![Test Coverage](https://codecov.io/gh/photoprism/photoprism/branch/develop/graph/badge.svg)][codecov] ###

A coverage log file created by the Go test runner is automatically sent to [Codecov][codecov] every time our `develop` branch was successfully built and tested on [Travis CI](https://travis-ci.org/photoprism/photoprism). Codecov provides a beautiful UI for displaying coverage reports and renders a badge showing the current test coverage. Custom settings for our report are located in [codecov.yml](https://github.com/photoprism/photoprism/blob/develop/codecov.yml). For example, `range: 50..90` means the badge will be green if coverage is >= 90% and red if it is <= 50%.
-->

## Use Quality Reports as Inspiration ##

[goreportcard.com][goreport] generates reports on the quality of Open Source Go projects. It uses several measures,
including `gofmt`, `go vet`, `go lint` and `gocyclo`:

[![Code Quality](https://goreportcard.com/badge/github.com/photoprism/photoprism)][goreport]

You can support the developers on [Patreon](https://www.patreon.com/goreportcard).

!!! example ""
    Not every problem reported by tools is really important and needs to be fixed immediately. Use the reports as
    inspiration when you need some.

[goreport]: https://goreportcard.com/report/github.com/photoprism/photoprism
[codacy]: https://www.codacy.com/project/lastzero/photoprism/dashboard
[codecov]: https://codecov.io/gh/photoprism/photoprism

[^1]: https://twitter.com/allenholub/status/1073738216140791808
[^2]: Martin, Robert C. [*Clean Code: A Handbook of Agile Software Craftsmanship*](https://enos.itcollege.ee/~jpoial/oop/naited/Clean%20Code.pdf). Upper Saddle River, NJ: Prentice Hall, 2009.
