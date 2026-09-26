# Testing OfficeBook

`./ob open FILE` copies a document to Download/ and opens it in the app;
`./ob logs` shows the app's log. Delete the Download/ copies afterwards.

## Checklist

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
