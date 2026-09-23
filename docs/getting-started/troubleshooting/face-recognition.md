# Troubleshooting Face Recognition

!!! info ""
    You are welcome to ask for help in our [community chat](https://link.photoprism.app/chat).
    [Sponsors](https://www.photoprism.app/membership/) receive direct [technical support](https://www.photoprism.app/contact/) via email.
    Before [submitting a support request](../../user-guide/index.md#getting-support), please go through the checklists below.

Faces are recognized in three stages — detection, embedding, and clustering — so a problem usually belongs to one of them. [AI Models > Face Recognition](../../user-guide/ai/face-recognition.md) explains how they work and lists the available config options.

## First Checks

Start here whatever the symptom, as this rules out the most common causes in one step:

- [ ] Run `photoprism faces status` [in a terminal](../docker-compose.md#command-line-interface). It reports the model in use, the options actually in force, and why clustering is waiting when no clusters are forming
- [ ] Note which build you are running: it is shown as **Build** in the footer of any Settings page, or run `photoprism --version`
- [ ] Watch the [service logs](docker.md#viewing-logs) while you reproduce the problem, and raise the log level if nothing stands out
- [ ] Make sure face recognition has not been switched off with `PHOTOPRISM_DISABLE_FACES`

## Tagging Is Slow

Naming faces should feel immediate. When it does not, first find out *where* the time goes, then work through the matching group:

- [ ] Update to the latest release and try again — the *People* view is improved regularly
- [ ] Open your [browser's developer tools](browsers.md#getting-error-details), switch to the **Network** tab, then click a face and save a name. This tells you whether the delay is in the browser or in a server request, which have completely different causes
- [ ] Check the [logs](docker.md#viewing-logs) for rate limit errors while you are editing faces — they look like slowness in the UI, but are not

If the server requests are slow:

- [ ] Use [MariaDB instead of SQLite](sqlite.md#migrating-to-mariadb) for larger libraries, and review its [performance notes](mariadb.md#bad-performance)
- [ ] Put the *storage* folder and the database on an [SSD rather than an HDD](performance.md#storage)
- [ ] Verify the server has enough [memory](performance.md#memory), and [add swap](docker.md#adding-swap) if it does not
- [ ] Check the [CPU](performance.md#server-cpu) is not saturated, and note that [older hardware](performance.md#legacy-hardware) is slower at this than at anything else PhotoPrism does
- [ ] Wait until indexing or import has finished, since the [background worker](../../known-issues.md#background-worker) competes with them

If only the browser is slow:

- [ ] [Try another browser](browsers.md#try-another-browser), and disable extensions that modify pages
- [ ] Look for errors in the **Console** tab

## No Faces Found

- [ ] Confirm a detector is active with `photoprism faces status`, and that `PHOTOPRISM_DISABLE_FACES` is unset
- [ ] Run `photoprism faces index` to detect faces in pictures that were indexed earlier
- [ ] Lower [`PHOTOPRISM_FACE_SIZE`](../../user-guide/ai/face-recognition.md#detection-settings) if the faces you expect are small, and see [Small Faces in Group Pictures](../../user-guide/ai/face-recognition.md#small-faces-in-group-pictures)
- [ ] Rotate pictures that are not displayed upright and index them again, as [rotated faces](../../known-issues.md#rotated-faces) are often not detected at all
- [ ] Note that recognition is less reliable for [young children](../../known-issues.md#children-and-pictures-taken-years-apart)

## No People Shown

Faces have been detected, but *People* stays empty:

- [ ] Run `photoprism faces status` to see why clustering is waiting
- [ ] Run `photoprism faces update --force` so a pass runs at the current settings instead of waiting for enough new faces
- [ ] Review [`PHOTOPRISM_FACE_CLUSTER_SIZE`](../../user-guide/ai/face-recognition.md#clustering-settings), which is the minimum size a face must have to help form a new person
- [ ] After a [model upgrade](../../known-issues.md#model-upgrade), run `photoprism faces index` before `photoprism faces update --force`
- [ ] Check that the [background worker](../../known-issues.md#background-worker) runs regularly

## Wrong Grouping

Different people are grouped together, or one person appears several times:

- [ ] Upgrade an older library to the current model, which separates people noticeably better — see [Upgrading an Existing Library](../../user-guide/ai/face-recognition.md#upgrading-an-existing-library)
- [ ] Change a distance threshold [relative to the value your model resolves to](../../user-guide/ai/face-recognition.md#tuning-tips), never by carrying a number over from another model
- [ ] Run `photoprism faces audit --fix` to resolve inconsistencies
- [ ] Check whether the pictures show [rotated faces](../../known-issues.md#rotated-faces) or [children](../../known-issues.md#children-and-pictures-taken-years-apart)
- [ ] See [Photos With All Faces Assigned Appear Under "New Faces"](../../known-issues.md#photos-with-all-faces-assigned-appear-under-new-faces) when stacked pictures are involved

## Lost Assignments

Names disappear, revert, or the logs mention ambiguous subjects:

- [ ] Wait until saving has finished before assigning the next face, and avoid editing people in several browser tabs at once
- [ ] Avoid running more than one instance against the same database, and do not change database content directly
- [ ] Run `photoprism faces audit --fix`, as described under [Inconsistent Face Assignments](../../known-issues.md#inconsistent-face-assignments)

## Missing XMP Names

Names stored in sidecar files or embedded metadata do not appear:

- [ ] Make sure [ExifTool is installed](metadata.md#installing-exiftool)
- [ ] Update to the latest release, since metadata support is extended regularly
- [ ] Index the affected pictures again, using a [complete rescan](../../user-guide/library/originals.md#when-should-complete-rescan-be-selected) if a normal run changes nothing
- [ ] Compare what your files contain with the fields we read, listed in [Adobe XMP](../../developer-guide/metadata/xmp.md#fields-extracted-from-xmp)

## Starting Over

When a library is in a state that is quicker to rebuild than to repair:

- [ ] [Create a backup](../../user-guide/ai/face-recognition.md#creating-a-backup) first, since none of the following can be undone
- [ ] `photoprism faces reset` removes automatic clusters and matches, keeping the names you assigned
- [ ] `photoprism faces reset --all` also removes the names, keeping the markers
- [ ] `photoprism faces reset --force` removes the markers as well, so faces must be detected again with `photoprism faces index`
