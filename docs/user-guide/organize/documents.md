# Reading Documents #

PhotoPrism indexes PDF files as *documents* and renders their first page as a cover image, so they appear in
search results next to your pictures and videos. Clicking a document opens it in the built-in viewer, where you
can read all of its pages without downloading the file first.

## Finding Documents ##

Navigate to *Search > Documents* to browse everything that has been classified as a document.
You can also limit any search to documents with the `document:yes` filter or the more general `type:document`
filter. [Learn more ›](../search/filters.md#filter-reference)

## Using the Viewer ##

Open a document by clicking its cover in search results. The viewer loads all pages and shows the following controls:

#### :material-view-grid: Thumbnails ####

A strip of page thumbnails is shown on the left so you can see the structure of a document at a glance and jump
straight to a page. Use the :material-view-grid: button to hide the strip and give the page more room.
It is not available on phones, where it would take up most of the screen.

#### :material-chevron-right: Pages ####

Scroll or swipe to move through the document, or use the :material-chevron-left: and :material-chevron-right:
buttons next to the page number. To jump to a specific page, type its number into the page field and press **Enter**.
On a keyboard, **Up**, **Down**, and **Page Down** scroll the current page.

#### :material-magnify-plus-outline: Zoom ####

A document opens at a zoom level that fits a whole page on your screen where possible, and fits the page width
otherwise. Use the :material-magnify-minus-outline: and :material-magnify-plus-outline: buttons to change it, or
pinch with two fingers on a touch screen. When a page is larger than the window, you can drag it with the mouse
to pan around.

#### :material-chevron-double-right: Other Documents ####

To move to the previous or next document without leaving the viewer, use the arrows at the left and right edge of
the screen, press the **Left** and **Right** arrow keys, or swipe inward from the left or right edge on a touch screen.

## Sharing Documents ##

Documents can be added to albums and [shared](../share/index.md) like any other file. Everyone who opens the
share link can read the shared documents in the same viewer, without being able to reach documents outside
the shared albums.

## Limitations ##

- The viewer is read-only. Editing, annotating, and filling in forms are not supported.
- Text inside a document cannot be selected or searched. Only the metadata PhotoPrism has indexed is searchable.
- Documents have no faces, so the *People* section of the [info sidebar](info-sidebar.md) is hidden for them.
- Very large documents with thousands of pages may take a moment to open.

!!! tldr ""
    PhotoPrism renders the cover image of a PDF with [ImageMagick](../settings/advanced.md#disable-imagemagick) while indexing, and reads its title, description, and page count with [ExifTool](../settings/advanced.md#disable-exiftool). The pages you read in the viewer are rendered by your browser, so a reasonably current browser is required.
