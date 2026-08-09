#!/usr/bin/env node
// Link and asset checker for the built site in site/.
//
// Two independent passes:
//
//   Internal (default) - resolves every site-relative src/href/poster/data-src/
//   srcset target against the files in site/. Deterministic, needs no network,
//   and exits non-zero on a miss, so it is safe to rely on as a gate.
//
//   External (--external) - probes off-site URLs. Report-only: it never changes
//   the exit status, because a third-party host being slow, rate-limiting us, or
//   returning an odd status for a deep link is not our build breaking.
//
// Why the external pass is deliberately careful:
//
//   An HTTP status code is not a verdict. Single-page apps routinely answer a
//   deep link with a 404 status while serving a complete, working page that
//   their client-side router then handles - a real visitor sees the right thing.
//   So this script follows redirects MANUALLY, attributes each status to the hop
//   that actually returned it (never to the original URL), and reads the body
//   before calling anything broken. A 4xx carrying a full HTML document is
//   reported as SOFT, not BROKEN.
//
//   github.com is skipped unless --include-github is passed: it rate-limits
//   unauthenticated probes hard enough to manufacture false failures, and the
//   docs link to it heavily.
//
//   Sibling copies live in photoprism-docs-de, photoprism-web and photoprism-blog. All four are kept
//   byte-identical apart from this header and the default build directory, so a fix
//   can be copied across; the repos share no build infrastructure.
//
// Usage:
//   node scripts/check-links.js                    internal only (default)
//   node scripts/check-links.js --external         internal + external probe
//   node scripts/check-links.js --external --include-github
//   node scripts/check-links.js --root site        override the build directory
//
// stdlib only - run after the site has been built into site/ (see the Makefile).

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");

const args = process.argv.slice(2);
const OPT = {
  external: args.includes("--external"),
  includeGithub: args.includes("--include-github"),
  root: path.resolve(process.cwd(), valueOf("--root") || "site"),
};

function valueOf(flag) {
  const i = args.indexOf(flag);
  return i === -1 ? null : args[i + 1];
}

// Attribute values that are never navigable resources.
const SKIP_PREFIX = ["mailto:", "tel:", "data:", "javascript:", "#", "blob:", "sms:"];

// Hosts that appear in documentation as placeholders or point at the reader's
// own machine. Probing them is meaningless - they are not expected to resolve
// from a build host. Covers the RFC 2606 reserved names plus loopback.
const SKIP_HOST_RE = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\]|.*\.(example|invalid|test|local|localhost))$/i;
const SKIP_HOST_EXACT = new Set(["example.com", "example.org", "example.net"]);

function isPlaceholderHost(host) {
  const bare = host.replace(/:\d+$/, "").toLowerCase();
  return SKIP_HOST_EXACT.has(bare) || SKIP_HOST_RE.test(bare);
}

// Production output is minified, so unquoted attribute values are the common
// case. A quoted-only pattern silently matches almost nothing.
const ATTR_RE = /\s(?:src|href|poster|data-src)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi;
const SRCSET_RE = /\ssrcset\s*=\s*(?:"([^"]*)"|'([^']*)')/gi;

// Concurrency for the external pass. Small on purpose: politeness beats speed.
const EXTERNAL_CONCURRENCY = 8;
const EXTERNAL_TIMEOUT_MS = 20000;
const MAX_REDIRECTS = 10;
// A 4xx/5xx body at least this long, containing markup, is treated as a page
// that renders rather than a dead link.
const SOFT_BODY_MIN = 500;
// How much of a non-2xx body to read when looking for the title.
const BODY_READ_MAX = 65536;
// ...unless it looks like the site's own error page. A custom 404 page renders
// perfectly well and would otherwise be excused as a working SPA deep link, so
// the title is checked for the usual error wording before granting SOFT.
const ERROR_TITLE_RE = /\b(4 ?0 ?4|not found|page unavailable|page not available|does ?n[o']?t exist|error)\b/i;

// walk returns every file under dir matching the predicate.
function walk(dir, match, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, match, out);
    } else if (match(entry.name)) {
      out.push(full);
    }
  }
  return out;
}

// pageUrl maps a built file to the URL path it is served at.
function pageUrl(file) {
  const rel = path.relative(OPT.root, file).split(path.sep).join("/");
  if (rel === "index.html") return "/";
  if (rel.endsWith("/index.html")) return "/" + rel.slice(0, -"index.html".length);
  return "/" + rel;
}

// decodeEntities expands the entities that appear inside URLs, including numeric
// character references. Themes obfuscate mailto: addresses as pure numeric entities
// (MkDocs Material does); without decoding them the href reads as a relative link and
// is reported as a broken internal target.
function decodeEntities(s) {
  return s
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10)))
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

