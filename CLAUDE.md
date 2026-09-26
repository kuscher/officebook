# OfficeBook

Collabora Office's Android app for the HP Googlebook 14, with the desktop UI.
There is no app source here: UPSTREAM pins a commit of the Collabora Online
monorepo (online code, browser UI, and the LibreOffice-based engine under
engine/), patches/ holds the changes, and GitHub Actions
(.github/workflows/build.yml) builds the APK, because the engine needs the
NDK's x86_64 toolchain. Read docs/DESIGN.md.

## Commands

```sh
./ob ci | wait | fetch        # build in Actions, download and sign the APK
./ob install | start | stop | logs [N] | crash | shot FILE
./ob open FILE                # a document into Download/, opened in the app
./ob share                    # the APK to the Googlebook's Download folder
./ob live-resize [on|off|status]
```

adb comes from VSCodeBook's setup; its server runs on a Unix socket. Never
start it on TCP 5037.

## Changing the patches

Work in a checkout at UPSTREAM's commit (~/.cache/officebook/co, branch
`officebook`), commit there, then regenerate:

```sh
rm patches/*.patch
git -C ~/.cache/officebook/co format-patch <ONLINE_COMMIT>..officebook -o ~/officebook/patches/
```

A patch touching engine/ invalidates the cached engine (hours of CI); keep
engine changes rare and batch them.

## Upstreaming

The user wants changes that would help Collabora on Googlebooks offered
upstream eventually. Every patch gets a row in docs/UPSTREAMING.md: upstream
candidate or OfficeBook-only, whether it applies to Collabora's main, and how
it was tested. Write candidates the way Collabora wants them (subject
`fix(android): …`, message with current state, problem, solution; see that
file). Device facts that matter to Collabora's Googlebook rollout go in its
notes section. Nothing is submitted to Collabora's Gerrit without the user:
it needs their sign-off (real name and email).

## Rules

- **Public repo.** Nothing secret goes in git: the signing key and its password
  (keystore.jks, keystore.pass, gitignored; a copy is in ~/.config/officebook),
  no personal email (patches use the GitHub noreply identity). Docs-only
  commits get `[skip ci]`.
- **Don't inject Android input.** Pickers, installs and permission dialogs
  belong to the user.
- **Kill processes by PID**, not `pkill -f`.
- **Each shared APK bumps** VERSION_CODE in VERSION. Keep keystore.jks:
  updates must be signed with it.
- **Clean up test files** `./ob open` puts in Download/.
- **Ask before outward-facing steps** (releases, sharing, patches upstream).
