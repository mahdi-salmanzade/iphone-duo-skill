#!/usr/bin/env python3
"""Download Apple’s complete DocC pages and verify the local source snapshot."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


SKILL = Path(__file__).resolve().parents[1]
CATALOG = SKILL / "references/apple-doc-sources.json"
CACHE = SKILL / "references/apple-source"
ORIGIN = "https://developer.apple.com"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def asset_url(url):
    # DocC's /images references are served below /tutorials, not the site root.
    if url.lstrip("/").startswith(("images/", "videos/")):
        return ORIGIN + "/tutorials/" + url.lstrip("/")
    return urljoin(ORIGIN, url)


def download(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "iphone-duo-skill-doc-fetch/1.3"}), timeout=40) as response:
                data = response.read()
                if not data:
                    raise ValueError(f"Empty response: {url}")
                return data, response.geturl(), response.headers.get("Content-Type", "")
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def save(relative, data, source_url, fetched_url, content_type):
    path = CACHE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)
    return {
        "path": relative, "source_url": source_url, "response_url": fetched_url,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "bytes": len(data), "sha256": digest(data), "content_type": content_type,
    }


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def fetch_page(page):
    endpoint = ORIGIN + "/tutorials/data" + urlsplit(page["url"]).path
    files = []
    for extension in ("json", "md"):
        url = endpoint + "." + extension
        data, final, content_type = download(url)
        if extension == "json":
            document = json.loads(data)
            if not document.get("metadata", {}).get("title"):
                raise ValueError(f"Not a DocC document: {url}")
        else:
            markdown = data.decode("utf-8")
            if not re.search(r"^# .+", markdown, re.M) or "<html" in markdown[:300].lower():
                raise ValueError(f"Not a complete Markdown document: {url}")
        files.append(save(f"raw/{page['id']}.{extension}", data, url, final, content_type))
    headings = [
        {"level": node["level"], "text": node["text"], "anchor": node.get("anchor")}
        for section in document.get("primaryContentSections", [])
        for node in walk(section) if node.get("type") == "heading"
    ]
    return {**page, "title": document["metadata"]["title"], "files": files, "headings": headings}, document, markdown


def image_ids(document):
    nodes = list(walk(document.get("primaryContentSections", [])))
    used = {node["identifier"] for node in nodes if node.get("type") == "image"}
    for node in nodes:
        if node.get("type") == "video":
            poster = document.get("references", {}).get(node.get("identifier"), {}).get("poster")
            if poster:
                used.add(poster)
    return used


def image_sources(documents, asset_pages):
    urls = set()
    for page_id in asset_pages:
        document = documents.get(page_id, {})
        for identifier in image_ids(document):
            for variant in document.get("references", {}).get(identifier, {}).get("variants", []):
                urls.add(asset_url(variant["url"]))
    return sorted(urls)


def fetch_image(url):
    data, final, content_type = download(url)
    if not content_type.startswith("image/"):
        raise ValueError(f"Not an image: {url}")
    filename = digest(url.encode())[:12] + "-" + Path(urlsplit(url).path).name
    return save("assets/" + filename, data, url, final, content_type)


def readable_markdown(page, document, markdown, pages_by_url, assets):
    references = document.get("references", {})

    def target(url):
        absolute = asset_url(url) if url.lstrip("/").startswith(("images/", "videos/")) else urljoin(ORIGIN + "/", url)
        parts = urlsplit(absolute)
        base = absolute.split("#")[0].lower().rstrip("/")
        if base in pages_by_url:
            suffix = "#" + parts.fragment.lower() if parts.fragment else ""
            return pages_by_url[base] + ".md" + suffix
        if absolute in assets:
            return "../" + assets[absolute]
        return absolute

    def doc_link(match):
        identifier = match.group(1)
        reference = references.get(identifier, {})
        url = reference.get("url")
        if not url:
            url = "/" + identifier.split("/", 3)[-1]
        label = reference.get("title", url.rsplit("/", 1)[-1])
        return f"[{label}]({target(url)})"

    # Preserve Apple’s downloaded originals in raw/. Only normalize links here.
    markdown = re.sub(r"<(doc://[^>]+)>", doc_link, markdown)
    markdown = re.sub(r"\]\((/?(?:images/|videos/|design/|documentation/)[^\s)]+)\)",
                      lambda match: "](" + target(match.group(1)) + ")", markdown)
    markdown = re.sub(r"(!\[[^\n]*?\]\()([A-Za-z][A-Za-z0-9+.-]*://[^\s)]+)(\))",
                      lambda match: match.group(1) + target(match.group(2)) + match.group(3), markdown)
    note = (f"> Apple source snapshot. [Original page]({page['url']}). "
            "Downloaded text; links normalized for local reading. "
            "Apple’s copyright and terms apply. See ../manifest.json for retrieval times and hashes.\n\n")
    return note + markdown


def verify(catalog):
    manifest_path = CACHE / "manifest.json"
    if not manifest_path.exists():
        raise ValueError("No local snapshot. Run this script without --verify first.")
    manifest = json.loads(manifest_path.read_text())
    failures = list(manifest.get("failures", []))
    if manifest.get("catalog_sha256") != digest(CATALOG.read_bytes()):
        failures.append("Source catalog changed; refresh the snapshot.")
    expected = {page["id"] for page in catalog["pages"]}
    actual = {page["id"] for page in manifest["pages"]}
    if expected != actual:
        failures.append(f"Missing/extra pages: {sorted(expected ^ actual)}")
    documents = {}
    for page in manifest["pages"]:
        path = CACHE / f"raw/{page['id']}.json"
        if path.is_file():
            try:
                documents[page["id"]] = json.loads(path.read_text())
            except (OSError, ValueError) as error:
                failures.append(f"Unreadable DocC source {path}: {error}")
    expected_images = set(image_sources(documents, catalog["asset_pages"]))
    actual_images = {entry["source_url"] for entry in manifest["assets"]}
    if expected_images != actual_images:
        failures.append(f"Missing/extra illustrations: {sorted(expected_images ^ actual_images)}")
    files = manifest["assets"] + manifest["generated_files"]
    for page in manifest["pages"]:
        files += page["files"]
    for entry in files:
        path = CACHE / entry["path"]
        if not path.is_file() or digest(path.read_bytes()) != entry["sha256"]:
            failures.append(f"Missing or changed file: {path}")
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        return 1
    print(f"Verified {len(actual)} complete pages, {len(manifest['assets'])} image variants, and {len(files)} file hashes.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Check local completeness and hashes without network access")
    args = parser.parse_args()
    catalog = json.loads(CATALOG.read_text())
    if args.verify:
        return verify(catalog)

    CACHE.mkdir(parents=True, exist_ok=True)
    pages, documents, texts, failures = {}, {}, {}, []
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = {pool.submit(fetch_page, page): page for page in catalog["pages"]}
        for future in as_completed(jobs):
            page = jobs[future]
            try:
                entry, document, markdown = future.result()
                pages[page["id"]] = entry
                documents[page["id"]] = document
                texts[page["id"]] = markdown
                print(f"Fetched: {entry['title']}", flush=True)
            except Exception as error:
                failures.append(f"{page['url']}: {error}")

    assets = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = {pool.submit(fetch_image, url): url for url in image_sources(documents, catalog["asset_pages"])}
        for future in as_completed(jobs):
            try:
                assets.append(future.result())
            except Exception as error:
                failures.append(f"{jobs[future]}: {error}")

    page_lookup = {page["url"]: page["id"] for page in pages.values()}
    asset_lookup = {entry["source_url"]: entry["path"] for entry in assets}
    generated = []

    def write_generated(relative, text):
        path = CACHE / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.encode()
        path.write_bytes(data)
        generated.append({"path": relative, "sha256": digest(data), "bytes": len(data)})

    index = ["# Apple documentation downloaded for iPhone Duo", "", catalog["scope"], "",
             "These are complete official page snapshots, not summaries. `raw/` preserves Apple’s responses. "
             "`pages/` contains the same Markdown with local links. All inline illustrations from the catalog "
             "are in `assets/`, including light/dark variants where supplied. [Browse the image atlas](IMAGES.md). "
             "Video resources, design kits, and links outside the catalog remain online.", "",
             "Copyright © Apple Inc. All rights reserved. These downloaded materials are not covered by the "
             "skill’s MIT license. [Apple site terms](https://www.apple.com/legal/internet-services/terms/site.html).", "",
             "This directory is a local, ignored source cache. Use `../apple-docs.md` for reading order and refresh instructions.", "",
             "## Complete pages", "", "| Page | Why included |", "| --- | --- |"]
    for item in catalog["pages"]:
        page = pages.get(item["id"])
        if not page:
            continue
        readable = readable_markdown(page, documents[page["id"]], texts[page["id"]], page_lookup, asset_lookup)
        write_generated(f"pages/{page['id']}.md", readable)
        index.append(f"| [{page['title']}](pages/{page['id']}.md) | {page['reason']} |")
    index += ["", "## Duo HIG section coverage", ""]
    main_id = catalog["asset_pages"][0]
    for heading in pages.get(main_id, {}).get("headings", []):
        index.append(f"- {heading['text']}")
    gallery = ["# Apple documentation image atlas", "",
               "Inline illustrations from the downloaded pages. Apple’s original alt text and variant labels "
               "are retained below. Copyright © Apple Inc.; Apple’s terms apply. See manifest.json for source URLs and hashes.", ""]
    for item in catalog["pages"]:
        document = documents.get(item["id"], {})
        used = image_ids(document)
        if not used:
            continue
        gallery += ["## " + item["title"], ""]
        for identifier in sorted(used):
            reference = document.get("references", {}).get(identifier, {})
            alt = reference.get("alt") or identifier
            gallery += ["### " + identifier, "", alt, ""]
            for variant in reference.get("variants", []):
                url = asset_url(variant["url"])
                if url in asset_lookup:
                    traits = ", ".join(variant.get("traits", []))
                    gallery += ["**" + (traits or "Default") + "**", "",
                                f"![{alt.replace('[', '').replace(']', '')}]({asset_lookup[url]})", ""]
    write_generated("IMAGES.md", "\n".join(gallery) + "\n")
    if failures:
        index += ["", "## Retrieval failures", "", *["- " + failure for failure in failures]]
    write_generated("INDEX.md", "\n".join(index) + "\n")
    manifest = {
        "schema_version": 1, "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "catalog_sha256": digest(CATALOG.read_bytes()), "scope": catalog["scope"],
        "pages": [pages[item["id"]] for item in catalog["pages"] if item["id"] in pages],
        "assets": sorted(assets, key=lambda entry: entry["path"]),
        "generated_files": generated, "failures": failures,
    }
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return verify(catalog)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
