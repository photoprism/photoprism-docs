"""MkDocs build hook that generates /llms.txt and /llms-full.txt.

See ../LLMS.md for the rationale, scope, and how to adjust generation.

- llms.txt      : curated, machine-readable index of the whole documentation
                  site (all top-level nav sections), one link per page.
- llms-full.txt : full-text Markdown dump of the User Guide and Getting Started
                  sections, with internal .md links and image references
                  rewritten to absolute public URLs.

The hook reads raw source Markdown (no HTML round-trip) and adds no third-party
dependencies. It is wired via `hooks:` in mkdocs.deploy.yml so it runs on the
production build (`make build` / CI gh-deploy) but not on `mkdocs serve`.

See https://llmstxt.org/ for the llms.txt convention.
"""

import logging
import posixpath
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.llmstxt")

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Top-level nav sections (by title) whose pages are dumped in full into
# llms-full.txt. The index (llms.txt) always covers every section.
FULL_TEXT_SECTIONS = ("Getting Started", "User Guide")

TITLE = "PhotoPrism Documentation"

DESCRIPTION = (
    "Official documentation for PhotoPrism: setup guides, the user guide, "
    "developer reference, and release notes for the privacy-focused, "
    "self-hosted AI photo and video app."
)

INTRO = (
    "PhotoPrism® is a privacy-focused, self-hosted AI photo and video app "
    "for browsing, organizing, and sharing media libraries. This is the "
    "official documentation site, covering installation and setup (Docker, "
    "NAS, Raspberry Pi, and cloud), the user guide for organizing and "
    "searching your library, a developer reference (APIs, build, and "
    "contribution guides), and release notes. For product information, "
    "editions, pricing, and support articles, see the main website at "
    "https://www.photoprism.app/."
)

# --------------------------------------------------------------------------- #
# Link resolution
# --------------------------------------------------------------------------- #

# A single target: `path "opt title"` — captures the target, ignores any title.
_TARGET = r'\s*([^)\s]+?)\s*(?:"[^"]*")?'
_ATTR = r'([ \t]*\{[^}]*\})?'  # trailing attr-list, e.g. { class="shadow" }
# Link text may contain one level of nested brackets (e.g. `foo [bar] baz`).
_TEXT = r'((?:[^\[\]]|\[[^\]]*\])+?)'

# Linked image:  [![alt](img)](link){ attr }  -- must be handled before the
# standalone image/link patterns, which cannot parse the nesting.
_LINKED_IMG_RE = re.compile(
    r'\[!\[([^\]]*)\]\(' + _TARGET + r'\)' + _ATTR + r'\]\(' + _TARGET + r'\)' + _ATTR
)
# ![alt](target "opt title"){ attr-list }
_IMG_RE = re.compile(r'!\[([^\]]*)\]\(' + _TARGET + r'\)' + _ATTR)
# [text](target "opt title"){ attr-list }  -- not preceded by '!'
_LINK_RE = re.compile(r'(?<!!)\[' + _TEXT + r'\]\(' + _TARGET + r'\)' + _ATTR)
# scheme: (http:, https:, mailto:, tel:, data:, ...)
_SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.\-]*:')

# HTML comment (possibly spanning multiple lines).
_HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)
# Three or more newlines (with optional intervening blank whitespace).
_BLANK_RUN_RE = re.compile(r'\n[ \t]*\n[ \t]*\n+')


def strip_html_comments(markdown):
    """Remove HTML comments (`<!-- ... -->`) from Markdown.

    These are hidden on the rendered site, so they should not appear in the
    full-text dump either. Blank-line runs left behind by a removed block are
    collapsed so the surrounding text stays tidy.
    """
    out = _HTML_COMMENT_RE.sub("", markdown)
    return _BLANK_RUN_RE.sub("\n\n", out)


def _abs_url(site_url, url):
    """Join a site_url with a root-relative MkDocs File.url into an absolute URL."""
    base = site_url.rstrip("/")
    if url in ("", ".", "./"):
        return base + "/"
    return base + "/" + url.lstrip("/")


def _resolve_target(target, current_src_uri, url_map, site_url):
    """Resolve a link/image target.

    Returns a (status, value) tuple:
      ("keep", target)  -> leave the target unchanged (external / rooted)
      ("url", abs_url)   -> resolved absolute URL
      ("notfound", target) -> relative target not found in the site
    """
    # External or protocol-relative or already-rooted targets: leave untouched.
    if _SCHEME_RE.match(target) or target.startswith("//") or target.startswith("/"):
        return ("keep", target)

    # Same-page anchor.
    if target.startswith("#"):
        base = url_map.get(current_src_uri)
        if base:
            return ("url", base + target)
        return ("keep", target)

    path, _, frag = target.partition("#")
    if path == "":
        return ("keep", target)

    norm = posixpath.normpath(posixpath.join(posixpath.dirname(current_src_uri), path))
    url = url_map.get(norm)
    if url:
        return ("url", url + ("#" + frag if frag else ""))
    return ("notfound", target)


