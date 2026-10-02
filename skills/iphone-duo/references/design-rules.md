# iPhone Duo design rules

Checked **2026-10-02** against Apple's written guidance and linked APIs. This practical interpretation does not establish app or framework compatibility. See [apple-platform.md](apple-platform.md) for toolchain prerequisites and documentation conflicts, and [apple-docs.md](apple-docs.md) for the complete local source and image catalog.

## Layout follows the containing view

**Apple guidance:** adapt the existing information hierarchy to available space. Base layout on the scene or containing view's bounds, size classes, margins, and safe areas. Device idiom and orientation do not describe usable space. Avoid fixed iPhone dimensions and a separate screen implementation for every pose. Wider layouts can expose more content while retaining the same functions and state. [Preparation: layout and resizing](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations), [Layout: size classes](https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes).

**Implementation checks:** calculate sheets and panes from their own bounds. Keep selections, drafts, navigation history, and active tasks outside replaceable layout branches. Resizing should not restart a task. Do not classify a fold from a model name or assume the display width belongs to a modal.

Preserve each tab's navigation and selection state when switching sections or adapting the layout. [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars#Discussion).

Native containers provide adaptation when the app actually uses them. A React Native `View`, custom JavaScript tab rail, or animated overlay does not automatically acquire reserved-region handling, native overflow, or adaptive sheet placement.

## Safe edges and interior regions are different

