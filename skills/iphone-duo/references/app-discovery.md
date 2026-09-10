# App discovery

Use this to understand the product paths that the migration can affect. Scale the depth to the user's request; do not read an entire backend to change a screen's layout.

## Identify the runnable product

Locate app targets and schemes, manifests and lockfiles, native entry points, environment setup instructions, and CI build commands. Resolve which configuration is used by the shipping app. In a monorepo, distinguish the mobile client from a website, backend, extensions, and examples.

Determine whether native files are maintained source, generated output, or a mix. Record framework and navigation-library versions from the lockfile. Look for checked-in documentation or scripts that explain how developers actually start and test the app. Inspect configuration names and references without dumping secret values.

For native projects, inspect the app/scene delegate or SwiftUI App, scene definitions, target settings, and presentation roots. For cross-platform projects, inspect both the shared app entry and iOS host; a JavaScript or Dart fix may still depend on native behavior.

## Trace behavior, not just files

Build a compact map with columns such as:

| Flow or screen | Entry and presentation | State owner | Layout dependencies | Platform dependency | Evidence |
| --- | --- | --- | --- | --- | --- |

Populate it from the app. Include user journeys reachable through onboarding, authentication, tabs, deep links, notifications, and modal presentation when those paths exist. Trace a primary action through its view, state update, side effect, and return path. Locate shared design components and whether screens override their layout behavior.

For a full migration, enumerate all user-facing destinations. Group screens only when they share the relevant implementation; inspect exceptions separately. Mark each destination as inspected, exercised, or inaccessible so the scope of the app map is reviewable. For a targeted fix, record the affected destinations and shared callers instead.

Map loading, empty, error, and populated states; a layout that works with short sample data may fail with real content. Note forms, editors, lists, media, maps, scanning, purchases, or live connections only where the product contains them. Read backend contracts only when a presentation change can affect requests, session identity, or data integrity.

For state continuity, identify navigation paths, selected item IDs, scroll anchors, drafts, focus, playback position, subscriptions, and active tasks. Check view identities and lifecycle callbacks around adaptive branches. A hidden second rendering can still start network requests, consume a camera, or subscribe twice.

## Investigate likely constraints

Search narrowly after orientation from the project map. Useful leads include cached display measurements, device-name checks, phone/tablet branches, orientation locks, fixed root frames, custom navigation bars, full-screen modals, global windows, and native plugins.

Do not mechanically replace every numeric width or device check. A thumbnail size can be intentional; a fixed content width inside a scrolling container can be valid. Confirm which constraint causes an observed failure and which users depend on it.

Read callers before changing a shared primitive. Record existing iPad, Android, and web behavior if those platforms share the affected code. Follow the current design language rather than importing a new component library to solve the migration.

## Resolve uncertainty

Run the app with the documented development setup when available. Use test accounts, fixtures, or previews already provided. Missing credentials can block one flow without blocking layout work elsewhere. Mark inaccessible flows explicitly; do not silently treat them as covered.

Before implementation, be able to explain which code owns the affected screen, what the user is doing during a transition, which state must survive, and how the result can be observed. Keep file references and unknowns alongside findings so another developer can review the reasoning.
