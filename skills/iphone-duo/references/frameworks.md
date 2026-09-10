# Implementation by framework

Read the section matching the repository. These are migration approaches; only the linked Apple reference establishes Duo-specific native behavior. Check dependency versions and their official documentation before choosing APIs or upgrades.

## SwiftUI and UIKit

Trace the scene root and existing navigation containers before changing presentation. Read the layout, bars, and fold-aware sections of [apple-platform.md](apple-platform.md) for the platform rules and new symbols.

Keep selection, drafts, and navigation identity in the existing model layer when swapping adaptive presentations. Inspect whether conditional roots reconstruct a model or repeat work. In UIKit, trace containment and constraints when a controller changes size; check custom views and embedded hosting controllers as well as the root.

Prefer a fix in the existing shared component over introducing a second app shell. If the app uses custom navigation for a product reason, adapt it deliberately and verify all actions. Do not promise the native system's new bar behavior merely because a view resembles a tab bar.

Check both local and CI compilers before adopting new SDK symbols. A supported deployment target is separate from the SDK used to build. Keep older-device behavior testable, and do not make upgrading the whole project the first step when an existing API solves the defect.

## React Native and Expo

Apple's Duo behavior is decided in the native layer; JavaScript only sees its results. Map each Apple rule in [apple-platform.md](apple-platform.md) to the layer that owns it before editing.

