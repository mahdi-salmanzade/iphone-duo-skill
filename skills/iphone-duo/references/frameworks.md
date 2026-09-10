# Implementation by framework

Read the section matching the repository. These are migration approaches; only the linked Apple reference establishes Duo-specific native behavior. Check dependency versions and their official documentation before choosing APIs or upgrades.

## SwiftUI and UIKit

Trace the scene root and existing navigation containers before changing presentation. Read the layout, bars, and fold-aware sections of [apple-platform.md](apple-platform.md) for the platform rules and new symbols.

Keep selection, drafts, and navigation identity in the existing model layer when swapping adaptive presentations. Inspect whether conditional roots reconstruct a model or repeat work. In UIKit, trace containment and constraints when a controller changes size; check custom views and embedded hosting controllers as well as the root.

Prefer a fix in the existing shared component over introducing a second app shell. If the app uses custom navigation for a product reason, adapt it deliberately and verify all actions. Do not promise the native system's new bar behavior merely because a view resembles a tab bar.

Check both local and CI compilers before adopting new SDK symbols. A supported deployment target is separate from the SDK used to build. Keep older-device behavior testable, and do not make upgrading the whole project the first step when an existing API solves the defect.

## React Native and Expo

React Native's [`useWindowDimensions`](https://reactnative.dev/docs/usewindowdimensions) updates with window and font-scale changes. Compare its live values with any cached `Dimensions.get(...)` values. For a component living in a column or modal, measure the actual parent through the app's layout mechanism instead of treating the whole window as available space.

Trace the navigation library, screen package, safe-area provider, and keyboard behavior through the iOS host. Review installed versions and native release notes. JavaScript-rendered bars do not acquire UIKit behavior automatically. Avoid using a tablet flag as a substitute for content constraints, and preserve Android behavior in shared components.

For Expo, determine whether the native project is generated or maintained manually. [Expo's Continuous Native Generation guide](https://docs.expo.dev/workflow/continuous-native-generation/) explains that clean prebuild can replace manual native edits. In generated projects, use supported configuration or a config plugin for persistent native changes. Do not run a clean prebuild over unrelated native work.

Inspect the development-client or production build path. JavaScript checks and Expo Go do not prove that a custom native integration compiles in the shipping app. If required Duo APIs are not exposed by the installed packages, assess a supported update or a narrowly scoped native module; do not fabricate JavaScript APIs or add a bridge for ordinary resizing alone.

## Flutter

Flutter's [adaptive-app guidance](https://docs.flutter.dev/ui/adaptive-responsive/general) distinguishes available window size from local layout constraints. Use `MediaQuery.sizeOf` or `LayoutBuilder` according to the space the widget actually owns. Review the project's breakpoints, inherited media data, navigation, and state before changing layout branches.

Preserve selected routes, scroll controllers, text controllers, and ongoing tasks across rebuilds. Check safe-area and keyboard handling in both the widget tree and iOS host. A global width can be wrong inside a nested navigator or constrained pane.

Do not assume Android folding features or a plugin's posture API is implemented for iPhone Duo. Confirm support in the installed Flutter engine and plugin code or official release notes. If a native bridge is needed, verify its Swift side against Apple's SDK and keep unavailable capabilities explicit. Run analysis, relevant widget tests, and a real iOS build.

## Web, PWA, Capacitor, and other web wrappers

First distinguish Safari from a native web view and identify which layer owns navigation, keyboard adjustment, and insets. Fix layout against the actual container. Inspect fixed overlays and the composer or form while the keyboard opens and the viewport resizes.

CSS [`env()`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/env) provides environment values including safe-area insets and documents viewport-segment variables. Their existence in CSS documentation does not prove support in the user's Safari or embedded engine. Check compatibility for the actual browser version and feature before using it, and retain a usable layout when a value or feature is unavailable.

Do not infer hinge support from ordinary viewport resizing or a successful CSS parser check. A wrapper may need a verified native integration for platform-only behavior. Test inside the built iOS wrapper when that is the delivered product; desktop browser checks cover only part of the result.
