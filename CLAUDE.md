# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Authoritative In-Repo References

Read these first — they cover everything below in more depth and are kept more current than this file:

- `AGENTS.md` — contributor and agent conventions, build/preview workflow, deployment, style rules, security notes.
- `CODEMAP.md` — where each piece of content lives under `docs/`, how `mkdocs.yml` / `mkdocs.deploy.yml` / `overrides/` fit together, tooling overview.
- `README.md` — MkDocs install, local preview, deployment overview for new contributors.

If anything below conflicts with those files or with the `Makefile`, those win.

## What This Repo Is

Public documentation for PhotoPrism, published at https://docs.photoprism.app/. It is a **MkDocs Material**-themed site — Markdown sources under `docs/`, rendered to static HTML. There is no application code; changes here are content, navigation, theme overrides, and build config.

**Build tool: ProperDocs.** The site is built with **ProperDocs**, a maintained drop-in fork of MkDocs 1.x (MkDocs core is EOL and its planned 2.0 drops the plugin system). ProperDocs reads our existing `mkdocs.yml`/`mkdocs.deploy.yml` unchanged, keeps every plugin and the `llms.txt` hook working, and silences the build-time MkDocs-2.0/ProperDocs warnings. The `make` targets and CI call `properdocs` (`properdocs build` / `properdocs gh-deploy`); `mkdocs` remains installed only as a library dependency of the Material theme.

The German translation lives in a separate repo, `photoprism/photoprism-docs-de`.

## Common Commands (via `Makefile`)

