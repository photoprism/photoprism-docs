# Info Sidebar

The Info Sidebar opens alongside the full-screen viewer and shows the metadata of the currently displayed picture or video. It is a lightweight alternative to the [Edit Dialog](edit.md) when you want to inspect or quickly correct individual fields without leaving the viewer.

<!-- TODO: screenshot info-sidebar-2505.jpg -->
![Screenshot](img/info-sidebar-2505.jpg){ class="shadow" }

## Opening the Info Sidebar

Press **Ctrl + I** while a picture is open in the full-screen viewer, or pick "Toggle Info Sidebar" from the viewer menu. The same shortcut closes it again. The sidebar position is remembered across page reloads, so it stays open until you explicitly close it.

## What It Shows

The sidebar surfaces the most frequently inspected metadata fields:

- **File:** path and filename of the currently displayed media file.
- **Camera:** make and model, lens, ISO, exposure, focal length, and f-number.
- **Description:** title, caption, artist, copyright, and license.
- **Labels:** clickable chips that link to the matching label page.
- **Albums:** clickable chips that link to the matching album page.
- **People:** clickable chips that link to the matching person page.

Clicking a chip navigates to the matching page so you can browse the rest of the collection in that context.

## Editing Metadata in Place

Click on a field to edit it. Some fields can be changed inline, while others open an overlay. Press Escape to cancel, and confirm to save your changes — invalid values cannot be saved.

## Face Markers

The Info Sidebar provides the same face-management actions that are available on the *People* tab of the [Edit Dialog](edit.md):

- [Assign Names to Faces](people.md#assign-names-to-faces)
- [Change People Assignments](people.md#change-people-assignments)
- [Remove Faces](people.md#remove-faces)

In addition, the Info Sidebar is the only place where you can **manually mark a face** that PhotoPrism missed during automatic detection, by drawing a rectangle on the picture and then assigning a person to it.

<!-- TODO: screenshot manual-face-marker-2505.jpg -->
![Screenshot](img/manual-face-marker-2505.jpg){ class="shadow" }
