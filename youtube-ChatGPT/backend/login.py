import asyncio
from playwright.async_api import async_playwright
# """
# ***** can't use this ---OpenAI’s login flow is not automated or supported by their UI for automated browsers.
# This is a common limitation with sites employing CAPTCHA, multi-step authentication, or phone verification. *********
# """
async def login_and_save_auth(auth_file='auth.json'):
    email = "anikajerin2@gmail.com"
    password = "x...."

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./temp-user-profile",
            headless=False
        )

        page = await context.new_page()
        await page.goto("https://chat.openai.com/auth/login")

        # Wait and fill email
        await page.wait_for_selector('input[type="email"]', timeout=30000)
        await page.fill('input[type="email"]', email)
        await page.click('button[type="submit"]')

        # Wait and fill password
        await page.wait_for_selector('input[type="password"]', timeout=30000)
        await page.fill('input[type="password"]', password)
        await page.click('button[type="submit"]')

        # Wait for user to manually complete any captcha / 2FA in visible browser
        print("If you have 2FA or captcha, please complete it manually in the browser window.")
        print("Waiting 60 seconds for manual interaction...")
        await asyncio.sleep(60)  # adjust time if needed

        # Wait for main chat input textarea to ensure login success
        await page.wait_for_selector("textarea[placeholder='Send a message.']", timeout=120000)

        # Save storage state (cookies, localStorage) to file for reuse
        await context.storage_state(path=auth_file)
        print(f"Login successful. Auth state saved to '{auth_file}'.")

        # Close context instead of browser directly
        await context.close()


if __name__ == "__main__":
    asyncio.run(login_and_save_auth()) 
