# Security Testing Guide

This guide provides a practical security testing baseline for PhotoPrism web, API, and deployment changes. It is based on the [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) and should be used together with code review, automated tests, dependency scanning, and manual verification.

PhotoPrism-specific focus areas include authentication, sessions, media upload and import workflows, metadata extraction, thumbnail/video processing, sharing, search, albums, WebDAV, user roles, configuration, and containerized deployments behind reverse proxies.

## Goals

Use this guide to:

- Verify that new features do not weaken authentication, authorization, session handling, or privacy boundaries.
- Test risky workflows such as upload, import, indexing, sharing, WebDAV, and administrative configuration changes.
- Keep regression tests aligned with common OWASP WSTG categories without copying the complete upstream guide into our documentation.
- Provide reviewers and contributors with a concise checklist that fits PhotoPrism's architecture.

## Scope

Test the following entry points when they are affected by a change:

- Web UI routes and frontend state transitions.
- JSON API endpoints used by the web app, CLI, mobile clients, integrations, and reverse proxies.
- Authentication, login, logout, password changes, session cookies, access tokens, and optional identity-provider integrations.
- Public links, shared albums, download endpoints, thumbnails, previews, originals, sidecar files, and WebDAV resources.
- Upload, import, indexing, library scanning, metadata extraction, file conversion, video transcoding, and background workers.
- Admin settings, user management, account provisioning, storage settings, and feature flags.
- Docker, Compose, reverse proxy, TLS, CORS, CSP, cache, and header configuration.
- Database-backed behavior on SQLite, MariaDB, and compatible environments.

## Testing Environments

Use at least one local development environment and, before release, a production-like deployment with TLS and a reverse proxy.

Recommended local setup:

```bash
git clone https://github.com/photoprism/photoprism.git
cd photoprism
make docker-dev
```

Recommended production-like coverage:

- Run behind Traefik, Caddy, Nginx, Apache, or another supported reverse proxy.
- Enable HTTPS and verify forwarded headers, cookie security flags, canonical host handling, and redirect behavior.
- Test with a non-admin user, an admin user, a public visitor, and an expired or invalid session.
- Test with realistic media files, including images, videos, sidecar files, uncommon extensions, malformed metadata, large files, and duplicate names.

## Tooling

Automated tools do not replace manual testing, but they help catch regressions and misconfiguration.

### Nuclei

