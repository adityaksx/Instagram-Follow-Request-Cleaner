import json, time
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

STATE = "ig_state.json"
JSON_PATH = "pending_follow_requests.json"

def load_links(path):
    data = json.load(open(path, "r", encoding="utf-8"))
    out = []
    for entry in data.get("relationships_follow_requests_sent", []):
        sl = entry.get("string_list_data", [])
        if isinstance(sl, list):
            for item in sl:
                if isinstance(item, dict) and item.get("href"):
                    out.append(item["href"])
        elif isinstance(sl, dict) and sl.get("href"):
            out.append(sl["href"])
    # normalize/validate
    clean = []
    for u in out:
        if not isinstance(u, str):
            continue
        s = u.strip()
        if not s:
            continue
        try:
            pr = urlparse(s)
            if pr.scheme in ("http", "https") and "instagram.com" in pr.netloc:
                clean.append(s)
        except Exception:
            continue
    return clean

def click_requested_then_unfollow(page):
    # 1) Click the "Requested" button visible on the profile header
    requested_locators = [
        "button:has-text('Requested')",
        "[role=button]:has-text('Requested')",
        "xpath=//button[normalize-space()='Requested']",
    ]
    clicked_requested = False
    for sel in requested_locators:
        loc = page.locator(sel).first
        if loc.count() > 0 and loc.is_visible():
            loc.click(timeout=8000)
            clicked_requested = True
            break
    if not clicked_requested:
        return False

    # 2) In the confirmation dialog, click "Unfollow"
    unfollow_locators = [
        "button:has-text('Unfollow')",
        "[role=button]:has-text('Unfollow')",
        "xpath=//div[@role='dialog']//button[normalize-space()='Unfollow']",
    ]
    for sel in unfollow_locators:
        loc = page.locator(sel).first
        if loc.count() > 0 and loc.is_visible():
            loc.click(timeout=8000)
            return True

    # If dialog opened but no Unfollow, close and report failure
    try:
        page.keyboard.press("Escape")
    except Exception:
        pass
    return False

def main():
    links = load_links(JSON_PATH)
    print(f"Loaded {len(links)} links")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STATE)  # reuse saved login
        page = context.new_page()

        ok, fail = 0, 0
        for i, url in enumerate(links, 1):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                # Small settle for dynamic UI
                page.wait_for_timeout(500)
                if click_requested_then_unfollow(page):
                    ok += 1
                    print(f"[{i}] OK")
                else:
                    print(f"[{i}] Skip: no Requested/Unfollow")
                time.sleep(2.0)
            except PWTimeoutError:
                fail += 1
                print(f"[{i}] FAIL: timeout")
            except Exception as e:
                fail += 1
                print(f"[{i}] FAIL: {e}")

        print(f"\nDone. OK={ok} FAIL={fail}")
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
