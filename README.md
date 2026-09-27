# OfficeBook

Collabora Office, the LibreOffice-based office suite, as an Android app for
the HP Googlebook 14, with the **desktop interface**: classic menus and
toolbars, as on a laptop, instead of the tablet ribbon Collabora's Play
Store app shows on Android. Writer, Calc, Impress and Draw documents (ODF and
Microsoft Office formats) open and save on the device. No server, no Linux
VM.

Status: builds and runs; documents open with the desktop UI (see
docs/TESTING.md). Editing, saving and printing still to be tried.

## Install

Open `OfficeBook-<version>.apk` from the Download folder in Files and allow
Files to install it if Android asks. It installs next to Collabora Office
from Play, if you have that; they don't share settings.

**Live window resizing** (optional, needs adb once): Android normally hides
a window behind a veil while you resize it. Run
`adb shell am compat enable ENABLE_FLUID_RESIZING local.officebook` (or
`./ob live-resize`) and reopen OfficeBook.

## What's different from Collabora Office for Android

- The desktop UI on Android PCs (Android's `FEATURE_PC`), which upstream
  only gives ChromeOS, with the tabbed ribbon like Collabora Office on the
  desktop (View > Use Compact view for the classic menus).
- Resizing the window or moving it to another display doesn't restart the
  document.
- The window's caption bar matches the app instead of the wallpaper.
- Its own name and package (`local.officebook`), so it isn't mistaken for
  Collabora's official app.
- English only for now.

## Building

The APK is built in GitHub Actions: Collabora's engine needs the Android
NDK's x86_64 toolchain.

```sh
./ob ci && ./ob wait      # build (hours the first time; the engine is cached after)
./ob fetch                # download and sign: executables/OfficeBook-<version>.apk
./ob install && ./ob start
```

`./ob fetch` signs with your own `keystore.jks` (password in
`keystore.pass`), which stays out of git; keep a backup, since updates
must be signed with the same key. See [docs/DESIGN.md](docs/DESIGN.md), and
[docs/UPSTREAMING.md](docs/UPSTREAMING.md) for the changes we'd like to
offer Collabora.

## License

Collabora Online is MPL-2.0; its engine (LibreOffice-based) is MPL-2.0 and
LGPL-3.0, with third-party parts under their own licenses. Whoever you give
the APK to is entitled to its source: this repository, and Collabora Online
at the commit in UPSTREAM. "Collabora" and "LibreOffice" are trademarks of
their owners; OfficeBook is not affiliated with either.
