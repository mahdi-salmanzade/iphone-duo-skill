# Complete Apple documentation and images

The source set centers on Apple's [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo). It contains the complete article, every DocC page linked from its body, and supporting UI guidance and APIs. It is a bounded reference library, not a recursive copy of Apple's developer website.

## Read the sources before changing layout

1. Open the [complete Duo HIG](apple-source/pages/design-human-interface-guidelines-designing-for-iphone-duo.md), including its illustrated outer/inner, folded, split-view, and toolbar examples.
2. Read the [practical design rules](design-rules.md). These distinguish Apple guidance, implementation checks, and product decisions.
3. Use the [complete source index](apple-source/INDEX.md) to open supporting pages and the [image atlas](apple-source/IMAGES.md) to inspect their illustrations. Review the actual images when making visual layout decisions; alt text is not a substitute.
4. Read [apple-platform.md](apple-platform.md) for SDK requirements, API details, and documented conflicts, and [frameworks.md](frameworks.md) for the app's integration limits.

Download the source set before opening the local references. The downloader saves Apple's full text and images under `references/apple-source/` inside the installed skill. These files are excluded from the repository. The download preserves Apple's complete responses; it does not replace them with summaries.

## Coverage and reading order

| Aspect | Complete local reference |
| --- | --- |
| Device anatomy, both displays, cameras, and supported poses | [Duo HIG — Anatomy](apple-source/pages/design-human-interface-guidelines-designing-for-iphone-duo.md#anatomy) |
| Resizing, hierarchy, functional continuity, and conditional game guidance | [Duo HIG — Best practices](apple-source/pages/design-human-interface-guidelines-designing-for-iphone-duo.md#best-practices) |
| Size classes, margins, safe areas, and text-size adaptation | [Layout](apple-source/pages/design-human-interface-guidelines-layout.md), [Preparation guide](apple-source/pages/documentation-technologyoverviews-preparing-your-app-for-iphone-duo.md) |
| Camera occlusions, Dynamic Island, folds, and even grid columns | [Duo HIG — Reserved regions](apple-source/pages/design-human-interface-guidelines-designing-for-iphone-duo.md#reserved-regions), [ReservedRegion](apple-source/pages/documentation-swiftui-reservedregion.md) |
| Collapsing navigation, selection, pane ownership, split and overlay arrangements | [Split views](apple-source/pages/design-human-interface-guidelines-split-views.md), [ArrangementView](apple-source/pages/documentation-swiftui-arrangementview.md), [UIKit arrangement controller](apple-source/pages/documentation-uikit-uiarrangementviewcontroller.md) |
| Side versus horizontal bars; portrait, landscape, Split View, RTL, and asymmetry | [Duo HIG — Vertical controls](apple-source/pages/design-human-interface-guidelines-designing-for-iphone-duo.md#vertical-controls), [Preparation guide](apple-source/pages/documentation-technologyoverviews-preparing-your-app-for-iphone-duo.md) |
| Navigation controls, toolbar groups, symbols, labels, priorities, and overflow | [Toolbars](apple-source/pages/design-human-interface-guidelines-toolbars.md); paired SwiftUI/UIKit APIs in the [index](apple-source/INDEX.md) |
| Destinations, tab state, sidebar behavior, and toolbar/tab compression | [Tab bars](apple-source/pages/design-human-interface-guidelines-tab-bars.md), [Sidebars](apple-source/pages/design-human-interface-guidelines-sidebars.md) |
| Sheet sizing, placement, detents, dismissal, focus, and full-screen alternatives | [Sheets](apple-source/pages/design-human-interface-guidelines-sheets.md), [Modality](apple-source/pages/design-human-interface-guidelines-modality.md), [UISheetPresentationController](apple-source/pages/documentation-uikit-uisheetpresentationcontroller.md) |
| Edge-to-edge backgrounds, inset foreground, scrolling, and scroll-edge effects | [Scroll views](apple-source/pages/design-human-interface-guidelines-scroll-views.md), [backgroundExtensionEffect](apple-source/pages/documentation-swiftui-view-backgroundextensioneffect.md) |
| Search, accessible controls, and content at larger text sizes | [Search fields](apple-source/pages/design-human-interface-guidelines-search-fields.md), [Accessibility](apple-source/pages/design-human-interface-guidelines-accessibility.md) |
| Device Hub, pose changes, rotation, presentations, and state verification | [Device Hub](apple-source/pages/documentation-xcode-device-hub.md), [verification matrix](validation.md) |

The source index lists every downloaded page. Each complete page retains its own links, resources, platform sections, examples, and change log where Apple supplies them. The atlas includes all inline image variants returned by the catalog's DocC pages, with Apple's alt text. Videos, downloadable design kits, and destinations outside the catalog stay linked online; they are not silently presented as downloaded material.

## Fetch or refresh

Run from the installed `iphone-duo` skill directory, using Python 3 with network access:

```sh
python3 scripts/fetch_apple_docs.py
python3 scripts/fetch_apple_docs.py --verify
```

The [source catalog](apple-doc-sources.json) lists the exact pages and why each is included. The script downloads official Markdown and DocC JSON, saves inline illustrations, and creates:

- `apple-source/raw/`: unchanged Apple responses, including available code, declarations, platform metadata, and references.
- `apple-source/pages/`: the complete Markdown with links normalized for local reading.
- `apple-source/assets/`: downloaded illustrations, including supplied light/dark variants.
- `apple-source/INDEX.md` and `IMAGES.md`: the reading index and illustrated atlas.
- `apple-source/manifest.json`: retrieval times, source and response URLs, byte counts, SHA-256 hashes, section coverage, and any failures.

`--verify` checks the catalog, page completeness, image inventory, and saved file hashes without network access. A failed fetch is reported as incomplete. A verified snapshot confirms retrieval integrity, not API availability or application correctness. Check current documentation and the installed SDK before implementation; report the dated snapshot if offline.

## Attribution and distribution

Apple owns the downloaded text and illustrations; their original notices and [Apple site terms](https://www.apple.com/legal/internet-services/terms/site.html) apply. The source cache is excluded from Git and the skill's MIT license. The repository distributes the source catalog, downloader, and independently written guidance. Fetching after installation recreates the complete local reference library inside the skill.