[Nuclei](https://github.com/projectdiscovery/nuclei) is a fast template-based vulnerability scanner.

Install on macOS:

```bash
brew install nuclei
```

Update templates:

```bash
nuclei -update
nuclei -ut
```

Run against a local instance:

```bash
nuclei -u http://localhost:2342 \
  -severity low,medium,high,critical \
  -exclude-tags intrusive,dos
```

Run against a production-like HTTPS deployment:

```bash
nuclei -u https://photos.example.com \
  -severity low,medium,high,critical \
  -exclude-tags intrusive,dos \
  -H 'User-Agent: PhotoPrism-Security-Test'
```

Do not run intrusive, destructive, brute-force, or denial-of-service templates against shared infrastructure without explicit approval.

### Additional Tools

Consider these tools depending on the change:

- Browser DevTools for cookies, storage, CORS, CSP, mixed content, redirects, and cache behavior.
- OWASP ZAP for authenticated crawling and passive scanning.
- `curl`, `httpie`, or Postman for API and header verification.
- `go test`, frontend tests, and targeted regression tests for server-side validation and access control.
- Dependency scanners such as Dependabot, GitHub code scanning, Trivy, or Grype.
- Fuzzing or malformed-file corpora for upload, import, parser, metadata, and media-processing changes.

## Baseline Checklist

Use the status markers `[ ]`, `[x]`, `[n/a]`, and `[risk accepted]` when copying sections into pull requests or release checklists.

### 1. Information Gathering

- [ ] Enumerate changed routes, API endpoints, query parameters, request bodies, and response fields.
- [ ] Identify affected user roles: public visitor, viewer, user, admin, service account, and anonymous shared-link visitor.
- [ ] Identify sensitive data touched by the change: originals, thumbnails, EXIF/GPS metadata, face data, labels, albums, private paths, account data, tokens, and configuration values.
- [ ] Check generated frontend bundles and API responses for leaked secrets, internal paths, stack traces, build metadata, debug flags, or private configuration.
- [ ] Review `robots.txt`, `sitemap.xml`, public asset paths, media URLs, and share URLs for unintended exposure.
- [ ] Confirm that documentation, examples, screenshots, and fixtures do not expose real credentials, private photos, access tokens, or hostnames.

### 2. Configuration and Deployment Management

- [ ] Verify secure defaults for new configuration options, environment variables, Compose examples, and Helm or reverse-proxy snippets.
- [ ] Confirm that admin-only settings cannot be changed by lower-privileged users or unauthenticated requests.
- [ ] Test behavior behind reverse proxies, including `X-Forwarded-*`, canonical host, scheme detection, secure cookies, and redirect targets.
- [ ] Verify security headers where applicable: `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options` or `frame-ancestors`, `Permissions-Policy`, and HSTS for HTTPS deployments.
- [ ] Ensure unsupported HTTP methods are rejected and method overrides cannot bypass routing or authorization.
- [ ] Check that development, debug, profiling, migration, and diagnostic endpoints are not exposed in production builds.
- [ ] Confirm old, backup, temporary, cache, sidecar, and generated files are not reachable unless intentionally served.

### 3. Identity Management

- [ ] Verify role definitions and permissions for any changed feature.
- [ ] Test account creation, provisioning, disabling, deletion, and role changes if touched by the change.
- [ ] Confirm that username, email, and display-name handling does not enable impersonation, spoofing, stored XSS, or confusing account collisions.
- [ ] Ensure user enumeration is not introduced through login, reset, invite, WebDAV, API, search, sharing, or error responses.
- [ ] Verify that external identity-provider or reverse-proxy authentication integrations cannot silently map users to the wrong account.

### 4. Authentication

- [ ] Confirm credentials are only submitted over HTTPS in production-like deployments.
- [ ] Test valid, invalid, missing, expired, disabled, and malformed credentials.
- [ ] Verify default credentials are documented only where needed and are rejected or forced to change where appropriate.
- [ ] Test rate limiting, lockout, throttling, and logging for repeated login failures.
- [ ] Confirm password change and reset workflows invalidate relevant sessions or tokens as intended.
- [ ] Check remember-me, API-token, app-password, WebDAV, and CLI authentication behavior if affected.
- [ ] Verify browser cache behavior around authenticated pages and sensitive API responses.

### 5. Authorization and Object-Level Access Control

- [ ] Test direct access to photos, videos, albums, people, labels, moments, places, originals, thumbnails, downloads, sidecar files, and WebDAV paths owned by another user or outside the current permission scope.
- [ ] Test vertical access control: non-admin users must not access admin settings, user management, indexing controls, import paths, diagnostics, logs, or maintenance actions.
- [ ] Test horizontal access control between users, shared albums, public links, private albums, archived items, hidden items, deleted items, and search results.
- [ ] Verify that frontend route guards are backed by server-side authorization checks.
- [ ] Attempt IDOR-style requests by changing IDs, UIDs, slugs, filenames, hashes, album IDs, user IDs, and path-like parameters.
- [ ] Confirm authorization is enforced consistently across UI, API, WebDAV, download, thumbnail, preview, and original-file endpoints.
- [ ] Verify access is revoked when a share is disabled, a user is disabled, a session is terminated, or permissions change.

### 6. Session Management

- [ ] Verify cookie flags: `HttpOnly`, `Secure` on HTTPS, appropriate `SameSite`, path, domain, expiry, and max-age.
- [ ] Confirm session IDs are rotated after login, logout, privilege changes, password changes, and authentication-provider changes where applicable.
- [ ] Test logout from the UI and API; session cookies and server-side state should become unusable.
- [ ] Test expired, invalid, tampered, reused, and concurrent sessions.
- [ ] Verify CSRF protections on state-changing browser requests, including admin settings, sharing, upload, delete, import, index, and user-management actions.
- [ ] Confirm session or token values are never exposed in URLs, logs, referrers, frontend state, crash reports, or analytics.
- [ ] Check JWT handling if tokens are used: issuer, audience, expiry, algorithm restrictions, signature validation, key rotation, and rejection of unsigned or malformed tokens.

### 7. Input Validation and Injection

- [ ] Test all changed parameters with missing, null, empty, oversized, duplicated, unexpected, malformed, and type-confused values.
- [ ] Test reflected, stored, and DOM-based XSS in filenames, titles, captions, descriptions, album names, labels, people names, places, camera metadata, EXIF fields, search queries, and admin settings.
- [ ] Test SQL injection and ORM/query-builder misuse in search, filters, sort fields, IDs, pagination, metadata filters, library paths, and admin queries.
- [ ] Test path traversal and file inclusion in upload, import, download, sidecar, thumbnail, cache, backup, and WebDAV operations.
- [ ] Test command injection around media tools, metadata extractors, video transcoding, file conversion, and external binary invocations.
- [ ] Test SSRF and host-header injection anywhere URLs, webhooks, remote imports, proxy headers, callback URLs, or external services are accepted.
- [ ] Test HTTP request smuggling and response splitting only in an approved production-like lab environment.
- [ ] Verify JSON, form, multipart, and WebDAV request parsing cannot bypass validation.
- [ ] Test mass assignment and auto-binding by adding unexpected JSON fields such as `admin`, `role`, `owner`, `path`, `uid`, `public`, `private`, `verified`, or `disabled`.
- [ ] Verify CSV, text, metadata, and export functionality cannot trigger CSV injection or formula execution when opened in spreadsheet software.

### 8. Upload, Import, and Media Processing

- [ ] Enforce allowlists for supported file types and reject dangerous extensions, polyglot files, scripts, archives, and unexpected MIME types.
- [ ] Validate file content independently of filename, extension, and client-provided MIME type.
- [ ] Test malformed EXIF, IPTC, XMP, ICC, GPS, video, RAW, and sidecar metadata.
- [ ] Test large files, many small files, duplicate names, Unicode normalization, reserved names, long paths, symlinks, hard links, hidden files, and path separators.
- [ ] Verify uploaded and imported files cannot escape configured storage, originals, import, cache, sidecar, or temp directories.
- [ ] Confirm generated thumbnails, previews, transcoded videos, and cached files do not expose originals or private metadata beyond the current user's permissions.
- [ ] Verify failed processing does not leave world-readable temp files, partial originals, stale database rows, or inconsistent permissions.
- [ ] Check antivirus, malware scanning, or external scanning integration if enabled in the target deployment.

### 9. Error Handling and Logging

- [ ] Ensure errors do not reveal stack traces, SQL queries, filesystem paths, secrets, internal hostnames, environment variables, tokens, or private metadata.
- [ ] Confirm security-relevant events are logged: login failures, logout, password changes, admin changes, share changes, import/index actions, suspicious access, and authorization failures.
- [ ] Verify logs redact passwords, cookies, authorization headers, API keys, tokens, private URLs, and sensitive metadata.
- [ ] Test failed uploads, parser crashes, database errors, storage errors, missing files, permission failures, and worker failures.
- [ ] Confirm user-facing errors are actionable but do not disclose implementation details.

### 10. Cryptography and Transport Security

- [ ] Verify TLS termination, redirect-to-HTTPS behavior, HSTS, secure cookies, and mixed-content handling in production-like deployments.
- [ ] Ensure secrets, tokens, password hashes, signing keys, and encryption keys use approved algorithms and adequate entropy.
- [ ] Confirm passwords are hashed with a modern password hashing scheme and never logged or returned.
- [ ] Verify random identifiers for sessions, shares, tokens, invite links, and reset flows are not predictable.
- [ ] Confirm sensitive values are not stored in local storage, browser storage, logs, config files, exported diagnostics, or crash reports unless explicitly intended and protected.

### 11. Business Logic

- [ ] Test workflows in unexpected order: upload before login, share after revoke, delete while indexing, download after archive/delete, role change during an active session, and concurrent edits.
- [ ] Verify state transitions for photos, albums, people, labels, private/public status, hidden/archive/delete, favorites, and shares.
- [ ] Test quotas, rate limits, pagination, batch operations, imports, indexing jobs, and background workers for abuse or inconsistent authorization.
- [ ] Confirm users cannot forge requests to assign ownership, change media paths, bypass indexing restrictions, or expose private content through search or sharing.
- [ ] Test race conditions in upload, import, delete, restore, share revoke, password change, and role change workflows.
- [ ] Verify email, notification, and external integration behavior does not leak private URLs or metadata.

### 12. Client-Side Security

- [ ] Test DOM XSS and HTML injection in UI-rendered filenames, metadata, descriptions, labels, people, places, search terms, and error messages.
- [ ] Verify frontend route guards do not display cached private data after logout, role change, session expiry, or user switch.
- [ ] Check CORS configuration for API endpoints, WebDAV, static assets, previews, and downloads.
- [ ] Verify CSP compatibility with the frontend build and reject unnecessary `unsafe-inline`, `unsafe-eval`, wildcard origins, or broad frame permissions.
- [ ] Test clickjacking protections for authenticated pages and sensitive actions.
- [ ] Review browser storage for sensitive values and ensure logout clears sensitive local state where applicable.
- [ ] Test reverse tabnabbing and unsafe external links in documentation, settings, metadata, and generated pages.

### 13. API Testing

- [ ] Enumerate API endpoints used by the UI and integrations; verify unauthenticated requests are rejected unless explicitly public.
- [ ] Test broken object-level authorization by changing object identifiers, UUIDs, slugs, paths, hashes, and pagination cursors.
- [ ] Test broken function-level authorization by invoking admin, import, index, delete, restore, share, and user-management endpoints with lower privileges.
- [ ] Verify excessive data exposure is not present in JSON responses, including hidden fields, private paths, GPS data, face/person data, tokens, config values, and internal IDs.
- [ ] Test schema validation for JSON bodies, query strings, multipart uploads, PATCH/PUT requests, and batch operations.
- [ ] Check rate limits and abuse controls for login, search, upload, download, thumbnails, WebDAV, and public links.
- [ ] Verify API errors use consistent status codes and do not leak implementation details.
- [ ] Confirm API documentation and generated clients do not expose private endpoints unintentionally.

### 14. WebDAV

- [ ] Verify WebDAV authentication and authorization independently from the web UI.
- [ ] Test `PROPFIND`, `GET`, `PUT`, `DELETE`, `MOVE`, `COPY`, `MKCOL`, and unsupported methods for access-control bypasses.
- [ ] Test path traversal, Unicode normalization, hidden files, reserved names, long paths, duplicate names, and case-sensitivity issues.
- [ ] Confirm WebDAV access respects disabled users, revoked sessions, password changes, read-only modes, private media, and configured storage restrictions.
- [ ] Verify WebDAV errors and directory listings do not expose private filesystem paths or implementation details.

### 15. Privacy and Metadata

- [ ] Verify GPS, camera serial numbers, timestamps, people/face data, labels, captions, albums, and private paths are only exposed where intended.
- [ ] Test public shares and unauthenticated endpoints for accidental metadata disclosure.
- [ ] Confirm thumbnail, preview, video, and export generation does not preserve sensitive metadata unless intended.
- [ ] Verify search indexes, cache files, sidecar files, logs, diagnostics, and backups do not expose private data beyond the deployment's threat model.
- [ ] Test account deletion, media deletion, and cleanup workflows for stale private data.

### 16. Denial of Service and Abuse Resistance

- [ ] Test reasonable limits for upload size, batch size, search complexity, pagination, concurrent requests, indexing jobs, import jobs, and WebDAV operations.
- [ ] Avoid destructive DoS testing on shared systems; use controlled local or staging environments.
- [ ] Test parser and media-processing failure modes with malformed or adversarial files.
- [ ] Verify background workers cannot be starved or forced into unbounded retries by user-controlled input.
- [ ] Confirm expensive endpoints require authentication and appropriate authorization unless intentionally public.

## Pull Request Review Template

Copy this section into security-sensitive pull requests:

```markdown
## Security Review

- [ ] Authentication impact reviewed
- [ ] Authorization and object-level access reviewed
- [ ] Session, cookie, CSRF, or token impact reviewed
- [ ] Input validation and injection risks reviewed
- [ ] Upload/import/media-processing risks reviewed
- [ ] Privacy and metadata exposure reviewed
- [ ] API response data exposure reviewed
- [ ] Reverse proxy, headers, CORS, or CSP impact reviewed
- [ ] Error handling and logging reviewed
- [ ] Regression tests added or updated
- [ ] Manual test notes included below

### Manual Test Notes

Environment:

Affected endpoints/routes:

Test users/roles:

Commands/tools used:

Findings:

Residual risk / follow-up issues:
```

## Reporting Findings

Security findings should include:

- Affected version, commit, branch, deployment mode, and database backend.
- Preconditions, user role, and required configuration.
- Exact request, route, endpoint, or UI workflow.
- Expected result and actual result.
- Security impact, affected data, and exploitability.
- Reproduction steps and logs with secrets redacted.
- Suggested fix and regression-test coverage.

Do not publish exploitable vulnerability details before maintainers have had a reasonable opportunity to investigate and release a fix. Use the project's documented security reporting channel for suspected vulnerabilities.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP WSTG Latest on GitHub](https://github.com/OWASP/www-project-web-security-testing-guide/tree/master/latest)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OpenSSF Best Practices](https://www.bestpractices.dev/)