#!/usr/bin/env python3
"""
Screenshot capture utility for UI validation.

Captures screenshots at multiple viewports for visual validation.
Uses Playwright for browser automation.

Usage:
    capture-screenshots.py <feature_dir> <story_id> [--pages "/page1,/page2"] [--viewports "375,768,1280"]

Examples:
    capture-screenshots.py features/F0004c-ui-polish-fixes F0004c-04
    capture-screenshots.py features/F0004c-ui-polish-fixes F0004c-04 --pages "/library,/read/test-id"
    capture-screenshots.py features/F0004c-ui-polish-fixes F0004c-04 --viewports "375,1280"

Output:
    Creates screenshots in: <feature_dir>/screenshots/<story_id>/
    - page-name-375.png
    - page-name-768.png
    - page-name-1280.png
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Check for Playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


def slugify(text: str) -> str:
    """Convert path to filename-safe slug."""
    return text.strip("/").replace("/", "-").replace("{", "").replace("}", "") or "home"


def start_app_server(port: int = 5098) -> subprocess.Popen:
    """Start the app server for screenshots."""
    import os

    env = os.environ.copy()
    env["PORT"] = str(port)
    env["APP_ENV"] = "development"

    process = subprocess.Popen(
        ["uv", "run", "python", "-m", "app"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    import httpx
    base_url = f"http://localhost:{port}"
    for _ in range(30):
        try:
            response = httpx.get(base_url, timeout=1.0)
            if response.status_code == 200:
                return process
        except Exception:
            pass
        time.sleep(0.5)

    process.terminate()
    raise RuntimeError("App server failed to start")


def capture_screenshots(
    feature_dir: str,
    story_id: str,
    pages: list[str],
    viewports: list[int],
    base_url: str = "http://localhost:5098",
) -> list[Path]:
    """Capture screenshots for all pages at all viewports."""

    if not PLAYWRIGHT_AVAILABLE:
        print("Error: Playwright not installed. Run: uv pip install playwright && playwright install chromium")
        sys.exit(1)

    # Create screenshot directory
    screenshot_dir = Path(feature_dir) / "screenshots" / story_id
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    captured = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for viewport_width in viewports:
            context = browser.new_context(
                viewport={"width": viewport_width, "height": 900},
            )
            page = context.new_page()

            for page_path in pages:
                try:
                    # Handle parameterized paths - use a test ID if needed
                    actual_path = page_path
                    if "{" in page_path:
                        # Try to get a real book ID from the library
                        page.goto(f"{base_url}/library")
                        page.wait_for_timeout(500)
                        book_link = page.locator(".book-card a").first
                        if book_link.count() > 0:
                            href = book_link.get_attribute("href")
                            if href:
                                actual_path = href
                        else:
                            print(f"  Skipping {page_path} - no books in library")
                            continue

                    url = f"{base_url}{actual_path}"
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(500)  # Extra time for animations

                    # Generate filename
                    slug = slugify(page_path)
                    filename = f"{slug}-{viewport_width}.png"
                    filepath = screenshot_dir / filename

                    page.screenshot(path=str(filepath), full_page=True)
                    captured.append(filepath)
                    print(f"  Captured: {filename}")

                except Exception as e:
                    print(f"  Error capturing {page_path} at {viewport_width}px: {e}")

            context.close()

        browser.close()

    return captured


def main():
    parser = argparse.ArgumentParser(description="Capture UI screenshots for validation")
    parser.add_argument("feature_dir", help="Feature directory path")
    parser.add_argument("story_id", help="Story ID (e.g., F0004c-04)")
    parser.add_argument("--pages", default="/,/library,/about",
                       help="Comma-separated page paths (default: /,/library,/about)")
    parser.add_argument("--viewports", default="375,768,1280",
                       help="Comma-separated viewport widths (default: 375,768,1280)")
    parser.add_argument("--base-url", default="http://localhost:5098",
                       help="Base URL (default: http://localhost:5098)")
    parser.add_argument("--start-server", action="store_true",
                       help="Start app server before capturing")

    args = parser.parse_args()

    pages = [p.strip() for p in args.pages.split(",")]
    viewports = [int(v.strip()) for v in args.viewports.split(",")]

    print(f"Capturing screenshots for {args.story_id}")
    print(f"  Pages: {pages}")
    print(f"  Viewports: {viewports}px")
    print(f"  Output: {args.feature_dir}/screenshots/{args.story_id}/")
    print()

    server = None
    try:
        if args.start_server:
            print("Starting app server...")
            server = start_app_server(port=5098)
            print("  Server started on port 5098")

        captured = capture_screenshots(
            args.feature_dir,
            args.story_id,
            pages,
            viewports,
            args.base_url,
        )

        print()
        print(f"Captured {len(captured)} screenshots")

        # Output paths for further processing
        for path in captured:
            print(f"  {path}")

    finally:
        if server:
            server.terminate()
            server.wait(timeout=5)


if __name__ == "__main__":
    main()
