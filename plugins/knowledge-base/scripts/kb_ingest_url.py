"""Download images from a URL's HTML page to the knowledge base raw/images/ directory.

HTML fetching is handled by Claude Code's WebFetch tool.
This script only handles image downloading (binary I/O that WebFetch cannot do).

Input (stdin JSON):
    {"url": "...", "kb_root": "...", "source_name": "..."}

Output (stdout JSON):
    {"images": [...], "image_dir": "...", "source_name": "...", "errors": [...]}
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlretrieve, urlopen


class ImageExtractor(HTMLParser):
    """Extract image src attributes from HTML."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag == "img":
            for attr, value in attrs:
                if attr == "src" and value:
                    absolute = urljoin(self.base_url, value)
                    if absolute.startswith(("http://", "https://")):
                        self.images.append(absolute)


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", "_", name)
    return name[:100].strip("_")


def download_page_html(url: str) -> str:
    """Download raw HTML for image extraction only."""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (KB-Plugin/0.1)"})
    with urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def download_image(img_url: str, save_dir: Path) -> str | None:
    """Download a single image. Returns local filename or None on failure."""
    try:
        parsed = urlparse(img_url)
        filename = sanitize_filename(Path(parsed.path).name)
        if not filename or filename == "_":
            filename = f"image_{hash(img_url) % 10000}.jpg"
        dest = save_dir / filename
        if not dest.exists():
            urlretrieve(img_url, dest)
        return filename
    except Exception:
        return None


def main():
    data = json.loads(sys.stdin.read())
    url = data["url"]
    kb_root = Path(data["kb_root"])
    source_name = data.get("source_name") or sanitize_filename(
        urlparse(url).netloc + "_" + urlparse(url).path.strip("/")
    )

    img_dir = kb_root / "raw" / "images" / source_name
    img_dir.mkdir(parents=True, exist_ok=True)

    errors = []

    # Download HTML just to extract image URLs
    try:
        html_content = download_page_html(url)
    except (URLError, Exception) as e:
        # Image download failure is non-fatal — WebFetch handles the main content
        print(json.dumps({
            "images": [],
            "image_dir": None,
            "source_name": source_name,
            "errors": [f"Failed to fetch HTML for image extraction: {e}"],
        }))
        sys.exit(0)

    # Extract and download images
    extractor = ImageExtractor(url)
    extractor.feed(html_content)

    downloaded_images = []
    for img_url in extractor.images:
        filename = download_image(img_url, img_dir)
        if filename:
            downloaded_images.append(filename)
        else:
            errors.append(f"Failed to download image: {img_url}")

    # Clean up empty image directory
    if not downloaded_images and img_dir.exists():
        try:
            img_dir.rmdir()
        except OSError:
            pass

    output = {
        "images": downloaded_images,
        "image_dir": str(img_dir) if downloaded_images else None,
        "source_name": source_name,
        "errors": errors,
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