The SDK tier is a build decision. For EAS Build it is set by the `image` in `eas.json` (or the `auto` alias); on 2026-09-10 the `latest` / `sdk-57` image shipped Xcode 26.6, so no EAS build reaches the iOS 27.1 tier until Apple releases Xcode 27.1 and Expo publishes an image carrying it. Check [Expo's build infrastructure page](https://docs.expo.dev/build-reference/infrastructure/) and the "Spin up build environment" section of the build log. Local `npx expo run:ios` uses the installed Xcode; Expo Go and an existing development client keep whatever SDK built them. An EAS Update never changes the tier. Record the tier the shipping binary actually has and claim no edge-to-edge layout or vertical bars beyond it.

The orientation lock does not constrain the inner display. `orientation: "portrait"` in app config writes `UISupportedInterfaceOrientations`, which Apple says the inner display does not honor, so a "portrait-only" app must still lay out regular-width, landscape-shaped windows there; `expo-screen-orientation` `lockAsync` cannot hold a size on that display either. `ios.requireFullScreen` writes `UIRequiresFullScreen`, an iPad compatibility key Apple deprecated in iOS 26; Apple's Duo material says every app participates in Split View, so treat it as no protection and test at Split View sizes.

Use the window, not the screen. React Native fills `Dimensions.get('screen')` and both `scale` values from `UIScreen.mainScreen`, which Apple calls ambiguous on a two-display device and deprecated in iOS 26 (verified in `RCTDeviceInfo.mm` of React Native 0.86). `Dimensions.get('window')` and [`useWindowDimensions`](https://reactnative.dev/docs/usewindowdimensions) read the key window's bounds and update on frame changes, including Split View resizes. Replace `screen`-based layout math and cached module-level `Dimensions.get(...)` values with live window values, and measure a column, modal, or pane through `onLayout` instead of treating the whole window as available space. The generated `AppDelegate.swift` in current Expo prebuild output creates its window with `UIScreen.main.bounds`; leave it alone unless the Duo simulator shows a wrong frame, and then fix it through the template or a config plugin, never by editing generated files.

JavaScript has no size-class API. `Platform.isPad` and `expo-device` `deviceType` report the idiom, which Apple says not to use; the inner display is regular in both size classes while the idiom stays phone. Derive layout from the measured width of the container with breakpoints explained by content. If a native size-class or reserved-region signal is truly needed, expose it through a small Expo Module and keep a JavaScript fallback.

Treat safe-area insets per edge. Apple's insets are asymmetric because controls sit along one edge, and along each app's outer edge in Split View. `react-native-safe-area-context` reports `top`, `right`, `bottom`, and `left` from the window's `safeAreaInsets`, so per-edge use is correct; audit for `insets.left * 2`, hardcoded status-bar heights, `StatusBar.currentHeight`, and React Native's core `SafeAreaView`. [Expo's safe areas guide](https://docs.expo.dev/develop/user-interface/safe-areas/) documents the provider and hook; Expo Router installs the provider.

Native containers may adapt; JavaScript bars will not. Apple's vertical-bar behavior belongs to `UINavigationController` and `UITabBarController` in a binary built with the 27.1 SDK. In Expo those are the `react-native-screens` native stack headers and Expo Router's `NativeTabs` (`expo-router/unstable-native-tabs`, a `UITabBarController` host); whether they receive the side placement depends on the SDK tier and on the installed `react-native-screens`, so verify on the Duo simulator rather than promising it. React Navigation's JavaScript tabs and custom headers stay where they are drawn: on the outer display that keeps a horizontal bar consuming the vertical space Apple's guidance protects, and no plist key changes that. `headerLeft` / `headerRight` elements are custom views inside a UIKit bar, which Apple says default to horizontal-only and may overflow; test them. Do not build a JavaScript imitation of the system's side bar.

Multiple windows are out of scope unless the native app already supports scenes. Expo's prebuild output uses a single `UIWindow` and no scene manifest, and Apple's multi-instance support requires `UIApplicationSupportsMultipleScenes`; treat "open in a new window" as a native feature request, not a migration item.

Reserved regions, arrangements, and the hinge are native-only. No Expo or React Native package exposes `reservedRegions`, `ArrangementView`, or `UIHingeInteraction`, and ordinary resizing needs none of them. When a flow needs one (for example keeping a composer clear of the fold), write a narrowly scoped Expo Module in Swift, guard it with `#available` and compile it only where the 27.1 SDK exists, ship any Info.plist or build-setting change through a config plugin, and keep the JavaScript fallback working on older SDKs. Do not fabricate JavaScript APIs or add a bridge for ordinary resizing alone.

Check camera and biometric assumptions. `expo-camera` picks devices through front and back `AVCaptureDevice.DiscoverySession`s and prefers the built-in wide-angle front camera; Apple says a front-position discovery yields the virtual front camera that follows the device pose, so `facing="front"` should switch automatically, but verify on hardware, since the talk names device types no Expo release enumerates yet and a correct preview in one pose does not prove the other. Apple's specs list a fingerprint sensor in the side button rather than Face ID: branch on `expo-local-authentication` `supportedAuthenticationTypesAsync()` instead of hardcoding "Face ID" copy, and keep the `NSFaceIDUsageDescription` (`faceIDPermission`) for Face ID devices.

For Expo, determine whether the native project is generated or maintained manually. [Expo's Continuous Native Generation guide](https://docs.expo.dev/workflow/continuous-native-generation/) explains that prebuild can replace manual native edits, and since SDK 57 `npx expo prebuild` cleans by default (`--no-clean` restores the additive behavior). In generated projects, use supported configuration or a config plugin for persistent native changes. Do not run a prebuild over unrelated native work.

Inspect the development-client or production build path. JavaScript checks and Expo Go do not prove that a custom native integration compiles in the shipping app or that the binary is on the wanted SDK tier. Expo CLI supports Xcode 27's Device Hub (from `@expo/cli` 56.1.16), so once Xcode 27.1 is installed the Duo simulator is an ordinary `npx expo run:ios` destination; discover it, do not hard-code it.

## Flutter

Flutter's [adaptive-app guidance](https://docs.flutter.dev/ui/adaptive-responsive/general) distinguishes available window size from local layout constraints. Use `MediaQuery.sizeOf` or `LayoutBuilder` according to the space the widget actually owns. Review the project's breakpoints, inherited media data, navigation, and state before changing layout branches.

Preserve selected routes, scroll controllers, text controllers, and ongoing tasks across rebuilds. Check safe-area and keyboard handling in both the widget tree and iOS host. A global width can be wrong inside a nested navigator or constrained pane.

Do not assume Android folding features or a plugin's posture API is implemented for iPhone Duo. Confirm support in the installed Flutter engine and plugin code or official release notes. If a native bridge is needed, verify its Swift side against Apple's SDK and keep unavailable capabilities explicit. Run analysis, relevant widget tests, and a real iOS build.

## Web, PWA, Capacitor, and other web wrappers

First distinguish Safari from a native web view and identify which layer owns navigation, keyboard adjustment, and insets. Fix layout against the actual container. Inspect fixed overlays and the composer or form while the keyboard opens and the viewport resizes.

CSS [`env()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env) provides environment values including safe-area insets and documents viewport-segment variables. Their existence in CSS documentation does not prove support in the user's Safari or embedded engine. Check compatibility for the actual browser version and feature before using it, and retain a usable layout when a value or feature is unavailable.

Do not infer hinge support from ordinary viewport resizing or a successful CSS parser check. A wrapper may need a verified native integration for platform-only behavior. Test inside the built iOS wrapper when that is the delivered product; desktop browser checks cover only part of the result.
