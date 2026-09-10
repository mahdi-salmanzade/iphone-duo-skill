# Apple platform reference

Source snapshot checked **2026-09-10**. This is a short research index, not a frozen SDK contract. Open the relevant primary source and inspect installed declarations before writing new API calls. Apple may revise names, availability, and behavior before or after release.

## Availability

Apple's [developer hub](https://developer.apple.com/iphone-duo/) currently lists Xcode 27.1 beta and the written preparation guide for later in September 2026. Its videos are already available. Recheck this status on each new migration; do not keep treating that dated announcement as the current release status. The hub also links the [Duo Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo).

## Baseline compatibility and layout

[Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) explains that existing binaries run, while SDK adoption changes available screen usage. Building with the iOS 27.1 SDK lets content extend to the display edges and enables vertical system controls.

The outer display follows familiar iPhone size-class behavior; the inner display is regular in both dimensions. The inner display does not honor supported interface orientations. Base layout on traits and scene geometry. Replace ambiguous main-screen assumptions with the relevant scene or environment. Treat each safe-area edge independently. Standard navigation and presentation containers adapt, but their custom content still needs inspection.

For tests, the talk describes Device Hub controls for opening, closing, rotating, and folding the simulated device. Discover the installed runtime and supported operations rather than inventing simulator command-line flags.

## Product layout

[Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) recommends a consistent hierarchy that adapts across sizes. Extra room can expose existing detail or hierarchy. Side controls conserve vertical content space, and sheets reposition with the device configuration. Keep meaningful controls usable around the fold while retaining a coherent reading experience. A bespoke arrangement should preserve the task and its functionality.

## Bars and overflow

[Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) distinguishes system-container bars from standalone custom bar instances: the latter do not automatically participate in the new arrangement. Inspect navigation-container ownership before promising automatic adaptation.

Custom items need a suitable representation for a narrow vertical bar. Keep accessible titles even when displaying symbols. Test which actions enter overflow when space shrinks or the keyboard appears. Essential actions must remain discoverable. Consult the talk and current SDK for axis, placement, and visibility-priority APIs; only apply them to controls that need those choices.

## Fold-aware content

[Strike a pose with adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/) introduces reserved regions: division regions for the fold and occlusion regions for cameras. Their activity and geometry change, so do not hard-code a hinge gap.

For two related content areas, the talk presents `ArrangementView` and `UIArrangementViewController` with split or overlay arrangements. They organize content; they do not replace navigation infrastructure. Do not put a navigation container inside an arrangement or an arrangement inside a scrollable container. Continuously scrolling content generally should not be displaced as one unit around the hinge. Retrieve exact signatures from the SDK before implementing.

## Scenes and multiple displays

[Multiple displays and scenes](https://developer.apple.com/videos/play/tech-talks/111464/) separates hinge input for interactions from region and arrangement APIs for layout. It presents `onHingeChange` and `UIHingeInteraction`; angle-driven effects are optional product features.

Duo supports side-by-side multitasking. Creating additional app windows is supported on the inner display; requests must handle unavailable configurations and errors. Support for multiple app instances and support for a resized single instance are different concerns.

Scene accessories are system-managed and their availability can change. `CameraCaptureAccessory` is described for supplementary outer-display content during an active camera session, with the main app full screen on the inner display. This is not a promise that arbitrary apps can independently render on both displays at all times.

## Camera apps only

[Build a great camera experience](https://developer.apple.com/videos/play/tech-talks/111465/) describes a virtual front camera that switches physical front cameras automatically, with a shared capability set. Apps selecting individual cameras take responsibility for switching.

For that path, investigate `AVCaptureDeviceDirectionCoordinator` in AVKit and keep camera-session work on its appropriate execution context. The talk uses sendable device descriptors to transfer information from the main-actor coordinator. It also covers preview framing, mirroring, and `AVCaptureDeviceRotationCoordinator` across display changes. Verify the selected capture format and direction on hardware; a working preview in one pose does not establish recording correctness.

## Applying the sources

These sources describe Apple's native frameworks. They do not establish support in any React Native package, Flutter plugin, Expo release, or browser. Verify those layers separately. When documentation, generated video snippets, and installed declarations differ, resolve the discrepancy before committing code. Record the source, availability, and actual compile result for a newly adopted API.