| Command           | What it does                                                                                                                                                      |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make deps`       | Debian/Ubuntu first-time setup: `apt` Python packages, then `make upgrade`                                                                                        |
| `make install`    | Create `venv/` and install MkDocs Material + `requirements.txt` (no `apt`)                                                                                        |
| `make upgrade`    | Nuke `venv/` and reinstall; use when dependencies drift or you want the latest Material                                                                           |
| `make watch`      | Alias for `make serve` — livereload on `0.0.0.0:8000`, watches `docs/`, `overrides/`, `mkdocs.yml`                                                               |
| `make build`      | Production render using `mkdocs.deploy.yml` → `site/` (do not commit `site/`)                                                                                     |
| `make deploy`     | `properdocs gh-deploy --force --config-file mkdocs.deploy.yml` — emergency manual publish only                                                                    |
| `make merge`      | `develop` → `deploy` merge that triggers the GitHub Actions publish pipeline                                                                                      |
| `make img-resize` | `mogrify` to cap screenshots at `1000x860`; run after adding images to `docs/user-guide/img`, `docs/user-guide/**/img`, or `docs/getting-started/nas/img/asustor` |
| `make fix`        | `chown`/`chmod` the tree when MkDocs can't read or write files                                                                                                    |

There are no repo-wide lint or test make targets — reviewing `make watch` output for build warnings (missing files, broken links in nav, unresolved references) is the closest equivalent. (The one exception is the `llms.txt` build hook, which has its own unit tests — see below.)

MkDocs Material Insiders is now public on PyPI, so **no `GH_TOKEN` is required** in `.env`.

**Building — two options:**

- **Ephemeral container (preferred — installs nothing on the host).** Use the upstream `squidfunk/mkdocs-material` image and add the repo's extra plugins from `requirements.txt` at run time. The image's entrypoint is `mkdocs`, so override it with `--entrypoint sh` to run `pip` first:

  ```sh
  docker run --rm --entrypoint sh -v "$PWD":/docs -w /docs squidfunk/mkdocs-material:latest \
    -c "pip install -r requirements.txt && properdocs build -f mkdocs.deploy.yml"
  ```

  This is a complete, throwaway build env. The container writes `site/` (and `hooks/__pycache__`) as **root** — both are git-ignored; remove with another `docker run … rm -rf site hooks/__pycache__` if they get in the way. Note: the repo's own `Dockerfile` is `FROM squidfunk/mkdocs-material` and nothing else — **not maintained**; don't `docker build` it (it lacks `mkdocs-redirects` / `mkdocs-tooltips`). The *upstream image* is current and maintained — a different thing.
- **Host `venv`.** `make deps` (first time), then `make watch` (livereload) or `make build`. Fine on a dev machine; the container just avoids installing a Python toolchain on the host.

The `llms.txt` build hook (see `LLMS.md`) has unit tests that need no MkDocs install: `cd hooks && python3 -m unittest test_llmstxt`.

## Architecture & Big-Picture Rules

**Two MkDocs configs, both must stay in sync.**
- `mkdocs.yml` — base config: `nav:`, theme options, plugins (`search`, `redirects` with the dev redirect map), Markdown extensions, metadata, edit links. **The `nav:` map is the sole source of truth for site navigation** — a new page is invisible until registered there.
- `mkdocs.deploy.yml` — inherits from `mkdocs.yml`, re-declares the plugins with the **production** redirect map, and adds the `privacy` plugin (mirrors external assets at build time) and a `hooks:` entry (`hooks/llmstxt.py`, which generates `/llms.txt` + `/llms-full.txt` — see `LLMS.md`). Used by `make build` and `make deploy` and by the CI pipeline. Production-only concerns live here, not in the base config, so `make watch` stays fast.

When you **add or rename a redirect**, update the redirect entries in **both** configs so local previews and production match. Same for any nav changes that affect URLs.

**Directory ≠ nav hierarchy.** Folder names mirror the canonical URL path, which is sometimes shorter than the nav label. Example: `docs/release-notes.md` renders at `/release-notes/` even though its nav entry is under "User Guide > Release Notes". Preserve these short-URL exceptions when restructuring.

**Content lives under `docs/` only.** Top-level content folders match the main nav: `getting-started/`, `user-guide/`, `developer-guide/`, plus landing/legal pages (`index.md`, `known-issues.md`, `release-notes.md`, `credits.md`, `license/`). Section-specific subfolders (`organize/`, `search/`, `advanced/`, `proxies/`, `ai/`, `vision/`, `api/`, `media/`, `metadata/`, …) have their own local `img/` directories — **store images next to the Markdown that references them**, not in the global `docs/img/`.

**Drafts go in `todo/`, not `docs/`.** `todo/` is the staging area for work-in-progress pages (e.g. `todo/developer-guide/setup-fedora.md`). They are not served. Promote into `docs/` and register in `mkdocs.yml` when ready.

**Theme and template overrides.**
- `overrides/main.html` — OG/Twitter cards, favicons, analytics (`a.photoprism.app`), announcement banner, and the site-wide `<meta name="keywords">` (set in the `extrahead` block with a `page.meta.keywords` front-matter override, mirroring how `description` is derived from `site_description`). Review light and dark themes and the approved-domains list when editing.
- `overrides/partials/copyright.html` — footer text.
- `docs/css/custom.css` — scoped overrides for Material; keep selectors tight.

**`site/` and `venv/` are build artifacts.** Never commit them and never edit `site/` by hand.

## Deployment Flow

Work happens on `develop`. **Merging `develop` → `deploy` (e.g. `make merge`) triggers the GitHub Actions pipeline** (`.github/workflows/ci.yml`) which installs `mkdocs-material` + `requirements.txt` and runs `properdocs gh-deploy --force --config-file mkdocs.deploy.yml`, publishing to `gh-pages`. The `web2` server then pulls `gh-pages` every 5 minutes and serves `docs.photoprism.app`. So: **`deploy` branch updates are production releases**, not a staging environment.

**Standard release flow — always perform all steps so `develop` and `deploy` contain the same commits and the local checkout ends on `develop`:**

1. Commit on `develop` and `git push origin develop`.
2. Run `make merge` (or, manually: `git checkout deploy && git pull origin deploy && git merge develop && git push origin deploy`). This fast-forwards `deploy` to match `develop` and kicks off the CI build.
3. Return to `develop` locally: `make merge` does this automatically with a trailing `git checkout develop`; if you ran the steps manually, switch back yourself so the next edit session doesn't accidentally land on `deploy`.

Verify with `git rev-parse develop deploy origin/develop origin/deploy` — all four should print the same SHA when the release is clean.

`make deploy` pushes to `gh-pages` from your laptop — reserved for emergencies, and coordinate with maintainers first so the CI pipeline does not overwrite your push.

**`deploy` is a protected branch.** Pushes print `remote: Bypassed rule violations for refs/heads/deploy:` and `Cannot update this protected ref.` in the log but still succeed with exit 0 — the user has an admin override. Don't treat those lines as errors.

## Editing Guardrails

- **`docs/getting-started/config-options.md` is auto-generated on release.** Do not hand-edit it — changes will be overwritten. When a new env var or flag needs to surface in docs, update the manually-maintained page that describes the feature (e.g. `docs/developer-guide/vision/face-recognition.md`, `docs/user-guide/settings/advanced.md`) and link to the auto-generated table for the full list.
- **Package READMEs in the main PhotoPrism repo are canonical.** Before rewriting a developer-guide page, check your local `photoprism/photoprism` checkout at `internal/<package>/README.md` — e.g. `internal/ai/face/README.md`, `internal/thumb/README.md`, `internal/meta/README.md`. These are kept more current than docs and usually contain the exact thresholds, benchmarks, and test recipes you need. Link to them from the dev-guide page rather than duplicating the content.
- **Don't rewrite historical `release-notes.md` entries** to reflect later removals or changes. Past entries (e.g. "Replaced `disintegration/imaging`…") stay as-is — they are the record of what shipped that release. Update the *current* pages that describe the feature instead.
- **The user sometimes edits docs manually between sessions.** Before starting work, `git status` + `git pull --ff-only origin develop` so local changes don't trample their edits (and so you aren't rebuilding content that has already been revised).

## Style Rules Specific to This Repo

- **Chicago-style Title Case** on every heading, nav label, and link title. Rules are spelled out in `AGENTS.md`. Always spell the product name `PhotoPrism` (proper noun, exception to generic rules).
- **Refresh `**Last Updated:**`** at the top of a doc whenever you change its contents (format: `January 20, 2026`, no time). Leave it alone for whitespace-only or pure-formatting edits.
- **Prefer Markdown over raw HTML.** Use Material components (admonitions, tabs, tooltips, mermaid) already configured in `mkdocs.yml` rather than inventing shortcodes.
- **Filenames** are lowercase-kebab (`snake-case.md`); directories mirror nav labels.
- **RFC 3339 UTC timestamps** in request/response examples; valid-looking IDs/UIDs/UUIDs in code samples.
- **CLI examples:** flags before positional arguments unless the command requires otherwise.

## Commit Messages

Concise, imperative subjects with a one-word `Prefix:` indicating scope. Subject ≤80 chars. Examples from recent `git log`:

```
Docs: Update release notes for preview 260420-7d39b2d9f
docs: point developer guide at Gemma 4 and frob/qwen3.5-instruct:4b
```

Do **not** append `Co-Authored-By: Claude …` trailers. No emojis in commit messages. Reference issue or PR IDs when relevant (e.g. `Docker: Use two stage build to reduce image size #123 #5632`).

## GitHub Issues

Only create, edit, close, reopen, or relabel GitHub issues when explicitly asked. When asked:

- Title: imperative mood, `Prefix: Subject` (e.g. `Search: Add filter for RAW image formats`).
- Body starts with a fully-bold one-sentence **User Story**: `**As a <role>, I want <goal>, so that <outcome>.**`
- Body ends with an **Acceptance Criteria** `- [ ]` checklist where each item uses one of `MUST` / `SHOULD` / `MAY`.