// refsIn extracts every resource reference from one HTML document. Commented-out
// markup is skipped: an image parked inside <!-- --> is not requested by a browser
// and must not be reported as missing.
function refsIn(rawHtml) {
  const html = rawHtml.replace(/<!--[\s\S]*?-->/g, "");
  const found = [];
  for (const m of html.matchAll(ATTR_RE)) {
    found.push(m[1] ?? m[2] ?? m[3] ?? "");
  }
  for (const m of html.matchAll(SRCSET_RE)) {
    for (const part of (m[1] ?? m[2] ?? "").split(",")) {
      const candidate = part.trim().split(/\s+/)[0];
      if (candidate) found.push(candidate);
    }
  }
  return found.map((r) => decodeEntities(r).trim()).filter(Boolean);
}

// resolvesLocally reports whether a site-absolute path maps to a built file.
function resolvesLocally(urlPath) {
  const rel = decodeURIComponent(urlPath).replace(/^\/+/, "");
  const candidate = path.join(OPT.root, rel);
  if (safeIsFile(candidate)) return true;
  if (safeIsFile(path.join(candidate, "index.html"))) return true;
  if (safeIsFile(candidate.replace(/\/+$/, "") + ".html")) return true;
  return false;
}

function safeIsFile(p) {
  try {
    return fs.statSync(p).isFile();
  } catch {
    return false;
  }
}

// collect walks the build output once and returns the internal misses plus the
// distinct external URLs, each mapped to the pages referencing it.
function collect() {
  const pages = walk(OPT.root, (n) => n.endsWith(".html"));
  const broken = new Map();
  const external = new Map();
  let checked = 0;

  for (const file of pages) {
    const base = pageUrl(file);
    const html = fs.readFileSync(file, "utf8");

    for (const raw of refsIn(html)) {
      const lower = raw.toLowerCase();
      if (SKIP_PREFIX.some((p) => lower.startsWith(p))) continue;

      let url;
      try {
        url = new URL(raw, "https://example.invalid" + base);
      } catch {
        continue;
      }

      if (/^https?:$/.test(url.protocol) && url.host !== "example.invalid") {
        if (isPlaceholderHost(url.host)) continue;
        const key = url.origin + url.pathname + url.search;
        if (!external.has(key)) external.set(key, new Set());
        external.get(key).add(base);
        continue;
      }
      if (url.host !== "example.invalid") continue; // non-http scheme we don't check

      checked++;
      if (!resolvesLocally(url.pathname)) {
        if (!broken.has(url.pathname)) broken.set(url.pathname, new Set());
        broken.get(url.pathname).add(base);
      }
    }
  }

  return { pages: pages.length, checked, broken, external };
}

// probe follows redirects by hand so each status is attributed to the hop that
// returned it, and reads the body so a rendering page is not called broken.
//
// It carries cookies across hops. Some sites (microsoft.com is the live example)
// bounce a cookie-less client between two cache-busting URLs forever, which looks
// exactly like a redirect loop but resolves in two hops for any real browser.
async function probe(startUrl) {
  const hops = [];
  const jar = new Map();
  const seen = new Set();
  let url = startUrl;

  for (let i = 0; i <= MAX_REDIRECTS; i++) {
    let res;
    try {
      const headers = {
        "User-Agent": "Mozilla/5.0 (compatible; photoprism-linkcheck/1.0)",
        Accept: "text/html,application/xhtml+xml,image/*;q=0.8,*/*;q=0.5",
      };
      if (jar.size) {
        headers.Cookie = [...jar].map(([k, v]) => `${k}=${v}`).join("; ");
      }
      res = await fetch(url, {
        redirect: "manual",
        signal: AbortSignal.timeout(EXTERNAL_TIMEOUT_MS),
        headers,
      });
      // Keep it simple: name=value only, no domain/path scoping. Enough to get
      // past the "set a cookie then redirect" pattern without a cookie library.
      for (const raw of res.headers.getSetCookie?.() ?? []) {
        const [pair] = raw.split(";");
        const eq = pair.indexOf("=");
        if (eq > 0) jar.set(pair.slice(0, eq).trim(), pair.slice(eq + 1).trim());
      }
    } catch (err) {
      const why =
        err.name === "TimeoutError"
          ? `timeout after ${EXTERNAL_TIMEOUT_MS} ms`
          : err.cause?.code || err.message || err.name || "request failed";
      hops.push({ url, status: 0, note: why });
      return { hops, verdict: "UNREACHABLE", reason: why };
    }

    hops.push({ url, status: res.status });

    if (res.status >= 300 && res.status < 400) {
      const loc = res.headers.get("location");
      if (!loc) return { hops, verdict: "BROKEN", reason: `${res.status} without a Location header` };
      try {
        url = new URL(loc, url).toString();
      } catch {
        return { hops, verdict: "BROKEN", reason: `unparseable redirect target: ${loc}` };
      }
      // A URL we have already requested means the chain is cycling. Report it,
      // but only as advisory: sites that alternate between cache-busting URLs
      // (microsoft.com does) settle immediately in a real browser, and we cannot
      // tell that apart from a genuinely stuck redirect.
      if (seen.has(url)) {
        return { hops, verdict: "SOFT", reason: "redirect loop - alternates between URLs; browsers typically settle on one" };
      }
      seen.add(url);
      continue;
    }

    if (res.status >= 200 && res.status < 300) return { hops, verdict: "OK" };

    // Non-2xx terminal status. Read the body before judging it. The cap has to be
    // generous: GitHub's <head> alone runs well past a few KB, and truncating before
    // the <title> made its "File not found" page look like a working SPA deep link.
    let body = "";
    try {
      body = (await res.text()).slice(0, BODY_READ_MAX);
    } catch {
      /* treat an unreadable body as empty */
    }
    const rendersAPage = body.length >= SOFT_BODY_MIN && /<html[\s>]/i.test(body);
    const title = pageTitle(body);
    if (rendersAPage && ERROR_TITLE_RE.test(title)) {
      return { hops, verdict: "BROKEN", reason: `status ${res.status}, error page: "${title}"` };
    }
    if (rendersAPage) {
      return { hops, verdict: "SOFT", reason: `status ${res.status} but serves a page${title ? `: "${title}"` : ""}` };
    }
    return { hops, verdict: "BROKEN", reason: `status ${res.status}, no page body` };
  }

  return { hops, verdict: "SOFT", reason: `more than ${MAX_REDIRECTS} redirects without settling` };
}

