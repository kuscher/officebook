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
