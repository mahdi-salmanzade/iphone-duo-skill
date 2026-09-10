# Verification and completion

Build a matrix for the flows identified in [app-discovery.md](app-discovery.md). This is an acceptance-test design guide, not a claim that every simulator can reproduce every behavior.

## Establish what can run

On a Mac with Xcode, these read-only discovery commands help identify the active toolchain and available targets:

```sh
xcode-select -p
xcodebuild -version
xcodebuild -showsdks
xcrun simctl list runtimes -j
xcrun simctl list devices available -j
```

Use the actual project or workspace path and scheme discovered in the repository. Ask Xcode for supported destinations before choosing a device. Follow existing build scripts and package-manager lockfiles. Do not hard-code a Duo simulator name, identifier, runtime version, or undocumented fold command. Xcode 27 replaced Simulator.app with Device Hub, and only Xcode 27.1 or later carries the Duo simulator and the iOS 27.1 SDK; record which Xcode or build image produced the tested binary, because its SDK tier decides what the app can show.

Capture pre-existing build and test failures before edits when practical. Test the current app on a supported target to establish behavior. If the host lacks Xcode, continue source work and portable checks but leave native compilation and device verification unverified.

## Exercise transitions during a task

Select critical and changed flows, then cover the configurations they can encounter. The expected outcomes below are acceptance criteria to test, not assumed platform guarantees.

| Configuration or action | Observable acceptance criterion |
| --- | --- |
| Outer display | Main navigation and actions fit and remain reachable; content is legible. |
| Inner display, portrait and landscape | The layout uses available room without losing hierarchy or access to actions; system bars are horizontal in portrait and on the side in landscape, and both are checked. |
| Partially folded, book-like and tabletop configurations | Important controls and grouped content remain usable around the fold. |
| Camera active on the inner display | The under-display camera region appears only while the camera is active; content moves aside without losing controls. |
| Open and close while viewing a detail | Selection and navigation history survive; Back returns to the expected destination. |
| Resize during text entry | Draft, focus where supported, validation messages, and submit controls remain usable. |
| Split View in both the left and right slot, and further window-size changes | Content follows the app's own bounds, with no dependency on full-screen dimensions; controls sit along the app's outer edge and safe areas keep the neighbor's controls off the content. |
| Present a sheet, menu, or popover, then change configuration | The presentation stays actionable and anchored to the intended context. |
| Scroll, resize, and return | The user keeps a meaningful reading position; content and requests are not duplicated. |
| Background and resume after a transition | Session state remains valid; subscriptions and ongoing work are managed correctly. |

Repeat relevant transitions through populated, loading, empty, and error states. Exercise actual navigation paths, including deep links and notification entry when they lead to changed screens. A collection of static screenshots cannot prove state continuity.

## Accessibility and regression coverage

Check larger text, VoiceOver labels and traversal, touch targets, long localized strings, and right-to-left layout where the app supports it (system side bars stay on the same hardware side in right-to-left languages). Where the app authenticates with biometrics, run the prompt on a target that reports fingerprint rather than face recognition, since the device has a side-button fingerprint sensor. Test keyboard-visible layouts and reduced-motion behavior when animations change. Confirm the user can complete the task, not merely see its first screen.

Run the changed flows on an ordinary supported iPhone. Also check iPad, Android, or web where code is shared. Keep an older supported OS in the matrix when availability branches change. Choose automated regression tests that exercise real constraints or state transitions; do not add tests whose only purpose is to match new source text.

## Optional device-dependent features

For camera, audio/video, multiwindow, or accessory work, extend the matrix only to features in scope. Record capability-unavailable behavior, permission handling, interruptions, resource ownership, and return to the primary flow.

Physical cameras, recording quality, thermal behavior, and real sensor input require appropriate hardware evidence. Simulator results must identify what was simulated. Test mode changes during an active operation where supported, and check that no duplicate sessions or resources remain after closing an auxiliary view.

## Evidence to retain

Record each row as passed, failed, blocked, or not applicable, with the target, OS/runtime, build configuration, exact command or reproduction steps, observed result, and relevant log or screenshot. Use the project's existing test-report location, or include a compact matrix in the handoff. Do not overwrite unrelated reports.

Run relevant checks after the final edit. A missing SDK or inaccessible account leaves a verification gap, even if other tests pass. Distinguish implemented-but-unverified changes from a verified flow, and state the command or manual test that would close each gap.
