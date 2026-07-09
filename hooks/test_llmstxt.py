"""Unit tests for the llms.txt generation hook (pure functions only).

Run with:  python3 -m unittest hooks.test_llmstxt   (from repo root)
       or:  python3 -m unittest test_llmstxt          (from hooks/)

These tests exercise only the pure assembly/link-resolution helpers and do not
require MkDocs to be installed.
"""

import unittest

import llmstxt


SITE = "https://docs.photoprism.app/"
CURRENT = "user-guide/library/index.md"
URL_MAP = {
    "user-guide/library/index.md": "https://docs.photoprism.app/user-guide/library/",
    "developer-guide/media/index.md": "https://docs.photoprism.app/developer-guide/media/",
    "user-guide/library/img/desktop-search.jpg":
        "https://docs.photoprism.app/user-guide/library/img/desktop-search.jpg",
}


def r(md):
    return llmstxt.resolve_links(md, CURRENT, URL_MAP, SITE)


class ResolveLinksTest(unittest.TestCase):
    def test_external_link_unchanged(self):
        self.assertEqual(r("[x](https://example.com/a)"), "[x](https://example.com/a)")

    def test_mailto_unchanged(self):
        self.assertEqual(r("[mail](mailto:hi@photoprism.app)"),
                         "[mail](mailto:hi@photoprism.app)")

    def test_relative_md_up_a_dir(self):
        # From user-guide/library/index.md, reaching root-level developer-guide
        # needs ../../ (library -> user-guide -> root).
        self.assertEqual(
            r("[file formats](../../developer-guide/media/index.md)"),
            "[file formats](https://docs.photoprism.app/developer-guide/media/)",
        )

    def test_relative_md_with_anchor(self):
        self.assertEqual(
            r("[exif](../../developer-guide/media/index.md#exif)"),
            "[exif](https://docs.photoprism.app/developer-guide/media/#exif)",
        )

    def test_same_page_anchor(self):
        self.assertEqual(
            r("[top](#intro)"),
            "[top](https://docs.photoprism.app/user-guide/library/#intro)",
        )

    def test_unresolvable_link_becomes_plain_text(self):
        self.assertEqual(r("see [here](../nope/missing.md) now"), "see here now")

    def test_image_resolved_and_attr_stripped(self):
        self.assertEqual(
            r('![Screenshot](img/desktop-search.jpg){ class="shadow" }'),
            "![Screenshot](https://docs.photoprism.app/user-guide/library/img/desktop-search.jpg)",
        )

    def test_unresolvable_image_with_alt_placeholder(self):
        self.assertEqual(r("![Diagram](img/missing.png)"), "[image: Diagram]")

    def test_unresolvable_image_no_alt_placeholder(self):
        self.assertEqual(r("![](img/missing.png)"), "[image]")

    def test_external_image_attr_stripped(self):
        self.assertEqual(r("![x](https://ex.com/a.png){ .cls }"), "![x](https://ex.com/a.png)")

    def test_absolute_rooted_link_unchanged(self):
        self.assertEqual(r("[x](/already/rooted/)"), "[x](/already/rooted/)")

    def test_plain_text_untouched(self):
        self.assertEqual(r("no links here, just prose."), "no links here, just prose.")

    def test_linked_image_both_resolved(self):
        # [![alt](img)](page.md) -> both image and link target resolved
        md = ("[![Search](img/desktop-search.jpg)]"
              "(../../developer-guide/media/index.md)")
        self.assertEqual(
            r(md),
            "[![Search](https://docs.photoprism.app/user-guide/library/img/desktop-search.jpg)]"
            "(https://docs.photoprism.app/developer-guide/media/)",
        )

    def test_linked_image_unresolvable_link_keeps_image(self):
        md = "[![Search](img/desktop-search.jpg)](../nope/missing.md)"
        self.assertEqual(
            r(md),
            "![Search](https://docs.photoprism.app/user-guide/library/img/desktop-search.jpg)",
        )

    def test_linked_image_external_link_unchanged(self):
        md = "[![Search](img/desktop-search.jpg)](https://example.com/)"
        self.assertEqual(
            r(md),
            "[![Search](https://docs.photoprism.app/user-guide/library/img/desktop-search.jpg)]"
            "(https://example.com/)",
        )

    def test_link_text_with_nested_brackets(self):
        md = "[set with `passwd [username]`](../../developer-guide/media/index.md)"
        self.assertEqual(
            r(md),
            "[set with `passwd [username]`](https://docs.photoprism.app/developer-guide/media/)",
        )


