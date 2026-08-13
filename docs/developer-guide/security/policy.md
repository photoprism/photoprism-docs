# Vulnerability Disclosure Guidelines

Visit [**photoprism.app/security-policy**](https://www.photoprism.app/security-policy/) to learn more about our security policy, responsible disclosure, and how you can report issues as a business or organization.

That page states the terms and is authoritative if anything here appears to differ. The sections below explain the reasoning behind three of them, since they are the ones that most often come up.

## Auto-Generated Reports

We ask that a report be reviewed by a person before it is sent, and we may not respond to one that
has clearly not been. This is not a formality: unreviewed output costs us the same attention as a
genuine finding, and that attention is the same resource we use to fix real issues.

A report has been reviewed when you can tell us:

- The exact version and build number you tested, which you will find in *Settings* by scrolling to
  the bottom, or by running `photoprism --version`.
- That you reproduced the behavior yourself against a running instance, and the steps you used.
- What you observed and what you expected instead.

Two things in particular are worth checking before you write to us:

- **A finding reported by a scanner is a starting point, not a conclusion.** Scanners flag patterns,
  not exploitability, and they cannot see which code paths an application actually reaches. If you
  send us scanner output, please tell us which tool and version produced it and which findings you
  have confirmed by hand.
- **A vulnerability in a dependency is not automatically a vulnerability in PhotoPrism.** Whether an
  advisory against a library affects us depends on whether we call the affected code and on how. We
  track our dependencies and update them on their own schedule, so a version-match alone is usually
  something we already know about.

Language models are useful for understanding unfamiliar code, and we use them ourselves. They are
also confident about behavior they have not observed, so please verify what one tells you against a
running instance before reporting it as a vulnerability.

## Publication and CVE Identifiers

We ask for 90 days between your report and any public disclosure, and we ask that you tell us before
requesting a CVE ID. The reasoning is worth stating plainly, because the timing matters more than it
might appear.

A CVE record is not only a description of a problem. Once published it is ingested by vulnerability
databases and by the scanners that our users, and their security teams, run against their
installations. A record that is inaccurate or that describes intended behavior therefore reaches
people who have no way to assess it, and corrections propagate slowly and unevenly, if at all. A
record that is accurate but published before a fix exists tells everyone how to reach a problem that
users cannot yet protect themselves against. Neither outcome helps the people the record is meant to
protect.

Anyone may request an identifier from a CVE Numbering Authority (CNA), and a CNA can assign one
without the vendor being involved. The CVE Program's CNA Operational Rules nevertheless expect a CNA
to make a good faith effort to notify the vendor before a record is published, and the program
provides a dispute process along with an escalation path through the assigning CNA, its Root, and the
Top-Level Root above it. So if you approach a CNA about PhotoPrism, please give it our contact
details and tell us at the same time. Our address is published in
[security.txt](https://www.photoprism.app/.well-known/security.txt), in
[SECURITY.md](https://github.com/photoprism/photoprism/blob/develop/SECURITY.md), and on our
[security policy](https://www.photoprism.app/security-policy/) page, so there is always a documented
way to reach us.

When a record is published without an attempt to contact us, we ask the assigning CNA to correct or
reject it. We also raise the matter with the CNA's Root if the rules were not followed and publish
our own assessment alongside the record. However, we would much rather agree on an accurate advisory
with you before publication.

## Bug Bounty Program

We do not operate a bug bounty program and do not offer payment or comparable compensation for
vulnerability reports.

PhotoPrism is developed by a small team, and a bounty program is not only its payouts: it is triage
capacity, an accepted-severity scale to argue over, and a steady volume of speculative submissions.
We would rather spend that time on the reports we do receive and on the software itself.

That does not make reports unwelcome. A report that follows our
[security policy](https://www.photoprism.app/security-policy/) gets read by a person, and confirmed
vulnerabilities are fixed within 90 days depending on severity and on whether third-party packages
are involved.
