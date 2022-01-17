# Creating a Pull Request

Because we want to create the best possible product for our users, we have a set of 
guidelines to ensure that all submissions are acceptable:

- **Features and improvements must be fully implemented** so that they can be released at any time without additional work
- **Automated tests are mandatory to ensure the changes work as expected** and to reduce repetitive manual work on our side
- **Frontend components must be responsive** to work and look properly on phones, tablets, and desktop computers; you must have tested them on all major browsers and different devices
- In case you submit database-related changes, they must be tested and compatible with SQLite, MariaDB, and MySQL
- If needed, updated documentation should be provided in a separate pull request

!!! example ""
    These guidelines are not intended as a filter or barrier to participation. If you are unfamiliar with
    Open Source development, we [will help you](https://gitter.im/browseyourlife/community).

### To submit new code... ###

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
  * **Add [tests](https://docs.photoprism.app/developer-guide/tests/) for any new code.** If you have questions about how to do this, please ask in your pull request.
  * Please run `make fmt` to ensure code is properly formatted according to our standards.
  * If all tests are green and you see no other errors, commit your changes. To reference related [GitHub issues](https://github.com/photoprism/photoprism/issues), please end your commit message with the issue ID like `#1234`:
      * `git status -s`
      * `git add .`
      * `git commit -m "Your commit message #1234"`

#### When you are ready... ####

  * Sign the [Contributor License Agreement (CLA)](https://cla-assistant.io/photoprism/photoprism).
  * Verify you didn't forget to add / commit files (output should be empty): 
    * `git status -s`
  * Push all commits to your forked remote repository on GitHub:
    * `git push -u origin feature/your_feature_name`
  * **[Create a pull request](https://help.github.com/articles/creating-a-pull-request/)** with a helpful description of what it does.
  * Wait for our code review and fix remaining issues, if any.
  * Write [documentation](https://docs.photoprism.app/developer-guide/documentation/) if you are adding new features or changing functionality. It is hosted on [docs.photoprism.app](https://docs.photoprism.app/) and automatically updates whenever changes are pushed to the repository.

You can also create a pull request if your changes are not yet complete or working. Just let us know 
it's in progress, so we don't try to merge them. We can help you with a code review or other feedback 
if needed. Please be patient with us.

**Reviewing, testing and finally merging pull requests requires significant resources on our side.
If it's not just a small fix, it can take several months.**
