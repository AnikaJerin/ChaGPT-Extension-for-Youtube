# save_auth.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://chat.openai.com/")

    print("Please log in to ChatGPT in the opened browser window.")
    input("After logging in, press Enter here to save the session and exit...")

    context.storage_state(path="auth.json")
    browser.close()
    print("Session saved to auth.json")
