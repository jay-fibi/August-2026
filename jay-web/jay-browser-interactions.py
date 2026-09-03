"""
jay-browser-interactions.py
Jay Task - Launch a browser on a test page with interactive elements, click a
button, type into form fields, submit the form and scroll the page.

Run:
    python3 jay-web/jay-browser-interactions.py                  # headless (default)
    JAY_HEADLESS=0 python3 jay-web/jay-browser-interactions.py   # visible window
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
JAY_PAGE = "jay-interactive.html"
JAY_SHOT_DIR = JAY_WEB_DIR / "jay-screenshots"

JAY_NAME_VALUE = "jay gohil"
JAY_EMAIL_VALUE = "jay.gohil@example.com"
JAY_ROLE_VALUE = "jay-engineer"
JAY_NOTES_VALUE = "Jay typed these notes through Playwright."


def jay_log(step, message):
    """Print a single labelled step line."""
    print(f"[Jay {step}] {message}", flush=True)


def jay_start_local_server(directory):
    """
    Serve `directory` over http://127.0.0.1:<port> in a daemon thread.

    ES modules are blocked by CORS on file:// URLs, so the local page is served
    over HTTP to let jay-interactive.js actually run.
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


def jay_report(evidence):
    """Print collected page evidence as indented key/value lines."""
    for key, value in evidence.items():
        jay_log("verify", f"  {key} = {value!r}")


def jay_step_one_load(page, base_url):
    """Step 1 - open the interactive test page and confirm it is ready."""
    url = f"{base_url}/{JAY_PAGE}"
    response = page.goto(url, wait_until="load")
    assert response.ok, f"Jay bad status for interactive page: {response.status}"

    page.wait_for_selector("body[data-jay-ready='true']", timeout=10_000)

    evidence = {
        "url": page.url,
        "title": page.title(),
        "buttons": page.locator("button").count(),
        "inputs": page.locator("input, select, textarea").count(),
        "forms": page.locator("form").count(),
        "scroll_rows": page.locator(".jay-scroll-item").count(),
    }
    assert "Jay Interactive" in evidence["title"], f"Jay title mismatch: {evidence['title']}"
    assert evidence["buttons"] >= 3, "Jay expected at least 3 buttons"
    assert evidence["inputs"] >= 5, "Jay expected at least 5 form controls"
    assert evidence["forms"] == 1, "Jay expected exactly 1 form"

    jay_log("step 1", f"loaded {url} -> HTTP {response.status}")
    jay_report(evidence)
    return evidence


def jay_step_two_click(page):
    """Step 2 - click a button element and confirm the handler ran."""
    button = page.locator("#jay-action-button")
    button.wait_for(state="visible")
    assert button.is_enabled(), "Jay action button is disabled"

    before = page.inner_text("#jay-click-output")
    button.click()
    page.wait_for_function(
        "() => document.querySelector('#jay-click-output').dataset.jayClicks === '1'"
    )

    button.click()
    button.click()
    page.wait_for_function(
        "() => document.querySelector('#jay-click-output').dataset.jayClicks === '3'"
    )

    after = page.inner_text("#jay-click-output")
    log_text = page.inner_text("#jay-click-log")

    assert before == "Jay clicks: 0", f"Jay unexpected initial state: {before}"
    assert after == "Jay clicks: 3", f"Jay click counter wrong: {after}"
    assert "3 time(s)" in log_text, f"Jay click log wrong: {log_text}"

    jay_log("step 2", f"clicked #jay-action-button 3x -> {after!r}")
    return {"before": before, "after": after, "log": log_text}


def jay_step_three_type(page):
    """Step 3 - input text into the form fields."""
    page.fill("#jay-name-input", JAY_NAME_VALUE)
    page.fill("#jay-email-input", JAY_EMAIL_VALUE)
    page.select_option("#jay-role-select", JAY_ROLE_VALUE)

    # type() presses real keys, proving per-keystroke handlers also fire.
    page.click("#jay-notes-input")
    page.type("#jay-notes-input", JAY_NOTES_VALUE, delay=10)
    page.check("#jay-terms-checkbox")

    values = {
        "name": page.input_value("#jay-name-input"),
        "email": page.input_value("#jay-email-input"),
        "role": page.input_value("#jay-role-select"),
        "notes": page.input_value("#jay-notes-input"),
        "terms_checked": page.is_checked("#jay-terms-checkbox"),
        "live_echo": page.inner_text("#jay-live-echo"),
    }

    assert values["name"] == JAY_NAME_VALUE, f"Jay name not typed: {values['name']}"
    assert values["email"] == JAY_EMAIL_VALUE, f"Jay email not typed: {values['email']}"
    assert values["role"] == JAY_ROLE_VALUE, f"Jay role not selected: {values['role']}"
    assert values["notes"] == JAY_NOTES_VALUE, f"Jay notes not typed: {values['notes']}"
    assert values["terms_checked"] is True, "Jay terms checkbox not checked"
    assert "Jay Gohil" in values["live_echo"], f"Jay live echo wrong: {values['live_echo']}"

    jay_log("step 3", "typed into text, email, select, textarea and checkbox")
    jay_report(values)
    return values


