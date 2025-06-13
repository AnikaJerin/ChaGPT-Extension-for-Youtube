import asyncio
from playwright.async_api import async_playwright
# """
# ***** can't use this ---OpenAI’s login flow is not automated or supported by their UI for automated browsers.
# This is a common limitation with sites employing CAPTCHA, multi-step authentication, or phone verification. *********
# """
async def main():
    async with async_playwright() as p:
        # 1️⃣ Open a non-headless browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 2️⃣ Navigate to ChatGPT
        await page.goto("https://chatgpt.com/")
        print("Please login manually in this browser.")
        await asyncio.sleep(60)  # wait 60 seconds or until you manually complete login

        # 3️⃣ Save authentication state
        await context.storage_state(path='auth.json')
        print("Auth state successfully saved.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main()) 
