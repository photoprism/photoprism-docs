# Reviewing Pull Requests

This guide shows how you can fetch and review GitHub pull requests on your local machine using Git. It builds on the general workflow described in [Pull Requests](pull-requests.md).

## Prerequisites

Before you start, make sure you are familiar with the basic steps for [creating pull requests](pull-requests.md) and running [tests](tests.md). You can verify your Git remotes with:

```bash
git remote -v
```

If you [cloned a fork](https://docs.github.com/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) of our [upstream repository](https://github.com/photoprism/photoprism), you should see the following:

```text
origin   https://github.com/[your username]/photoprism.git (fetch)
origin   https://github.com/[your username]/photoprism.git (push)
upstream https://github.com/photoprism/photoprism.git (fetch)
upstream https://github.com/photoprism/photoprism.git (push)
```

## Fetching a Pull Request into a Local Branch

GitHub exposes pull requests as special references under `refs/pull`. You can fetch them directly into a local branch.

### Example for PR #5297

```bash
git fetch https://github.com/photoprism/photoprism.git pull/5297/head:pr5297
```

This command:

1. Uses `git fetch` to download commits without changing your current branch.
2. Fetches from the main repository via its public [HTTPS URL](https://github.com/photoprism/photoprism.git)
3. Requests the special GitHub reference for the PR head:
    - `pull/5297/head` → `refs/pull/5297/head`
4. Stores it locally as a branch named:
    - `pr5297` → `refs/heads/pr5297`

In other words, it fetches the current head of **PR #5297** and creates or updates a local branch called **`pr5297`** pointing to that code.

After fetching, you can check out the branch:

```bash
git checkout pr5297
# or:
git switch pr5297
```

### Using an Existing Remote

If your `origin` is set to our main GitHub repository and you have a valid SSH key for authentication, you do not need to use the full HTTPS URL:

```bash
git fetch origin pull/5297/head:pr5297
```

If you have cloned a fork and configured our [main repository](https://github.com/photoprism/photoprism) as `upstream`, replace `origin` with `upstream` in this and subsequent command examples:

```bash
git fetch upstream pull/5297/head:pr5297
```

This does the same thing as the [previous example](#example-for-pr-5297), but uses your configured `origin` or `upstream` remote instead of the public HTTPS repository URL.

### General Pattern

You can reuse the same pattern for any pull request:

```bash
git fetch origin pull/<PR_NUMBER>/head:pr<PR_NUMBER>
git checkout pr<PR_NUMBER>
```

For example, for PR #1234:

```bash
git fetch origin pull/1234/head:pr1234
git checkout pr1234
```

## Running Tests & Reviewing Changes

Once you have checked out the PR branch (for example `pr5297`), you can:

- Run tests:
  ```bash
  make test
  ```
- Format code if needed:
  ```bash
  make fmt
  ```
- Inspect the changes:
  ```bash
  git status -s
  git log --oneline --graph --decorate
  git diff develop...pr5297
  ```

See also our [test guidelines](tests.md) and [code quality](code-quality.md) documentation.

## Updating a Local PR Branch

If the contributor pushes new commits to their PR after your initial review, you can update your local branch:

```bash
git checkout pr5297
git fetch origin pull/5297/head:pr5297
```

Because the refspec is the same, this will fast-forward (or update) your local `pr5297` branch to match the latest state of the pull request.

If you prefer, you can combine this with `git switch` and a single `fetch`:

```bash
git fetch origin pull/5297/head:pr5297
git switch pr5297
```

## Fetching the Merged Result of a Pull Request (Optional)

GitHub also exposes the result of merging a PR into the base branch as `pull/<PR_NUMBER>/merge`. This is useful to see the merge result (if it merges cleanly) without actually merging it yourself.

Example for PR #5297:

```bash
git fetch origin pull/5297/merge:pr5297-merge
git checkout pr5297-merge
```

This:

- Fetches `refs/pull/5297/merge` from `origin`,
- Creates (or updates) a local branch named `pr5297-merge` that contains the *merged* result.

You can then check if the merge builds and passes tests:

```bash
make test
```

## Comparing Pull Requests to Local Branches

To see what a PR changes compared to the current `develop` branch:

```bash
git checkout develop
git fetch origin
git merge --ff-only origin/develop  # keep local develop up-to-date

git diff develop...pr5297
```

Useful comparison commands:

- Show files changed:
  ```bash
  git diff --stat develop...pr5297
  ```
- Show a detailed diff with function context:
  ```bash
  git diff -p develop...pr5297
  ```
- Open an interactive view in your editor (examples):
  ```bash
  git difftool develop...pr5297
  ```

## Cleaning Up Local PR Branches

Over time, you may accumulate many local `pr*` branches. You can delete them once they are no longer needed.

Delete a single local branch:

```bash
git branch -d pr5297  # safe delete; will fail if not merged into current branch
git branch -D pr5297  # force delete; use with care
```

List all local PR branches:

```bash
git branch | grep '^  pr'
```

Delete all local PR branches matching a pattern (example):

```bash
git branch | grep '^  pr' | xargs -n 1 git branch -D
```

!!! danger "Be careful when deleting branches"
    Make sure you no longer need the branch, and the pull request is either merged or closed, before deleting it locally. Forced deletion (`git branch -D`) cannot be undone.

## Useful Git Commands

The following commands are often helpful when reviewing pull requests locally.

Pull a PR into a local branch if you are working directly with our main [GitHub repository](https://github.com/photoprism/photoprism) as `origin`:

- `git fetch origin pull/<PR_NUMBER>/head:pr<PR_NUMBER>`
- `git checkout pr<PR_NUMBER>`

Configure our main [GitHub repository](https://github.com/photoprism/photoprism) as the `upstream` remote:

- `git remote -v` – List configured remotes
- `git remote add upstream https://github.com/photoprism/photoprism.git` – Add the main repository as `upstream`

Keep your local `develop` branch up to date if you are using a clone of the `upstream` repository:

- `git checkout develop`
- `git fetch upstream`
- `git merge upstream/develop`

Fetch a PR into a local branch if you are using a clone of the `upstream` repository:

- `git fetch upstream pull/<PR_NUMBER>/head:pr<PR_NUMBER>`
- `git checkout pr<PR_NUMBER>`

Fetch the merged result of a PR:

- `git fetch upstream pull/<PR_NUMBER>/merge:pr<PR_NUMBER>-merge`
- `git checkout pr<PR_NUMBER>-merge`

Compare PR to `develop`:

- `git diff develop...pr<PR_NUMBER>`
- `git diff --stat develop...pr<PR_NUMBER>`

Clean up:

- `git branch -d pr<PR_NUMBER>`
- `git branch -D pr<PR_NUMBER>` – Force
- `git branch | grep '^  pr'`

Use these commands to review changes thoroughly, run tests locally, and help ensure that contributions are stable and ready to be merged.
