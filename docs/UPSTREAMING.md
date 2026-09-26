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
| 0001 `feat(android): desktop UI on Android PCs, not only on ChromeOS` | `LOActivity.isDesktop()` = ChromeOS or `FEATURE_PC`, used for the UI mode, the web UI's `isChromeOS()` JavaScript interface and the start screen's button | yes | not yet (first build running) | candidate |
| 0002 `fix(android): keep documents open when a desktop window is resized` | `smallestScreenSize` and `density` in both activities' configChanges | yes | not yet | candidate |

Questions to settle before submitting:

- 0001: should FEATURE_PC also get the file picker's ChromeOS workaround
  (no MIME filter)? We kept it ChromeOS-only because Android's own
  picker handles the filter; confirm on the device.
- 0001: the JavaScript interface keeps the name `isChromeOS()`; upstream
  may prefer renaming it (web UI and app together).
- 0002: check that the web UI relays out cleanly on a `density` change
  (moving the window to an external display).

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

None yet.