def jay_step_four_submit(page):
    """Step 4 - submit the form and confirm the submitted values render."""
    assert page.locator("#jay-form-result").is_hidden(), "Jay result visible too early"

    page.click("#jay-submit-button")
    page.wait_for_selector("#jay-form-result:not([hidden])", timeout=10_000)
    page.wait_for_selector("form[data-jay-submit-state='submitted']", timeout=10_000)

    submitted = {
        "message": page.inner_text("#jay-form-message"),
        "submit_count": page.get_attribute("#jay-signup-form", "data-jay-submit-count"),
        "error_hidden": page.locator("#jay-form-error").is_hidden(),
    }
    for field in ("jayName", "jayEmail", "jayRole", "jayNotes", "jayTerms"):
        submitted[field] = page.inner_text(f"dd[data-jay-field='{field}']")

    assert "submitted successfully" in submitted["message"], submitted["message"]
    assert submitted["submit_count"] == "1", f"Jay submit count: {submitted['submit_count']}"
    assert submitted["error_hidden"], "Jay error banner should stay hidden"
    assert submitted["jayEmail"] == JAY_EMAIL_VALUE, submitted["jayEmail"]
    assert submitted["jayTerms"] == "true", submitted["jayTerms"]

    jay_log("step 4", f"form submitted -> {submitted['message']!r}")
    jay_report(submitted)
    return submitted


def jay_step_five_scroll(page):
    """Step 5 - scroll down the page and confirm the viewport actually moved."""
    start_y = page.evaluate("window.scrollY")

    # Mouse wheel scrolling, the closest match to a real user gesture.
    for _ in range(6):
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(80)

    mid_y = page.evaluate("window.scrollY")
    assert mid_y > start_y, f"Jay wheel scroll did not move: {start_y} -> {mid_y}"

    # Keyboard scrolling, then a programmatic jump to the very bottom.
    page.keyboard.press("End")
    page.wait_for_function(
        "() => window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2",
        timeout=10_000,
    )

    page.locator("#jay-scroll-sentinel").scroll_into_view_if_needed()
    page.wait_for_selector("#jay-scroll-sentinel[data-jay-seen='true']", timeout=10_000)

    scroll_state = {
        "start_y": start_y,
        "after_wheel_y": mid_y,
        "final_y": page.evaluate("window.scrollY"),
        "max_scroll_y": page.evaluate("document.body.dataset.jayMaxScroll"),
        "readout": page.inner_text("#jay-scroll-readout"),
        "depth_percent": page.get_attribute("#jay-scroll-readout", "data-jay-scroll-depth"),
        "sentinel_visible": page.locator("#jay-scroll-sentinel").is_visible(),
    }

    assert scroll_state["final_y"] >= mid_y, "Jay page scrolled back up unexpectedly"
    assert int(scroll_state["depth_percent"]) >= 90, scroll_state["readout"]
    assert scroll_state["sentinel_visible"], "Jay bottom sentinel not in viewport"

    jay_log("step 5", f"scrolled {start_y} -> {scroll_state['final_y']}px")
    jay_report(scroll_state)
    return scroll_state


def jay_main():
    """Drive the full interactive browser session end to end."""
    headless = os.environ.get("JAY_HEADLESS", "1") != "0"
    JAY_SHOT_DIR.mkdir(exist_ok=True)

    httpd, base_url = jay_start_local_server(JAY_WEB_DIR)
    jay_log("server", f"serving {JAY_WEB_DIR} at {base_url}")

    exit_code = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.on("console", lambda msg: jay_log("console", f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: jay_log("pageerror", str(err)))
        jay_log("launch", f"Chromium {browser.version} (headless={headless})")

        try:
            jay_step_one_load(page, base_url)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-1-loaded.png"))

            jay_step_two_click(page)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-2-clicked.png"))

            jay_step_three_type(page)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-3-typed.png"))

            jay_step_four_submit(page)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-4-submitted.png"))

            jay_step_five_scroll(page)
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-5-scrolled.png"))

        except Exception as error:
            exit_code = 1
            jay_log("error", f"{type(error).__name__}: {error}")
            page.screenshot(path=str(JAY_SHOT_DIR / "jay-interactive-failure.png"))

        finally:
            context.close()
            browser.close()
            jay_log("close", f"browser closed (connected={browser.is_connected()})")

    httpd.shutdown()
    httpd.server_close()
    jay_log("server", "local HTTP server stopped")
    jay_log("done", "PASS" if exit_code == 0 else "FAIL")
    return exit_code


if __name__ == "__main__":
    sys.exit(jay_main())