class StripHtmlCommentsTest(unittest.TestCase):
    def test_inline_comment_removed(self):
        out = llmstxt.strip_html_comments("before <!-- hidden --> after")
        self.assertNotIn("hidden", out)
        self.assertIn("before", out)
        self.assertIn("after", out)

    def test_multiline_comment_removed(self):
        md = "Intro para.\n\n<!--\n### Hidden Section\n\nsecret body\n-->\n\nNext para."
        out = llmstxt.strip_html_comments(md)
        self.assertNotIn("Hidden Section", out)
        self.assertNotIn("secret body", out)
        self.assertIn("Intro para.", out)
        self.assertIn("Next para.", out)

    def test_commented_out_image_removed(self):
        out = llmstxt.strip_html_comments("<!--![Screenshot](img/confirm-archive.jpg)-->")
        self.assertEqual(out.strip(), "")

    def test_blank_line_runs_collapsed(self):
        md = "a\n\n<!-- x -->\n\nb"
        out = llmstxt.strip_html_comments(md)
        self.assertNotIn("\n\n\n", out)
        self.assertIn("a", out)
        self.assertIn("b", out)

    def test_no_comment_unchanged(self):
        md = "Just some **prose** with a [link](https://x.example/)."
        self.assertEqual(llmstxt.strip_html_comments(md), md)


class RenderIndexTest(unittest.TestCase):
    def test_sections_headings_and_nesting(self):
        header = "# H\n\n> desc"
        sections = [
            ("Getting Started", [
                (0, "Setup", "https://docs.photoprism.app/getting-started/"),
                (0, "Config Files", None),
                (1, "options.yml", "https://docs.photoprism.app/getting-started/config-files/"),
            ]),
        ]
        out = llmstxt.render_index(header, sections)
        self.assertTrue(out.startswith("# H\n\n> desc"))
        self.assertIn("## Getting Started", out)
        self.assertIn("- [Setup](https://docs.photoprism.app/getting-started/)", out)
        # section without url renders as a plain (unlinked) label
        self.assertIn("- Config Files", out)
        # nested page is indented two spaces
        self.assertIn("  - [options.yml](https://docs.photoprism.app/getting-started/config-files/)", out)
        self.assertTrue(out.endswith("\n"))


class RenderFullTest(unittest.TestCase):
    def test_page_block_layout(self):
        header = "# H"
        pages = [("Setup", "https://docs.photoprism.app/getting-started/", "Body text here.")]
        out = llmstxt.render_full(header, pages)
        self.assertIn("# Setup", out)
        self.assertIn("Source: https://docs.photoprism.app/getting-started/", out)
        self.assertIn("Body text here.", out)
        self.assertIn("\n---\n", out)


class HeaderTest(unittest.TestCase):
    def test_pointer_included_when_requested(self):
        h = llmstxt.build_header(SITE, include_pointer=True)
        self.assertIn("# PhotoPrism Documentation", h)
        self.assertIn("> ", h)
        self.assertIn("https://docs.photoprism.app/llms-full.txt", h)

    def test_pointer_omitted_when_not_requested(self):
        h = llmstxt.build_header(SITE, include_pointer=False)
        self.assertNotIn("llms-full.txt", h)


if __name__ == "__main__":
    unittest.main()
