"""
jay-browser-session.py
Jay Task - Launch a browser, load a local HTML page, verify it, navigate to a
second page, then close the browser.

Run:
    python3 jay-web/jay-browser-session.py                  # headless (default)
    JAY_HEADLESS=0 python3 jay-web/jay-browser-session.py   # visible window
"""

import functools
import http.server
import os
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

JAY_WEB_DIR = Path(__file__).resolve().parent
JAY_PAGE_ONE = "jay-index.html"
JAY_PAGE_TWO = "jay-about.html"
JAY_EXTERNAL_URL = "https://example.com/"
JAY_SHOT_DIR = JAY_WEB_DIR / "jay-screenshots"


def jay_log(step, message):
    """Print a single labelled step line."""
    print(f"[Jay {step}] {message}", flush=True)


def jay_start_local_server(directory):
    """
    Serve `directory` over http://127.0.0.1:<port> in a daemon thread.

    ES modules and fetch() are blocked by CORS on file:// URLs, so the local
    page is served over HTTP to let jay-app.js actually run.
    """
    class JayQuietHandler(http.server.SimpleHTTPRequestHandler):
        """SimpleHTTPRequestHandler with per-request stderr logging disabled."""

        def log_message(self, format, *args):
            pass

    handler = functools.partial(JayQuietHandler, directory=str(directory))

    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    httpd.allow_reuse_address = True
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{port}"


def jay_verify_page(page, expected_title_fragment, required_selectors):
    """
    Verify a page really loaded.

    Checks the document load state, the title, and that every required selector
    is present in the DOM. Returns collected evidence, raises AssertionError on
    any failure.
    """
    page.wait_for_load_state("load")

    evidence = {
        "url": page.url,
        "title": page.title(),
        "ready_state": page.evaluate("document.readyState"),
        "dom_nodes": page.evaluate("document.getElementsByTagName('*').length"),
    }

    assert evidence["ready_state"] == "complete", (
        f"Jay page not complete: readyState={evidence['ready_state']}"
    )
    assert expected_title_fragment.lower() in evidence["title"].lower(), (
        f"Jay title mismatch: expected ~'{expected_title_fragment}', "
        f"got '{evidence['title']}'"
    )
    assert evidence["dom_nodes"] > 0, "Jay page rendered zero DOM nodes"

    for selector in required_selectors:
        locator = page.locator(selector)
        assert locator.count() > 0, f"Jay missing selector: {selector}"
        evidence[selector] = locator.first.inner_text().strip()

    return evidence


def jay_report(evidence):
    """Print collected page evidence as indented key/value lines."""
    for key, value in evidence.items():
        jay_log("verify", f"  {key} = {value!r}")


def jay_main():
    """Drive the full browser session end to end."""
    headless = os.environ.get("JAY_HEADLESS", "1") != "0"
    JAY_SHOT_DIR.mkdir(exist_ok=True)

    httpd, base_url = jay_start_local_server(JAY_WEB_DIR)
    jay_log("server", f"serving {JAY_WEB_DIR} at {base_url}")

    exit_code = 0
    with sync_playwright() as playwright:
        # --- Step 1: launch a browser instance ---
        browser = playwright.chromium.launch(headless=headless)
        jay_log("step 1", f"launched Chromium {browser.version} (headless={headless})")

        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        page.on("console", lambda msg: jay_log("console", f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: jay_log("pageerror", str(err)))

        try:
            # --- Step 2: navigate to the local HTML file ---
            local_url = f"{base_url}/{JAY_PAGE_ONE}"
            response = page.goto(local_url, wait_until="networkidle")
            jay_log("step 2", f"navigated to {local_url} -> HTTP {response.status}")
            assert response.ok, f"Jay bad status for page one: {response.status}"

            # --- Step 3: verify page loading ---
            page.wait_for_selector("#jay-status.jay-status--ok", timeout=10_000)
            evidence = jay_verify_page(
                page,
                expected_title_fragment="Jay Web Demo",
                required_selectors=[
                    "#jay-app-title",
                    "#jay-status",
                    "#jay-counter-output",
                ],
            )
            feature_count = page.locator("#jay-feature-list .jay-feature-item").count()
            evidence["feature_items_rendered"] = feature_count
            assert feature_count == 5, f"Jay expected 5 features, got {feature_count}"

            page.click("#jay-counter-button")
            evidence["after_click"] = page.inner_text("#jay-counter-output")
            assert evidence["after_click"] == "Jay clicks: 1", "Jay click handler failed"

            jay_log("step 3", "page one verified (title, DOM, config render, JS click)")
            jay_report(evidence)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-page-one.png"), full_page=True)

            # --- Step 4: navigate to a second page ---
            second_url = f"{base_url}/{JAY_PAGE_TWO}"
            response_two = page.goto(second_url, wait_until="load")
            jay_log("step 4", f"navigated to {second_url} -> HTTP {response_two.status}")
            assert response_two.ok, f"Jay bad status for page two: {response_two.status}"

            evidence_two = jay_verify_page(
                page,
                expected_title_fragment="Jay About Page",
                required_selectors=[
                    "#jay-about-title",
                    "#jay-about-body",
                    "#jay-back-link",
                ],
            )
            jay_log("step 4", "page two verified")
            jay_report(evidence_two)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-page-two.png"), full_page=True)

            # --- Step 4b: a web-based page, to prove external navigation too ---
            try:
                response_web = page.goto(
                    JAY_EXTERNAL_URL, wait_until="load", timeout=15_000
                )
                jay_log(
                    "step 4b",
                    f"navigated to {JAY_EXTERNAL_URL} -> HTTP {response_web.status}",
                )
                jay_report(jay_verify_page(page, "Example", ["h1"]))
            except Exception as web_error:  # offline sandbox should not fail the run
                jay_log("step 4b", f"skipped external navigation: {web_error}")

            # Back-navigation through browser history, for good measure.
            page.go_back()
            page.wait_for_load_state("load")
            jay_log("step 4c", f"history back -> {page.url} ({page.title()})")

        except Exception as error:
            exit_code = 1
            jay_log("error", f"{type(error).__name__}: {error}")
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-failure.png"))

        finally:
            # --- Step 5: close the browser ---
            context.close()
            browser.close()
            jay_log("step 5", f"browser closed (connected={browser.is_connected()})")

    httpd.shutdown()
    httpd.server_close()
    jay_log("server", "local HTTP server stopped")
    jay_log("done", "PASS" if exit_code == 0 else "FAIL")
    return exit_code


if __name__ == "__main__":
    sys.exit(jay_main())
