# Upstreaming to Collabora

OfficeBook's changes that would help Collabora Office itself run well on
Googlebooks (Android's desktop mode) are tracked here, to be offered to
Collabora. Nothing has been submitted yet.

## How Collabora takes changes

From CONTRIBUTING.md in the monorepo:

- **Gerrit, not GitHub.** Changes go to https://gerrit.collaboraoffice.com
  (sign in with GitHub, add an SSH key). Pull requests on the GitHub mirror
  are closed automatically. Install Gerrit's commit-msg hook (Change-Id),
  then `git push origin HEAD:refs/for/main`.
- **Against main.** Our patches are made on co-26.04-mobile, the branch the
  store apps ship from; check they still apply to main before submitting
  (`git apply --check` in a main checkout).
- **Sign-off (DCO).** Every commit needs `Signed-off-by:` with a real name
  and real email; no pseudonyms. The patch files here carry the GitHub
  noreply identity; whoever submits adds their own sign-off.
- **Commit messages:** a short title (`fix(android): …`, `feat(android): …`
  in the repo's style), then the current state, the problem, and the
  solution.
- **AI policy:** AI tools are allowed, but the submitter must understand
  every hunk and must have tested the result; untested or not-understood
  patches are not accepted. So each entry below records how it was tested,
  and none goes up before it has been tried on a Googlebook.

## Candidate patches

| Patch | What | Applies to main (2026-09-26) | Tested | Status |
| --- | --- | --- | --- | --- |
| 0001 `feat(android): desktop UI on Android PCs, not only on ChromeOS` | `LOActivity.isDesktop()` = ChromeOS or `FEATURE_PC`, used for the UI mode, the web UI's `isChromeOS()` JavaScript interface and the start screen's button | yes | 2026-09-27 on a Googlebook: a .docx opens with the classic menu bar and desktop status bar, no ribbon. Editing not yet tried | candidate |
| 0002 `fix(android): keep documents open when a desktop window is resized` | `smallestScreenSize` and `density` in both activities' configChanges | yes | 2026-09-27: window resized 1382x864 → 731x592 → back (`am task resize`), same process, no restart, document stays open. Display change not tried | candidate |
| 0003 `feat(android): tabbed ribbon on desktops, like the desktop app` | desktops (ChromeOS and Android PCs) ask for the notebookbar, as tablets do; phones keep classic | yes, after 0001 | not yet (build 2) | candidate; changes ChromeOS's default too, which reviewers may want to discuss |
| 0004 `fix(android): no wallpaper-coloured caption bar in desktop windows` | transparent caption bar (API 35+) in both activities, the web UI's background under it in the document window | yes, after 0003 | not yet (build 2) | candidate |

| 0005 `fix(browser): Android app on ChromeOS was never detected as a Chromebook` | `isChromebook()` asked on first use instead of before `ThisIsTheAndroidApp` is set | yes | not yet (build 3) | candidate, standalone; affects ChromeOS today |
| 0006 `feat(browser): the Android app on a PC can be the desktop app` | `isCODesktop()` for the Android app when it opts in; Android exceptions (presenter console, welcome, task workers, Options); `postMobileCall()`; Ctrl+O/Ctrl+N for the Chromebook platform | yes, after 0005 | tsc (no new errors), eslint and prettier's check pass locally; device: not yet | candidate; the direction to agree with Collabora first |
| 0007 `feat(android): answer the desktop app's messages on a PC` | `isCODesktop()`, `postMobileCall()`, GETRECENTDOCS/opendoc/newdoc/Open/SaveAs/TEXTCLIPBOARD/SETDARKMODE/FULLSCREENPRESENTATION/LICENSE in LOActivity, `DesktopDocuments` | yes, after 0006 | not yet | candidate |
| 0008 `feat(android): the desktop app's starter screen on a PC` | `StarterActivity` with the web starter screen; the launcher hands over on a PC | yes, after 0007 | not yet | candidate |

OfficeBook-only (not for upstream): `branding/` (name, icon), passed with
`--with-app-branding`; Collabora ships its own branding. Patch 0009 (the
adb-only WebView debugging switch).

Found, not patched yet:

- **`file://` VIEW intents hang.** LOActivity logs `SCHEME_FILE: getPath()`
  and then only continues when `mTempFile` is set, which happens for
  `content://` URIs; with a `file://` URI the "Preparing…" dialog stays up
  forever. Either load the file directly or finish with an error. (Seen
  from `adb shell am start -d file:///…`; apps rarely send file URIs now,
  so it's low priority.)

Questions to settle before submitting:

- 0001: should FEATURE_PC also get the file picker's ChromeOS workaround
  (no MIME filter)? We kept it ChromeOS-only because Android's own
  picker handles the filter; confirm on the device.
- 0001: the JavaScript interface keeps the name `isChromeOS()`; upstream
  may prefer renaming it (web UI and app together).
- 0004: the colours under the caption are the web UI's palette values,
  copied into Java; upstream may prefer reading them from the page.
- 0002: check that the web UI relays out cleanly on a `density` change
  (moving the window to an external display).

- 0006: whether Collabora wants the Android app on PCs (ChromeOS
  included) to be "the desktop app" in the web UI at all; this is the
  biggest behaviour change in the series. Worth asking on their forum or
  Matrix before submitting.

## Notes for Collabora's Googlebook rollout (not code)

- **What a Googlebook reports.** HP Googlebook 14, Android 17
  (`ro.build.characteristics=desktop`, `ro.hardware=android-desktop`). It
  declares `android.hardware.type.pc` and
  `android.software.freeform_window_management`, but not ChromeOS's
  `org.chromium.arc.device_management`. So every `isChromeOS()` branch in
  the app takes the phone/tablet path, and Collabora Office from Play
  shows the tablet ribbon there (read from the code; the Play build
  wasn't installed on the device we tested).
- **Live resizing.** Android's desktop windowing resizes a window under a
  veil (icon on a plain colour) and lets the app lay out once at the end.
  In this Googlebook's SystemUI, a window resizes live when compat change
  `ENABLE_FLUID_RESIZING` (460405642) is on for its package. It is off by
  default, and Google turns it on for its own apps (Chrome, Gmail, Docs,
  Calendar and others) through the `app_compat_overrides` device config.
  There is no manifest opt-in. Collabora could ask Google to add
  `com.collabora.libreoffice`; the app should also stay open across
  resizes (patch 0002).
- **Building for Android.** The GitHub mirror has no Android CI.
  OfficeBook's workflow builds co-26.04-mobile for arm64 on GitHub-hosted
  runners, with the engine's outputs and ccache cached. Build problems we
  hit are listed below.

## Build problems found

None: co-26.04-mobile at 794af00 built for arm64 as android/README.md
describes, first try (engine 165 minutes on a 4-core GitHub runner).