// pageTitle returns the document title, preferring the one inside <head>. Inline
// SVGs carry their own <title> element (Traefik's docs open with a logo), so simply
// taking the first match can report the logo's label as the page title.
function pageTitle(body) {
  const head = body.split(/<\/head>/i)[0];
  const from = (s) => ((s.match(/<title[^>]*>([^<]*)<\/title>/i) || [])[1] || "").trim();
  return from(head) || from(body);
}

// runPool executes tasks with a bounded number in flight.
async function runPool(items, limit, worker) {
  const results = [];
  let next = 0;
  const runners = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (next < items.length) {
      const i = next++;
      results[i] = await worker(items[i], i);
    }
  });
  await Promise.all(runners);
  return results;
}

function describeHops(hops) {
  return hops.map((h) => `${h.status || h.note} ${h.url}`).join("\n        -> ");
}

async function main() {
  if (!safeIsFile(path.join(OPT.root, "index.html"))) {
    console.error(`No build found at ${path.relative(ROOT, OPT.root)}/ - run "make build" first.`);
    process.exit(2);
  }

  const { pages, checked, broken, external } = collect();

  console.log(`Scanned ${pages} pages in ${path.relative(ROOT, OPT.root)}/`);
  console.log(`Internal references checked: ${checked}`);

  if (broken.size === 0) {
    console.log("Internal: OK - every reference resolves.\n");
  } else {
    console.log(`Internal: ${broken.size} target(s) do not resolve:\n`);
    for (const [target, pagesUsing] of [...broken].sort()) {
      const list = [...pagesUsing].sort();
      const shown = list.slice(0, 4).join(", ") + (list.length > 4 ? ` (+${list.length - 4} more)` : "");
      console.log(`  ${target}\n      on: ${shown}`);
    }
    console.log("");
  }

  if (OPT.external) {
    let urls = [...external.keys()];
    const skipped = OPT.includeGithub ? [] : urls.filter((u) => new URL(u).host.endsWith("github.com"));
    if (!OPT.includeGithub) urls = urls.filter((u) => !new URL(u).host.endsWith("github.com"));

    console.log(`External URLs: ${urls.length} to probe` + (skipped.length ? `, ${skipped.length} github.com skipped (use --include-github)` : ""));

    const results = await runPool(urls, EXTERNAL_CONCURRENCY, async (u) => ({ url: u, ...(await probe(u)) }));

    const bad = results.filter((r) => r.verdict === "BROKEN");
    const soft = results.filter((r) => r.verdict === "SOFT");
    const unreachable = results.filter((r) => r.verdict === "UNREACHABLE");

    for (const [label, group] of [["BROKEN", bad], ["UNREACHABLE", unreachable], ["SOFT", soft]]) {
      if (!group.length) continue;
      console.log(`\n${label}: ${group.length}`);
      for (const r of group.sort((a, b) => a.url.localeCompare(b.url))) {
        const pagesUsing = [...(external.get(r.url) || [])].sort();
        const shown = pagesUsing.slice(0, 3).join(", ") + (pagesUsing.length > 3 ? ` (+${pagesUsing.length - 3} more)` : "");
        console.log(`  ${r.url}`);
        console.log(`      ${r.reason}`);
        console.log(`      chain: ${describeHops(r.hops)}`);
        console.log(`      on: ${shown}`);
      }
    }

    console.log(
      `\nExternal summary: ${results.length - bad.length - soft.length - unreachable.length} ok, ` +
        `${bad.length} broken, ${unreachable.length} unreachable, ${soft.length} soft (renders despite the status).`
    );
    console.log("External findings are advisory and do not affect the exit status.");
  }

  process.exit(broken.size === 0 ? 0 : 1);
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
