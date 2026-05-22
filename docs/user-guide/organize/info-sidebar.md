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

The Info Sidebar provides the same face-management actions that are available on the *People* tab of the [Edit Dialog](edit.md), and is the only place where you can **manually mark a face** that PhotoPrism missed during automatic detection.

Click :material-pencil-outline: next to *People* to enter *edit mode*, which displays all existing face markers on the image and unlocks the change, remove, and manual-marker actions below. Click :material-pencil-off-outline: when you are done. Edit mode is not required to assign a name to an existing unnamed face.

### Assign Names to Faces ###

1. Open a photo in the [full-screen viewer](../search/views.md) and open the Info Sidebar by pressing **Ctrl + I**.
2. Click the name field next to the face you want to name.
3. Start typing a name; existing people are suggested as you type.
4. Press *enter* to confirm.

### Change People Assignments ###

1. Open a photo in the [full-screen viewer](../search/views.md) and open the Info Sidebar by pressing **Ctrl + I**.
2. Click :material-pencil-outline: next to *People* to enter edit mode.
3. Click :material-eject: next to the person you want to change.
4. Type a new name and press *enter*, or leave the field empty.

### Remove Faces ###

Like on the *People* tab of the Edit Dialog, only unnamed face markers can be removed.

1. Open a photo in the [full-screen viewer](../search/views.md) and open the Info Sidebar by pressing **Ctrl + I**.
2. Click :material-pencil-outline: next to *People* to enter edit mode.
3. Click the face marker on the image.
4. Click :material-check: in the confirm pill to remove it.

### Manually Mark a Face ###

1. Open a photo in the [full-screen viewer](../search/views.md) and open the Info Sidebar by pressing **Ctrl + I**.
2. Click :material-pencil-outline: next to *People* to enter edit mode.
3. Drag on the image to draw a rectangle around the missed face.
4. Click :material-check: in the confirm pill to keep the new marker.
5. Type a name in the new row that appears under *People*, then press *enter* to assign a person.

<!-- TODO: screenshot manual-face-marker-2505.jpg -->
![Screenshot](img/manual-face-marker-2505.jpg){ class="shadow" }
