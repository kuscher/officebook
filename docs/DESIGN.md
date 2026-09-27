# OfficeBook design

## What Collabora's Android app is

Collabora Office for Android (android/ in the Collabora Online monorepo) is
three layers in one APK:

- **The engine** (engine/, LibreOffice-based, C++): Writer, Calc, Impress
  and Draw, built for Android as one big `liblo-native-code.so` plus NSS
  libraries and its resources (instdir: fonts, configuration, dictionaries).
- **COOLWSD in-process** (online's common/, kit/, net/, wsd/ as
  `libandroidapp.so`): the same document server that runs Collabora Online,
  talking to the web UI over a fake socket instead of the network.
- **The web UI** (browser/, the one Collabora Online serves) in a WebView,
  `file:///android_asset/dist/cool.html`, driven by `LOActivity`.
  `LibreOfficeUIActivity` is the start screen (recent files, new document).

## The patches

1. **Desktop UI on Android PCs.** The app picks the tablet ribbon
   ("notebookbar") for large screens unless `isChromeOS()`, and the web UI
   asks the same question through the `COOLMessageHandler.isChromeOS()`
   JavaScript interface: `global.mode.isDesktop()` is true, `isTablet()`
   false, only on ChromeOS. The Googlebook runs Android itself and declares
   `android.hardware.type.pc` (FEATURE_PC; checked with `pm list features`),
   not ChromeOS's `org.chromium.arc.device_management`. The patch adds
   `LOActivity.isDesktop()` (ChromeOS or FEATURE_PC) and uses it for the UI
   mode, the JavaScript interface and the start screen's button. The file
   picker keeps a ChromeOS-only workaround (no MIME filter), which
   Android's own picker doesn't need.
2. **Resizing keeps the document open.** The two activities didn't declare
   `smallestScreenSize` and `density` in configChanges, so a desktop window
   resized across a size bucket, or moved to another display, restarted the
   activity and reloaded the document.
3. **The tabbed ribbon on desktops.** The app asked the web UI for the
   classic menu bar on ChromeOS (and, with patch 1, Android PCs) and for the
   tabbed ribbon ("notebookbar") only on tablets, a choice from before the
   desktop app, which always uses the ribbon. Desktops now get the ribbon
   too; phones keep the classic mobile UI. View > Use Compact view switches
   back and is remembered.
4. **No wallpaper-coloured caption bar.** Android's desktop mode draws each
   window's caption bar in colours from the wallpaper (the SystemUI code
   takes only light or dark from the app) unless the app asks for a
   transparent one. Both activities ask for it; the document window paints
   the web UI's `--color-main-background` under it, and the start screen's
   toolbar already reaches up under it.

5. **Chromebook detection (a web UI bug).** `global.mode.isChromebook()`
   was computed in `InitializerBase`'s constructor, before
   `AndroidAppInitializer` sets `ThisIsTheAndroidApp`, so it was always
   false: the app on ChromeOS (and with patch 1, on a Googlebook) took the
   tablet paths, with the floating edit button. It's now asked on first use.
6. **The desktop app's behaviour (web UI).** `window.mode.isCODesktop()`
   unlocks what Collabora Office on Windows, macOS and Linux does
   differently: the backstage view (a full-window File tab with New, Open,
   recent documents, Save As, Export, Print), the starter screen, the
   ruler by default, Ctrl+O and Ctrl+N, and more. It's also true when the
   Android app says so (`COOLMessageHandler.isCODesktop()`, asked once).
   What the Android app can't host stays off there: the presenter console
   and swapping monitors (a second window), the welcome slideshow (not
   packaged), task workers (file:// origin), the Options dialog (settings
   storage). `postMobileCall()` returns the app's answer.
7. **The desktop app's messages (Android).** `LOActivity` says it's the
   desktop app on a PC and answers what the backstage sends, as
   qt/Bridge.cpp does: `GETRECENTDOCS`, `opendoc`, `newdoc` (a template
   from the web UI's templates/, copied to where the user picks),
   `uno .uno:Open`, `uno .uno:SaveAs` (the existing copy-with-TakeOwnership
   path), `TEXTCLIPBOARD`, `SETDARKMODE`, `FULLSCREENPRESENTATION`,
   `LICENSE`, and drops the desktop-only rest. `DesktopDocuments` holds the
   document actions and the recent list (the start screen's
   `RECENT_DOCUMENTS_LIST`, now without duplicates).
8. **The starter screen (Android).** On a PC, the launcher's start screen
   hands over to `StarterActivity`: `cool.html?starterMode=true` in a
   WebView with no document and no COOLWSD, answering the starter's
   messages with `DesktopDocuments`, and reloading when a document closes.
9. **OfficeBook only:** a broadcast receiver guarded by `DUMP` (adb's
   shell) turns on WebView debugging (`./ob devtools on`), since the
   setting for it hangs off the phone-style start screen.

## Branding

`branding/` goes to configure as `--with-app-branding`, the build's own hook
for a branded app, so no patch is needed: `android/` is copied into the
app's resources (the launcher icon `ic_launcher_brand`, an adaptive icon
of a page in the suite's colours, and the About dialog's icon), and
`branding.js` names the product OfficeBook in the web UI. `branding.css` and
`images/toolbar-bg-logo.svg` only have to exist for the build.

## Building (GitHub Actions)

The engine's configure picks the NDK's `linux-x86_64` toolchain and Gradle's
CMake comes as x86_64 only, and the Googlebook's Linux VM is arm64, so the
build runs on ubuntu-24.04 runners, following android/README.md and the
monorepo's Nix shell (nix/shells/android.nix: NDK 29.0.14206865, CMake
3.22.1, build-tools 37.0.0, JDK 17, Node):

1. Check out UPSTREAM's commit (2.3 GB: the engine is in the monorepo), apply
   patches/.
2. **Engine**: engine.conf becomes engine/autogen.input
   (`--with-distro=CPAndroidAarch64`, English only), then `make`. Its outputs
   that the app build reads (instdir, android/jniLibs, POCO/zstd/libpng from
   the workdir, config_host) are cached as one tarball under a key of
   UPSTREAM, engine.conf and any engine/ patch. ccache (6 GB) is saved even
   when the build times out, so a cold build that doesn't fit in one 6-hour
   job continues in the next run.
3. **App**: online's `./configure --enable-androidapp` with our package name
   (`local.officebook`), app name and version, `make` (web UI and config),
   then `./gradlew assembleRelease`, which compiles online's C++ against the
   engine and packages the APK.
4. The unsigned APK is the artifact; `./ob fetch` signs it with the local
   keystore.jks (not in git).

Versions: versionName is Collabora's (26.04.3.1 from configure.ac), and
versionCode is VERSION_CODE; configure takes both as
`--with-android-package-versioncode=26.04.3.1-<code>`.

UPSTREAM follows `distro/collabora/co-26.04-mobile`, the branch the store
apps come from, not main.
