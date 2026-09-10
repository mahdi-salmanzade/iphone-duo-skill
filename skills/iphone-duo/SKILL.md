---
name: iphone-duo
description: Audit and adapt an existing iOS app for iPhone Duo by tracing its architecture, fixing resizing and state continuity, and verifying supported device configurations. Use for Duo compatibility or foldable iPhone migration in SwiftUI, UIKit, React Native, Expo, Flutter, and iOS web wrappers.
license: MIT
metadata:
  author: mahdi-salmanzade
  version: "1.1.0"
---

# iPhone Duo

Make the user's existing app work across iPhone Duo configurations while preserving its product behavior and supported platforms. Understand the app through evidence from its code and runtime. Do not equate a repository scan with complete app understanding or a successful build with device compatibility.

For an implementation request, carry the work through changes and verification. For an audit request, report findings without editing application code. For a targeted bug, trace the affected flow and shared infrastructure; do not expand it into a full migration.

## Establish the app and toolchain

Read the project's instructions and inspect its working-tree changes. Locate the actual iOS app in a monorepo, its build configuration, and the source of generated native files. Follow the project's existing search or code-graph workflow. Exclude dependencies and build output from initial discovery.

Read [app-discovery.md](references/app-discovery.md) to build an app map: entry points, navigation, screens, state ownership, platform integrations, and tests. Attach file or symbol evidence to the map. Inspect the implementations behind routes and shared wrappers, then exercise important flows when the app can run. Identify unknowns that could change the implementation and ask only for missing information that the repository and tools cannot resolve.

Read [apple-platform.md](references/apple-platform.md) before choosing Duo behavior or APIs. Check its source links against current Apple documentation and the actual installed SDK. Record the check date, Xcode version, SDK, simulator runtime, deployment target, and relevant framework versions. For a cross-platform app also record which Xcode or build image produces the shipping binary: the Duo behavior tier is fixed by the SDK that linked it, and no JavaScript, Dart, or over-the-air change moves it. If online documentation is unavailable, label the reference snapshot as dated and limit changes to APIs verified in the available toolchain.

Choose a buildable path:

- With an available SDK, runtime, and framework integration, implement and test the supported Duo behavior.
- Without those prerequisites, complete independently useful app fixes that compile with the existing toolchain. Record the exact blocked work and how to verify it later. Do not introduce fake APIs, guessed device identifiers, speculative plist keys, or unresolved symbols.
- A runtime availability check cannot make an older SDK recognize a new symbol. Check compile-time support separately and retain a working fallback. Preserve the deployment target unless a required change is justified and within the user's scope.

## Turn app knowledge into changes

Create a short working checklist in the project's existing task notes, or keep it in the response when no artifact is needed. Each finding needs a trigger, affected screen and source, user-visible failure, proposed fix, and verification method. Treat search matches as leads; confirm the actual constraint before editing.

Prioritize blocked interactions, lost state, crashes, and inaccessible controls, followed by layout defects and useful enhancements. Work through shared layout and navigation primitives before duplicating fixes across screens. Read [frameworks.md](references/frameworks.md) for the app's implementation stack.

For each affected flow, decide what should happen as its available space changes. Follow existing information hierarchy and design components. Check whether detail content, selection, navigation history, a draft, playback, or a live session belongs above a layout branch. Change presentation without creating a second competing owner of the same task.

Use the evidence in the Apple reference for system behavior. Do not infer a folding state from a model name, an arbitrary width, or an iPad flag. Any product breakpoint should be explained by what the content needs. Avoid forcing every app into two columns or adding a separate screen implementation for every pose.

Treat ordinary compatibility and optional features separately. Add multiwindow, camera accessories, hinge-driven effects, or a native bridge only when they serve an existing flow or the user's explicit request. Enabling them is not a prerequisite for every app.

Scope changes to the migration. Preserve unrelated edits and the existing language, framework, design system, signing configuration, and supported platforms. Follow repository rules for commits and publishing; this skill itself grants no permission to deploy, upload builds, change accounts, or publish a repository.

## Verify the result

Read [validation.md](references/validation.md) and build a matrix from the actual app map. Establish a baseline, run the relevant build and automated checks, then exercise the changed flows through configuration transitions. Capture observable outcomes, including state continuity and accessibility. Add regression coverage where it proves a failure is fixed; static searches alone do not establish correctness.

Classify evidence precisely:

- **Verified on Duo simulator:** name the runtime, configurations, and flows tested.
- **Verified on Duo hardware:** identify the tested hardware and device-dependent features exercised.
- **Verified on another target:** name that target and explain what the check covers.
- **Unverified or blocked:** state the missing tool, access, dependency, or test and its next step.

An iPad, desktop browser, mocked hinge, or manually resized viewport can validate parts of a layout. None proves that Duo display transitions or hardware features work. If a required target is unavailable, complete the available checks and explicitly leave that acceptance criterion open.

## Hand off

Report the app structure relevant to the change, what changed and why, files affected, commands and runtime checks performed, regressions checked, and remaining blockers. Include the Apple sources and verification date for new platform behavior. Distinguish pre-existing failures from regressions caused by the change. Claim only the compatibility level supported by the evidence.
