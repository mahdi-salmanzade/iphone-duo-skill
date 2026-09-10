# Apple platform reference

Source snapshot checked **2026-09-10**. This is a short research index, not a frozen SDK contract. Open the relevant primary source and inspect installed declarations before writing new API calls. Apple may revise names, availability, and behavior before or after release.

## Availability

Apple's [developer hub](https://developer.apple.com/iphone-duo/) still lists Xcode 27.1 beta and the written guide "Preparing your app for iPhone Duo" as coming later in September 2026. Its six Tech Talks and the [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) Human Interface Guidelines page (added 2026-09-09) are live, and the hub schedules group labs (September 16–17) and SwiftUI, UIKit, and Photos & Camera Q&As (September 23).

As of the check date, none of the new symbols named in the talks (`ReservedRegion`, `ArrangementView`, `UIArrangementViewController`, `UIHingeInteraction`, `AVCaptureDeviceDirectionCoordinator`, `CameraCaptureAccessory`, …) has a page under developer.apple.com/documentation. Every name below is transcribed from a video or the HIG; treat it as unconfirmed until an installed SDK declares it. Recheck this status on each new migration; do not keep treating that dated announcement as the current release status.

## SDK tiers

[Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) describes three outcomes, decided by the SDK that linked the binary:

- Built with a pre-iOS 27 SDK: the app runs unmodified at a familiar iPhone size and aspect ratio.
- Built with the iOS 27 SDK: on the inner display the app extends to the left of the status bar area.
- Built with the iOS 27.1 SDK: content reaches the display edge, standard navigation and toolbar buttons lay out vertically, and the reserved-region APIs become available.

The tier is fixed at build time. No runtime check, plist key, JavaScript change, or over-the-air bundle moves an app between tiers; only a binary produced by an Xcode that carries the wanted SDK does. Xcode 27.1 is the first Xcode with the iOS 27.1 SDK and the Duo simulator.

## Baseline compatibility and layout

