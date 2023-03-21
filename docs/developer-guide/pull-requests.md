# Pull Requests

## Acceptance Criteria ##

Because we want to create the best possible product for our users, we have a set of criteria to ensure that all
submissions are acceptable:

- [ ] **[Features and enhancements](issues.md) must be fully implemented** so that they can be released at any time without additional work
- [ ] **[Automated unit and/or acceptance tests](code-quality.md#code-that-cannot-be-tested-is-flawed) are mandatory** to ensure the changes work as expected and to reduce repetitive manual work
- [ ] **[Frontend components](ui/introduction.md) must be responsive** to work and look properly on phones, tablets, and desktop computers; you must have tested them on [all major browsers](../getting-started/index.md#browsers) and different devices
- [ ] **[Documentation](documentation.md) and [translation](translations.md) updates** should be provided if needed
- [ ] In case you submit database-related changes, they must be tested and [compatible](../getting-started/index.md#databases) with [SQLite 3](https://www.sqlite.org/) and [MariaDB 10.5.12+](https://mariadb.org/)

!!! example ""
    These guidelines are not intended as a filter or barrier to participation. If you are unfamiliar with
    Open Source development, we [will help you](https://link.photoprism.app/chat).

## Contributor License Agreement ##

After you submit your first pull request, you will be asked to accept our Contributor License Agreement (CLA). Visit [photoprism.app/cla](https://www.photoprism.app/cla) to learn more.

## How to Create and Submit a Pull Request ##

#### Fork our repository ####

  * Click the [Fork button](https://help.github.com/articles/working-with-forks/) in the header of our [main repository](https://github.com/photoprism/photoprism)
  * Clone the forked repository on your local computer: 
    * `git clone https://github.com/[your username]/photoprism`
  * Connect your local to our "upstream" main repository by [adding it as a remote](https://help.github.com/articles/configuring-a-remote-for-a-fork/): 
    * `git remote add upstream https://github.com/photoprism/photoprism.git` 
  * Create a new branch from `develop` - it should have a short and descriptive name (not "patch-1") that does not already exist, for example:
    * `git checkout -b feature/your_feature_name` 
  * See also https://guides.github.com/activities/forking/

#### Make your changes ####

  * While you are working on it and your pull request is not merged yet, pull in changes from "upstream" often so that you stay up to date and there is a lower risk for [merge conflicts](https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/):
    * `git fetch upstream`
    * `git merge upstream/develop`
  * We recommend running [tests](https://docs.photoprism.app/developer-guide/tests/) after each change to make sure you didn't break anything:
    * `make test`
  * **Add [tests](https://docs.photoprism.app/developer-guide/tests/) for any new code** 
    * If you have questions about how to do this, please ask in your pull request
  * Run `make fmt` to ensure code is properly formatted according to our standards
  * If all tests are green and you see no other errors, commit your changes. To reference related [GitHub issues](https://github.com/photoprism/photoprism/issues), please end your commit message with the issue ID like `#1234`:
      * `git status -s`
      * `git add .`
      * `git commit -m "Your commit message #1234"`

#### When you are ready... ####

- [ ] Verify you didn't forget to add / commit files, output of `git status -s` should be empty
- [ ] Push all commits to your forked remote repository on GitHub:<br>`git push -u origin feature/your_feature_name`
- [ ] **[Create a pull request](https://help.github.com/articles/creating-a-pull-request/)** with a helpful description of what it does
- [ ] Wait for us to perform a code review and fix the remaining issues, if any
- [ ] Update and/or add [documentation](https://docs.photoprism.app/developer-guide/documentation/) if needed
- [ ] Sign the [Contributor License Agreement (CLA)](#contributor-license-agreement-cla)

You can also create a pull request if your changes are not yet complete or working. Just let us know 
it's in progress, so we don't try to merge them. We can help you with a code review or other feedback 
if needed. Please be patient with us.

**Be aware that reviewing, testing and finally merging pull requests requires significant resources on our side. It can therefore take several months if it is not just a small fix, especially if extensive testing is needed to prevent bugs from getting into our stable version.**

!!! example "Privacy Notice"
    We operate a number of web services that help us develop and maintain our software in collaboration with the open source community, for example [translate.photoprism.app](https://translate.photoprism.app/).
    
    Because many of these apps and tools were originally developed for internal use without a high level of privacy in mind, we ask that you do not enter personal information such as your real name or personal email address if you want it to remain private.
    
    **Personal details may otherwise show up in logs, source code, translation files, commit messages, and pull request comments.**