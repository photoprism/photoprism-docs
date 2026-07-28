# PhotoPrism® Docs Repository Guidelines

**Last Updated:** July 9, 2026

## Purpose

This file serves as a single, up-to-date reference for agents and contributors working on PhotoPrism's public documentation. It explains where canonical content is located, how to preview and ship changes, and which conventions maintain consistency between https://docs.photoprism.app/ and the main application repository at https://github.com/photoprism/photoprism/.

## Sources of Truth

- `README.md` — contributor onboarding, MkDocs overview, and deployment expectations for this repository.
- `mkdocs.yml` — primary navigation tree (Getting Started, User Guide, Developer Guide, About) and metadata used by MkDocs Material. The `nav:` map is the sole source of truth for site navigation, so every new page must be registered there before it becomes visible in the UI.
- `mkdocs.deploy.yml` — release-time configuration that enables the privacy plugin, mirrors remote assets, hosts the production redirect rules, and runs the `llms.txt` build hook (`hooks/llmstxt.py`; see `LLMS.md`).
- Main app references: `AGENTS.md` and `CODEMAP.md` in the main `photoprism/photoprism` repo (https://github.com/photoprism/photoprism) remain authoritative for product behavior, CLI semantics, and backend/frontend boundaries.
- Published docs: https://docs.photoprism.app/ is the live contract; verify edits there before referencing version-specific behavior.
- Contributor process notes: `docs/developer-guide/documentation.md`, `docs/developer-guide/pull-requests.md`, and `docs/developer-guide/reviewing-pull-requests.md` describe how documentation changes are reviewed alongside code.
- Make targets defined in `Makefile` (e.g., `make deps`, `make watch`, `make merge`) are the supported way to install dependencies, run MkDocs, resize images, and deploy.

## Documentation Scope

- MkDocs pulls Markdown from `docs/`, where the top folders align with the site navigation: `getting-started/`, `user-guide/`, and `developer-guide/`. Keep new topics inside these trees to benefit from inherited index pages and local `img/` directories.
- Directory names mirror canonical URLs, not necessarily the navigation hierarchy. For example, `docs/release-notes.md` renders at https://docs.photoprism.app/release-notes/ for a short path, even though its nav entry lives under “User Guide > Release Notes”. Maintain these short-link exceptions when they exist.
- Landing and shared pages live at `docs/index.md`, `docs/known-issues.md`, `docs/release-notes.md`, `docs/credits.md`, and `docs/license/` (AGPL, Apache, and documentation terms). Update these when legal notices or release metadata change.
- Static assets ship from `docs/img/` (global) and the section-specific `img/` folders. Icons and favicons reside in `docs/icons/`; logos include `docs/icons/logo/*.svg` plus `docs/icons/LICENSE`.
- Styling overrides belong in `docs/css/custom.css`. Theme overrides live in `overrides/` (`main.html` for OG/Twitter tags and analytics, `partials/copyright.html` for footer text).
- Work-in-progress drafts go under `todo/` (currently `todo/developer-guide/setup-fedora.md`). Clearly mark TODO files until they are promoted into `docs/`.

## Build & Preview Workflow

- Build tool: the site is built with **ProperDocs**, a maintained drop-in fork of MkDocs 1.x (MkDocs core is EOL; its planned 2.0 removes the plugin system). It reads `mkdocs.yml` unchanged, keeps every plugin and the `llms.txt` hook working, and silences the MkDocs-2.0/ProperDocs build warnings. `make` and CI invoke `properdocs`; `mkdocs` stays installed only as a dependency of the Material theme.
- Local Python environment: run `make deps` on Debian/Ubuntu (installs system packages) or `make install` elsewhere. Both targets create `venv/`, grab MkDocs Material (the former Insiders build now ships via PyPI, so no `GH_TOKEN` is required), and pull all pinned requirements from `requirements.txt`.
- Refresh dependencies with `make upgrade` whenever you need the latest MkDocs Material release; it rebuilds the virtualenv before you start working.
- Preview: `make watch` (alias for `make serve`) invokes `./venv/bin/properdocs serve --watch docs --watch overrides --watch mkdocs.yml -a 0.0.0.0:8000` (ProperDocs enables livereload by default). A common loop is `make upgrade && make watch`, then browse http://localhost:8000/ while it hot-reloads Markdown, templates, and configuration.
- Build artifacts: `make build` renders the production site using `mkdocs.deploy.yml`, while `make deploy` runs `properdocs gh-deploy --force --config-file mkdocs.deploy.yml` for manual GitHub Pages pushes. The rendered HTML lands in `site/` locally—never edit files there by hand or commit that directory.
- Image hygiene: `make img-resize` (ImageMagick `mogrify`) enforces a `1000x860` max width for specific folders. Run it after adding screenshots to `docs/user-guide/img` or `docs/getting-started/**/img`.
- Spell check: `make spellcheck` runs [`typos`](https://github.com/crate-ci/typos) over `docs/`, configured in `_typos.toml`. `make install-typos` fetches a pinned, checksum-verified binary into `bin/` — there is no GitHub Action, and no interpreter or package manager is involved. It only flags words in a curated typo list, so a finding is almost always real; add genuine product terms and personal names to `_typos.toml` rather than working around them. Apply fixes with `./bin/typos --write-changes docs/`.
- Prose style (**optional, under evaluation**): `make vale` runs [`vale`](https://vale.sh/) with the in-repo house style under `styles/PhotoPrism/`, installed the same way via `make install-vale`. It is deliberately **not** a gate — the target swallows a non-zero exit status, and it is not part of `make build`. Findings are advisory while we judge whether prose linting earns its keep; do not treat them as a review blocker.
- Containerized workflow: the repo's own `Dockerfile` (`FROM squidfunk/mkdocs-material:latest`, nothing else) is **not maintained** — don't `docker build` it, as it lacks the extra plugins (`mkdocs-redirects`, `mkdocs-tooltips`). To build without installing a host toolchain, run the *upstream* `squidfunk/mkdocs-material` image and `pip install -r requirements.txt` at run time; the exact command is in `README.md` / `CLAUDE.md` (§ Building in a Container).

## Repository Layout & Ownership

- `mkdocs.yml` defines navigation, metadata (`site_name`, `extra.social`, edit links), plugins (`search`, `redirects`), theme options, and Markdown extensions (pymdownx, tooltips, tabs, mermaid). Always update nav entries and redirect maps in this file when adding or moving pages.
- `mkdocs.deploy.yml` inherits from `mkdocs.yml`, re-declares the plugins with the production redirect map, and adds the `privacy` plugin plus a `hooks:` entry (`hooks/llmstxt.py`, which generates `/llms.txt` + `/llms-full.txt` — see `LLMS.md`). When you add redirects, mirror them in both configs so local previews and production builds behave the same.
- `overrides/` contains the only custom templates. `overrides/main.html` augments meta tags, favicons, analytics, and announcement banners; update it when branding or tracking domains change. `overrides/partials/copyright.html` injects footer copy.
- `docs/css/custom.css` holds layout tweaks for the Material theme; limit overrides to what cannot be configured in `mkdocs.yml` and keep selectors scoped to avoid regressions.
- `LICENSE` (root) covers the repository; `docs/license/docs.md` spells out the documentation license (CC BY-NC-SA 4.0). Keep legal text in sync with the main application repository when terms change.
- Helper directories: `venv/` (local virtualenv), `site/` (build output), and `todo/` (drafts) are workspace artifacts; they should remain uncommitted and are safe to delete when resetting your environment.

## Style Notes

### Content Standards

- Headings, link titles, and navigation labels must use **Chicago-style title case**, matching the main repository’s style requirement. When copying headings from other sources, normalize them before committing.
- Prefer Markdown over raw HTML; use MkDocs Material components (admonitions, tabs, tooltips) configured in `mkdocs.yml`. When HTML is unavoidable, keep it minimal and validate that `make watch` renders it correctly in dark/light themes.
- Update `mkdocs.yml` navigation whenever you add, rename, or move a page. If a URL changes, add a redirect entry to both `mkdocs.yml` and `mkdocs.deploy.yml` so legacy links stay valid.
- Store images next to the Markdown that references them (for example, `docs/user-guide/organize/img/`). Optimize screenshots before committing and include descriptive alt text in Markdown.
- Reuse canonical CLI flags, file paths, and configuration snippets from the main PhotoPrism repository. When documenting new application behavior, confirm the implementation in `photoprism/photoprism` before publishing.
- Front matter: use MkDocs `meta` blocks (or the `page.meta` keys referenced in `overrides/main.html`) when you need a custom page title or social caption. Avoid adding bespoke metadata keys unless templates consume them.

> **Title Case** rules (Chicago-style, with code- and path-aware normalization):
> - Capitalize the first word, the first word after a colon, dash, or end punctuation, and all major words, including the second part of a hyphenated major word.
> - Lowercase only articles, short conjunctions, and short prepositions of three letters or fewer when they are not in one of those positions.
> - Preserve known acronyms (for example, API, CLI, HTTP, JSON) and slash-separated acronym groups (for example, CSV/TSV) as uppercase.
> - Preserve inline code spans (`` `foo` ``), file paths (e.g. `docs/foo-bar.md`), and slash commands (e.g. `/grill-me`) verbatim; do not recase their contents.
> - Use `&` instead of `And`/`Or` in headings.

### Commit Messages

Use concise, imperative subjects with a one-word prefix indicating the scope or topic:

- `Config: Add tests for "darktable-cli" path detection`

If the commit relates to specific issues or pull requests, reference their IDs in the message:

- `Docker: Use two stage build to reduce image size #123 #5632`

Commit messages must not exceed 80 characters in length.

### GitHub Issues

Issue titles MUST be concise, use the imperative mood, and start with a single capitalized prefix followed by a colon and a space, e.g. `Search: Add filter for RAW image formats`.

Issue descriptions MUST begin with a one-sentence **User Story** where the sentence itself is fully bold in the format: `**As a <role>, I want <goal>, so that <outcome>.**`
Follow the User Story with a clear summary of the expected behavior, rationale, technical considerations, and constraints.

Descriptions MUST conclude with a checklist of **Acceptance Criteria**:
- Use GitHub checklist formatting: `- [ ]`
- Criteria MUST be clear, testable, and unambiguous.
- Each item MUST use one of the following priority keywords:
  - `MUST`   — required for the issue to be considered complete
  - `SHOULD` — strongly recommended but not strictly required
  - `MAY`    — optional enhancement

Additional details MAY be included as needed, such as related issues, references, screenshots, or external resources.

> Agents MUST create, edit, close, reopen, relabel, or otherwise modify GitHub issues only when explicitly requested by the user.

## Deployment & Publishing

- Working branch is `develop`. Merge `develop` into `deploy` (or run `make merge`) to trigger the GitHub Actions pipeline that rebuilds and uploads docs to docs.photoprism.app. Always resolve conflicts locally so deployment commits stay clean.
- `mkdocs deploy` is reserved for emergency GitHub Pages pushes; it writes to the `gh-pages` branch. Coordinate with maintainers before using it so automation does not overwrite manual changes.
- The built-in `privacy` plugin (part of Material for MkDocs, enabled in `mkdocs.deploy.yml`) mirrors external assets (badges, images) into the site. Keep `assets_exclude` up to date when new PhotoPrism-owned domains are introduced.
- Verify redirects, social previews, and structured data locally with `make build` before merging. Production uses the same config, so a clean local build is the release gate.

## Security & Access

- Never commit credentials. MkDocs Material Insiders is now public on PyPI, so we no longer ask contributors to add `GH_TOKEN` values to `.env`; keep that file untracked if you use it for other local overrides.
- Treat `docs/license`, `docs/icons/LICENSE`, and `docs/img/LICENSE` as authoritative for third-party assets. Confirm redistribution rights before adding new binaries or artwork.
- All social sharing and analytics scripts live in `overrides/main.html`. Review those tags when changing analytics providers to ensure we only load scripts from approved domains (`a.photoprism.app` for outbound tracking).
- Follow the main repository’s security and contribution policies (see `SECURITY.md` and `CONTRIBUTING.md` in photoprism/photoprism) when referencing vulnerabilities or non-public features in these docs.