- **Size classes.** The outer display follows familiar iPhone size-class behavior (compact width). The inner display is regular in both dimensions in every orientation and does not honor `UISupportedInterfaceOrientations`; base layout on size classes and scene geometry, not orientation or the `phone` idiom. The HIG allows games to lock orientation, but they must still fill the screen in every pose.
- **Screen.** `UIScreen.main` is ambiguous on a two-display device; Apple's documentation marks it deprecated since iOS 26 in favor of `UIWindowScene.screen`, and the talk replaces `UIScreen.main.scale` with `traitCollection.displayScale`.
- **Safe areas.** Insets are asymmetric because system controls sit along one edge (and along each app's outer edge in Split View). Inset each edge independently (`bounds.inset(by: safeAreaInsets)`), never `left * 2`. Keep interactive content inside the safe area; let background artwork extend past it.
- **Standard containers adapt.** `NavigationSplitView` / `UISplitViewController` collapse on the outer display and tile or overlay on the inner one; `TabView` / `UITabBarController`, sheets, popovers, context menus, and alerts reposition around reserved regions. Sidebar placement on the inner display: `.defaultTabBarPlacement(.sidebar)` / `tabBarController.sidebar.preferredPlacement = .sidebar`. Custom content inside these containers still needs inspection.
- **Multitasking.** [Multiple displays and scenes](https://developer.apple.com/videos/play/tech-talks/111464/) says every app participates in Split View on the inner display. Apple documents `UIRequiresFullScreen` as an iPad compatibility key deprecated since iOS 26 (pointing to `UISceneSizeRestrictions` and `prefersInterfaceOrientationLocked`); nothing in the Duo material says it exempts an app from Duo resizing, so treat it as no protection and test at Split View sizes.
- **Testing.** Xcode 27.1's Device Hub adds open, close, rotate, and fold controls for the simulated device. Discover the installed runtime and supported operations rather than inventing simulator command-line flags.

## Product layout

[Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) and the HIG recommend one consistent hierarchy that adapts across sizes: a compact-width layout for the outer display and a regular-width layout for the inner display cover every pose. Don't reinvent the app when it resizes; let the existing layout expand, and show one extra level of hierarchy on the inner display when the content justifies it (Mail shows list or message when closed, both when open). Keep functionality and element state identical across displays and poses; controls may overflow and content may move, but the same actions stay reachable.

The outer display is wider and shorter than any other iPhone display, so the system moves toolbars, tab bars, navigation controls, the status bar, and the Dynamic Island to the side to preserve vertical space. On the inner display the controls stay on the side in landscape and return to horizontal bars in portrait. Sheets get vertical controls on the outer display and horizontal bars on the inner one, and slide aside from the fold when the device is partially folded. Immersive, non-scrolling interfaces may span the full width (Calculator); a background or header can span full width while scrollable content stays inset. A bespoke arrangement must preserve the task and its functionality.

## Bars and overflow

[Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) distinguishes system-container bars from standalone custom bar instances: only bars owned by `NavigationStack` / `NavigationSplitView` / `TabView` or `UINavigationController` / `UITabBarController` participate in the vertical arrangement. Inspect navigation-container ownership before promising automatic adaptation.

- Placement order, top to bottom: primary navigation (Back or Close: `cancellationAction`; UIKit `leftItemsSupplementBackButton = false`), then prominent actions (`topBarPinnedTrailing` / `pinnedTrailingGroup`), then the remaining groups. Items overflow from bottom to top by default; `ToolbarItemVisibilityPriority` / `UIBarButtonItemVisibilityPriority` reorder that, whole groups first.
- Symbol-only items go vertical automatically; text-only items stay in a horizontal bar; custom views default to horizontal-only unless `axisBehavior = .verticalPreferred`; state-transition controls such as Select/Done use `.horizontalOnly`. Always provide a title, even for a symbol item, because overflow menus and expanded forms use it. Prefer `.badge` over inline text.
- Custom views read `\.toolbarVerticalEdge` / `traitCollection.verticalBarEdge` to adapt. Flexible spacers collapse to zero in a vertical bar; group items with `ToolbarItemGroup` / `UIBarButtonItemGroup` instead of fixed spacing.
- Compression: by default toolbar items overflow first and the tab bar stays; `toolbarVerticalCompressionBehavior(.prefersToolbarItems)` / `verticalBarCompressionBehavior = .prefersBarItems` flips that for task-oriented screens. Overflow is triggered on the outer display in landscape and when the keyboard appears. Fold custom overflow into `ToolbarOverflowMenu` / `additionalOverflowItems` and reserve the ellipsis for it.
- Opting out (`toolbarVerticalBehavior(.disabled)` / `preferredVerticalBarBehavior`) is for single-page bottom-heavy layouts or one-control sheets; the HIG says not to override the default placement in general. In right-to-left languages the bar stays on the same hardware side.

## Fold-aware content

The HIG names three reserved regions: the outer front camera (always present; it expands into the Dynamic Island for Live Activities), the inner front camera (present only while the camera is active; it is under the display and invisible otherwise), and the folding region (a division region, active when partially folded and zero width when flat). Their activity and geometry change, so do not hard-code a hinge gap.

[Strike a pose with adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/) queries them with `GeometryProxy.reservedRegions(kind: .division | .occlusion, options: .includeInactive)` in SwiftUI and `UIView.reservedRegions(kind:options:)` in UIKit. Many system components already move: alerts, context menus, and sheets avoid the fold; split views rebalance columns; grids keep outer margins and widen the gap at the hinge (the HIG prefers an even number of columns). Continuously scrolling content is not displaced as one unit. In the book pose alerts move to the trailing side; in the tabletop pose the top region is for viewing and the bottom for interactive controls. Favor small adjustments over rearrangement.

For two related content areas the talk presents `ArrangementView { primary } secondary: { … }` with `.arrangementViewStyle(.split)`, `.split.axes(.horizontal)`, or `.overlay` (plus `\.overlayArrangementZIndex`), and UIKit `UIArrangementViewController` with `setViewController(_:for: .primary / .secondary)`, `updateArrangement(…)`, and `state(for:)`. A split arrangement maps to an existing `HStack` / `VStack`, an overlay to a `ZStack`. Arrangements organize content; they do not replace navigation. Keep navigation containers around, not inside, an arrangement, and never nest an arrangement in a scroll view or list. Retrieve exact signatures from the SDK before implementing.

## Scenes and multiple displays

[Multiple displays and scenes](https://developer.apple.com/videos/play/tech-talks/111464/) separates hinge input for interactions from region and arrangement APIs for layout. SwiftUI `onHingeChange { previous, context in … }` exposes `context.hinge` (nil on a device without a hinge) with a status of closed, partially open, or fully open and a continuous angle; UIKit uses `UIHingeInteraction`. Angle-driven effects are optional product features.

Duo is the first iPhone that can run multiple instances of an app's UI, using the existing multi-scene support (`UIApplicationSupportsMultipleScenes`). New windows cannot be created on the outer display, requests must handle errors, and the `UIWindowSceneActivation` action hides itself when unavailable. Support for multiple app instances and support for a resized single instance are different concerns.

Scene accessories are system-managed and their availability can change; observe it. `CameraCaptureAccessory`, registered with `.sceneAccessory { … }` and `.onAvailabilityChange`, pairs outer-display content (a teleprompter, a preview) with an active camera session while the main app is full screen on the inner display. This is not a promise that arbitrary apps can independently render on both displays at all times.

## Camera apps only

[Build a great camera experience](https://developer.apple.com/videos/play/tech-talks/111465/) describes two front cameras: outer (corner, always visible) and inner (under the display). A front-position `AVCaptureDeviceDiscoverySession` yields a virtual front camera that switches physical cameras automatically with a shared capability set (1080p at 60 fps, no depth). Selecting an individual camera (transcribed device types `.builtInOuterUltraWideCamera`, `.builtInInnerUltraWideCamera`, `.builtInDualWideCamera`) unlocks the outer camera's 4K at 120 fps and depth, and makes the app responsible for switching. Both cameras report position `.front`.

For that path, `AVCaptureDeviceDirectionCoordinator(view:deviceTypes:changeHandler:)` in AVKit is tied to a view and its display, reports which camera faces the user, and hands out `Sendable` `AVCaptureDeviceDescriptor` values so the capture actor can build devices off the main actor; use one coordinator per display when combined with scene accessories. On a change, reconfigure the session, update mirroring (mirror when the rear camera faces the user), and update controls. Preview framing uses `videoGravity` and `AVCaptureDevice.dynamicAspectRatio`; rotation uses `AVCaptureDeviceRotationCoordinator`, after which `isCameraSensorOrientationCompensationEnabled` can be disabled on front cameras. Verify the selected capture format and direction on hardware; a working preview in one pose does not establish recording correctness.

## Hardware facts

Apple's [tech specs](https://www.apple.com/iphone-duo/specs/) list a 7.6-inch inner display (1878×2670 at 430 ppi), a 5.4-inch outer display (1398×2034 at 460 ppi), and a fingerprint sensor built into the side button rather than Face ID. Use these to check cached assumptions (a fixed status-bar height, a "Face ID" string, a hardcoded aspect ratio), not as layout breakpoints or device detection.

## Applying the sources

These sources describe Apple's native frameworks. They do not establish support in any React Native package, Flutter plugin, Expo release, or browser. Verify those layers separately. When documentation, generated video snippets, and installed declarations differ, resolve the discrepancy before committing code. Record the source, availability, and actual compile result for a newly adopted API.