def resolve_links(markdown, current_src_uri, url_map, site_url):
    """Rewrite relative Markdown links and images to absolute public URLs.

    Trailing attr-list blocks (`{ ... }`) on links/images are stripped. Links
    that cannot be resolved fall back to their plain text; images that cannot be
    resolved fall back to a `[image: <alt>]` (or `[image]`) placeholder.
    """
    def _image_md(alt, target):
        """Render an image, or a plain-text fallback when it can't resolve."""
        status, value = _resolve_target(target, current_src_uri, url_map, site_url)
        if status == "notfound":
            log.debug("llmstxt: unresolved image %r in %s", target, current_src_uri)
            return None  # caller decides on placeholder / link text
        return "![%s](%s)" % (alt, value)

    def linked_img_cb(m):
        alt, img_target, link_target = m.group(1), m.group(2), m.group(4)
        inner = _image_md(alt, img_target)
        if inner is None:
            inner = alt if alt.strip() else "image"
        status, value = _resolve_target(link_target, current_src_uri, url_map, site_url)
        if status == "notfound":
            log.debug("llmstxt: unresolved link %r in %s", link_target, current_src_uri)
            return inner
        return "[%s](%s)" % (inner, value)

    def img_cb(m):
        alt = m.group(1)
        inner = _image_md(alt, m.group(2))
        if inner is None:
            return "[image: %s]" % alt if alt.strip() else "[image]"
        return inner

    def link_cb(m):
        text, target = m.group(1), m.group(2)
        status, value = _resolve_target(target, current_src_uri, url_map, site_url)
        if status == "notfound":
            log.debug("llmstxt: unresolved link %r in %s", target, current_src_uri)
            return text
        return "[%s](%s)" % (text, value)

    markdown = _LINKED_IMG_RE.sub(linked_img_cb, markdown)
    markdown = _IMG_RE.sub(img_cb, markdown)
    markdown = _LINK_RE.sub(link_cb, markdown)
    return markdown


# --------------------------------------------------------------------------- #
# Rendering (pure)
# --------------------------------------------------------------------------- #

def build_header(site_url, include_pointer):
    lines = ["# " + TITLE, "", "> " + DESCRIPTION, "", INTRO]
    if include_pointer:
        lines += [
            "",
            "A plain-text dump of the User Guide and Getting Started sections is "
            "available at %sllms-full.txt." % site_url,
        ]
    return "\n".join(lines)


def render_index(header, sections):
    """Render llms.txt from an ordered list of (heading, entries).

    entries: ordered list of (depth, title, url_or_None). A None url renders as
    an unlinked label (used for grouping sub-sections).
    """
    parts = [header, ""]
    for heading, entries in sections:
        parts.append("## " + heading)
        parts.append("")
        for depth, title, url in entries:
            indent = "  " * depth
            if url:
                parts.append("%s- [%s](%s)" % (indent, title, url))
            else:
                parts.append("%s- %s" % (indent, title))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def render_full(header, pages):
    """Render llms-full.txt from an ordered list of (title, url, markdown)."""
    parts = [header, ""]
    for title, url, md in pages:
        parts.append("# " + title)
        parts.append("")
        parts.append("Source: " + url)
        parts.append("")
        parts.append(md.strip())
        parts.append("")
        parts.append("---")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# MkDocs event hooks (glue)
# --------------------------------------------------------------------------- #

_state = {"url_map": {}, "raw": {}, "nav": None}


def on_files(files, config, **kwargs):
    """Build the site-wide src_uri -> absolute_url map (pages + static assets)."""
    site_url = config.get("site_url") or ""
    url_map = {}
    for f in files:
        url_map[f.src_uri] = _abs_url(site_url, f.url)
    _state["url_map"] = url_map
    return files


def on_nav(nav, config, **kwargs):
    _state["nav"] = nav
    return nav


def on_page_markdown(markdown, page, **kwargs):
    _state["raw"][page.file.src_uri] = markdown
    return markdown


def _page_url(page, site_url):
    return page.canonical_url or _abs_url(site_url, page.file.url)


def _walk(items, depth, site_url):
    out = []
    for item in items:
        if getattr(item, "is_section", False):
            out.append((depth, item.title, None))
            out.extend(_walk(item.children, depth + 1, site_url))
        elif getattr(item, "is_page", False):
            title = item.title or item.file.src_uri
            out.append((depth, title, _page_url(item, site_url)))
        elif getattr(item, "is_link", False):
            out.append((depth, item.title, item.url))
    return out


def _collect_pages(items):
    pages = []
    for item in items:
        if getattr(item, "is_section", False):
            pages.extend(_collect_pages(item.children))
        elif getattr(item, "is_page", False):
            pages.append(item)
    return pages


def on_post_build(config, **kwargs):
    nav = _state["nav"]
    if nav is None:
        log.warning("llmstxt: no nav captured; skipping llms.txt generation")
        return

    site_url = config.get("site_url") or ""
    url_map = _state["url_map"]
    raw = _state["raw"]

    # Index: every top-level section.
    index_sections = []
    for item in nav.items:
        if getattr(item, "is_section", False):
            index_sections.append((item.title, _walk(item.children, 0, site_url)))
        elif getattr(item, "is_page", False):
            title = item.title or item.file.src_uri
            index_sections.append((title, [(0, title, _page_url(item, site_url))]))

    index_txt = render_index(build_header(site_url, include_pointer=True), index_sections)

    # Full dump: only the configured sections.
    full_pages = []
    for item in nav.items:
        if getattr(item, "is_section", False) and item.title in FULL_TEXT_SECTIONS:
            for page in _collect_pages(item.children):
                md = strip_html_comments(raw.get(page.file.src_uri, ""))
                resolved = resolve_links(md, page.file.src_uri, url_map, site_url)
                title = page.title or page.file.src_uri
                full_pages.append((title, _page_url(page, site_url), resolved))

    full_txt = render_full(build_header(site_url, include_pointer=False), full_pages)

    site_dir = Path(config["site_dir"])
    (site_dir / "llms.txt").write_text(index_txt, encoding="utf-8")
    (site_dir / "llms-full.txt").write_text(full_txt, encoding="utf-8")
    log.info(
        "llmstxt: wrote llms.txt (%d sections) and llms-full.txt (%d pages)",
        len(index_sections), len(full_pages),
    )