A safe area describes clearance from obscured window edges. Layout margins provide alignment and breathing room; they are not another hardware exclusion zone. Apply each physical edge independently and verify the coordinate space used. [Layout: guides and safe areas](https://developer.apple.com/design/human-interface-guidelines/layout#Guides-and-safe-areas).

Duo also has interior reserved regions: the outer camera is always present and can expand for Live Activities; the inner camera region becomes relevant while its camera is active; a partially folded inner display has a division region. Safe-area padding alone cannot represent every interior obstruction. [Duo HIG: reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions).

Query regions in the affected view's coordinate space. Distinguish occlusions from divisions and inspect `isActive`, frames, and margins. Verify query options and default filtering in the SDK: the written prose and option documentation differ about inactive regions. SwiftUI's default layout-direction behavior mirrors coordinates; `.fixed` preserves physical coordinates. Avoid double mirroring. [GeometryProxy.reservedRegions](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)), [documented discrepancy](apple-platform.md#Fold-aware-content).

**Implementation checks:** refresh geometry when bounds, regions, or presentation change. Do not retain a transient top inset after bars move to a side, reuse the host window's side clearance inside a differently positioned sheet, or invent a constant hinge gutter. Measure the actual overlap before applying clearance. For grids, Apple prefers an even column count so items divide cleanly around a fold; adjust to the actual usable regions. [Duo HIG: reserved regions](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Reserved-regions).

## Bar location and horizontal alignment

The default Duo pattern places system and app bars on the side, except on the inner display in portrait. In Split View, each app's controls occupy its outer edge; the left app therefore has controls on the left. The hardware-aligned position does not reverse simply because text direction changes. [Duo HIG: vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls).

| Context | Documented bar arrangement |
| --- | --- |
| Outer display | Vertical controls along the hardware-aligned side |
| Inner landscape | Vertical controls |
| Inner portrait | Standard horizontal bars |
| Split-view sidebar or content column | Horizontal |
| Split-view detail column | Vertical |
| Inspector | Horizontal |
| Outer-display sheet | Vertical by default |
| Inner centered or leading sheet | Horizontal |
| Inner trailing sheet | Vertical |

The container-specific rows come from [Preparation: vertical presentation](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Optimize-bars-for-vertical-presentation). Verify the actual container rather than applying the outer-display rule to every nested view.

**Product decision:** centering within the safe area and centering on the physical display differ when clearance is asymmetric. Apple advises using safe areas to accommodate asymmetry; equal left and right padding is a product choice. For a physically centered capped column, preserve clearance on both sides and align headings, search, cards, and shelves consistently. Narrow panes may favor usable width. Keep the column within real safe bounds.

## Foreground and backgrounds

Keep tappable controls and important foreground information clear of obscured regions. Background artwork can extend behind bars; extending a background does not authorize moving buttons into the same area. Apple's background-extension effect duplicates and blurs a background beyond its bounds and should be used selectively. [backgroundExtensionEffect](https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect()).

**Product decision:** edge-to-edge backgrounds can coexist with inset scrolling content. Progressive blur is not a blanket Duo requirement. Custom backgrounds must preserve readability and system effects. [Toolbars: best practices](https://developer.apple.com/design/human-interface-guidelines/toolbars#Best-practices).

Apple prefers the automatic scroll-edge effect when scrolling content sits behind floating controls. Use one effect per view, with consistent heights across split panes; avoid decorative effects where nothing scrolls beneath the header. Test legibility before choosing a soft effect. [Scroll views: scroll-edge effects](https://developer.apple.com/design/human-interface-guidelines/scroll-views#Scroll-edge-effects).

Immersive, non-scrolling interfaces can use the full width while avoiding system regions. Games may lock orientation, but must remain playable through pose changes; prefer adapting the aspect ratio, and fill unavoidable letterboxing with artwork. These are conditional exceptions, not a reason to make every screen immersive. [Duo HIG: best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices).

## Toolbar hierarchy, grouping, and overflow

In a vertical bar, primary navigation such as Back or Close comes first, followed by a prominent action such as Done. Keep remaining related actions grouped. Locate pane-specific controls near the content they affect. Prefer semantic toolbar groups to hand-inserted fixed spacing. [Preparation: organize bar items](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Organize-items-in-your-bars).

Provide a recognizable symbol and meaningful title so an action can adapt between a vertical icon, horizontal control, and overflow entry. Text-only or custom-view items do not automatically become vertical controls. Check axis eligibility; an essential horizontal-only item needs a reachable presentation when no horizontal bar exists. [axisBehavior](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:)).

Vertical items overflow from bottom to top by default. Lower visibility priorities overflow before higher ones. Preserve frequent actions and useful status indicators; use the system overflow menu and reserve the ellipsis for overflow. [visibilityPriority](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)), [Duo HIG: vertical controls](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Vertical-controls).

Choose compression according to the task: navigation-focused views favor destination access; task-focused views may favor toolbar actions over tabs. [toolbarVerticalCompressionBehavior](https://developer.apple.com/documentation/swiftui/view/toolbarverticalcompressionbehavior(_:)). Use concise, contextual titles and recognizable Back/Close behavior. A title should identify the current content, rather than repeat the app name. [Toolbars: titles and navigation](https://developer.apple.com/design/human-interface-guidelines/toolbars#Titles).

## Split content without duplicating navigation

A standard split view collapses on the outer display and expands on the inner display. Arrangement views instead organize primary and secondary content: split arrangements adapt the axis; overlay arrangements can separate layered content around a fold. They are layout containers, not navigation owners. [Duo HIG: split views](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Split-views), [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview).

**Product decision:** equal halves can suit two equally important panes. They are not a universal Apple requirement; Apple's examples also use unequal widths when fully open. Decide pane proportions from content needs and active regions, and avoid large rearrangements during small fold changes.

**Composition caveat:** the HIG keeps navigation outside arrangement views, while the preparation guide warns against nesting an arrangement view inside a navigation split view, list, or scroll view. Do not infer that every outer-container combination is supported. Check the intended composition against the SDK and runtime. [Duo HIG: arrangement views](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views), [Preparation: arrangements](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Arrange-views-in-different-poses).

## Sheets follow the task and presentation bounds

Use a sheet for a focused task related to the current context. Prefer page/form sheets on iPadOS; full-screen presentation can suit media or a prolonged editing task. Medium detents can disclose additional content progressively, but compose tasks may need the full available height. A resizable sheet needs a grabber and usable dismissal behavior. [Sheets: best practices and iOS/iPadOS](https://developer.apple.com/design/human-interface-guidelines/sheets#iOS-iPadOS).

Sheet placement defaults to automatic. SwiftUI's `presentationPlacement` requests leading or trailing placement; only sheet presentations respect it. Placement also affects Duo bar arrangement, as listed above. [presentationPlacement](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)).

**Product decision:** choose a bounded width or a pane-filling presentation based on the task and actual container. The reviewed Apple sources prescribe no universal numeric Duo sheet maximum width. A medium detent concerns height; it is not a half-width rule. Verify keyboard space, scrolling, and safe clearance inside the presented sheet.

Provide a clear exit and distinguish Back from dismissal. Retain drafts through layout changes; confirm when dismissal would discard work. Avoid stacked modal tasks that obscure the return path. [Modality: best practices](https://developer.apple.com/design/human-interface-guidelines/modality#Best-practices).

## Verify transitions, not just screenshots

Apple recommends checking every view, sheet, and popover while opening, folding, closing, and rotating. [Preparation: resizing checks](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo#Address-common-layout-and-resizing-considerations).

**Practical QA:** exercise outer, fully open, partially folded, tall/wide, both rotations, and both Split View sides where supported. Repeat transitions with scrolled content, a draft, keyboard, selection, open presentation, and camera or Live Activity region changes. Check controls remain reachable, important foreground avoids active reserved regions, backgrounds stay continuous, and state survives. Include large text and right-to-left layouts. Record simulator versus hardware evidence, linked SDK, and untested behavior; source review and a successful build are not device verification.

Use [Apple Design Resources](https://developer.apple.com/design/resources/#ios-apps) for official assets and [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) when preparing store images. Neither replaces runtime layout checks.
