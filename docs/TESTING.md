# Testing OfficeBook

`./ob open FILE` copies a document to Download/ and opens it in the app. The
shell can't grant the app a file of the Googlebook's user, so it turns on the
all-files access the app requests; `./ob revoke` turns it off and deletes the
test files. `./ob logs` shows the app's log. `adb shell am task resize TASK
L T R B` resizes the window without touching input.

## Checked on the Googlebook (2026-09-27, build 36273679248, 26.04.3.1-1)

| Check | Result |
| --- | --- |
| Build | first try, public runner (4 cores, 15 GB): engine 165 min, web UI 1 min, Gradle 5 min; APK 267 MB (native libraries 214 MB) |
| Install, start screen | opens in a desktop window, "OfficeBook" |
| First document start | "Preparing for the first start after an update" while it unpacks fonts and resources, then the document |
| Desktop UI (patch 0001) | a .docx opens with the classic menu bar (File, Edit, View, Help), the Viewing/Editing switch and the desktop status bar (page, word count); no tablet ribbon |
| Resize (patch 0002) | 1382x864 → 731x592 → back with `am task resize`: same process, no activity restart, document stays open |
| Live resize | `./ob live-resize` on; dragging not tried yet |

Known issues: the launcher icon is Android's generic one (the build has no
branding), and the caption bar is pink (the theme's colour). A `file://`
VIEW intent leaves LOActivity on "Preparing…" for good: it only continues
for `content://` URIs.

## Checklist (for a person)

- [ ] The start screen opens in a desktop window; New document (Writer,
      Calc, Impress, Draw) works.
- [ ] A document opens with classic menus (File, Edit, View…) and the
      desktop toolbar, not the tablet ribbon.
- [ ] Keyboard shortcuts (Ctrl+S, Ctrl+B, Ctrl+Z), right-click menus,
      copy and paste with other apps.
- [ ] Resize the window while a document is open: it stays open and
      relays out. With `./ob live-resize` on, no veil.
- [ ] Open .docx, .xlsx, .pptx and ODF files from Files; save in place;
      Save As.
- [ ] Print; export PDF.
- [ ] Impress slideshow.
