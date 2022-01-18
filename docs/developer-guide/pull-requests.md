# Creating a Pull Request

Because we want to create the best possible product for our users, we have a set of 
guidelines to ensure that all submissions are acceptable:

- [ ] **Features and improvements must be fully implemented** so that they can be released at any time without additional work
- [ ] **Automated unit and/or acceptance tests are mandatory** to ensure the changes work as expected and to reduce repetitive manual work on our side
- [ ] **Frontend components must be responsive** to work and look properly on phones, tablets, and desktop computers; you must have tested them on all major browsers and different devices
- [ ] In case you submit database-related changes, they must be tested and compatible with SQLite, MariaDB, and MySQL
- [ ] Updated documentation and translations should be provided (specify if needed)

!!! example ""
    These guidelines are not intended as a filter or barrier to participation. If you are unfamiliar with
    Open Source development, we [will help you](https://gitter.im/browseyourlife/community).

### Contributor License Agreement (CLA) ###

After submitting your first pull request, you will automatically be asked to [accept our CLA](https://cla-assistant.io/photoprism/photoprism):

- This gives us the ability to [(re-)license all code and documentation](https://en.wikipedia.org/wiki/Software_relicensing) at any time, *almost* as if we had created it ourselves (you retain the rights to your own work, which may be different for other CLAs)
- Otherwise, we cannot accept pull requests, as this would mean that we are not able to change the license of our software and documentation at a later time, even though most of it was developed and written by us
- This may be necessary, for example, if the license is incompatible with a larger combined work, we want to remove some restrictions on the AGPL/Creative Commons license, or it turns out that someone is abusing the existing license in a way we don't yet know about
- The lack of a formal contract would also lead to legal uncertainty, as some contributors could later claim that they did not intend to license their code in any way and that it was stolen

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

**Reviewing, testing and finally merging pull requests requires significant resources on our side.
If it's not just a small fix, it can take several months.**
