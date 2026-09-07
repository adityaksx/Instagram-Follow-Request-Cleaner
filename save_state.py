# save_state.py
from playwright.sync_api import sync_playwright

STATE = "ig_state.json"

with sync_playwright() as p:
    # Use Chromium; headless=False for manual login
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=60000)
    print("Log into Instagram in this window, then press Enter here...")
    input()
    context.storage_state(path=STATE)
    print(f"Saved login state to {STATE}")
    context.close()
    browser.close()
