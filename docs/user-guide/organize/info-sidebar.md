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

Each editable field opens a small popover when clicked. Enter the new value and confirm to save — input is validated against the same length and range limits as the [Edit Dialog](edit.md), and the popover refuses to save invalid values.

If you change your mind, close the popover with Escape or by clicking outside. Leaving the sidebar with unsaved changes prompts you to discard or keep them.

## Face Markers

When a picture is open in the viewer, you can add, edit, and remove face markers directly from the Info Sidebar:

- **Add:** draw a rectangle around an unrecognized face and assign or create a person.
- **Edit:** click an existing marker to reassign it to a different person or to refine the bounding box.
- **Remove:** delete an incorrect or duplicate marker.

Changes are saved immediately and reflected in the People section.

## Roles & Permissions

The Info Sidebar respects the same access rules as the rest of PhotoPrism:

- **Admins and Managers** see all fields and can edit them inline.
- **Guests, Visitors, and Contributors** see a reduced, read-only view that omits administrative metadata.

See [User Roles](../users/roles.md) for the complete capability matrix.
