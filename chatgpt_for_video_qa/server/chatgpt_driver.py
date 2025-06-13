import asyncio
import os
from playwright.async_api import async_playwright

async def chat_with_gpt(question, transcript):
    prompt = f"Here is a video transcript:\n{transcript}\n\nQuestion: {question}\n\nAnswer:"

    # Adjust this path to your Chrome executable (macOS default)
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # Adjust this to your actual Chrome user profile folder
    user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default")

    async with async_playwright() as p:
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=chrome_path,
            headless=False,  # Show browser for debugging
        )
        page = await browser_context.new_page()

        # Go to ChatGPT
        await page.goto("https://chat.openai.com/chat", wait_until="networkidle")

        # Wait until the textarea for typing your prompt is visible and enabled
        try:
            await page.wait_for_selector("textarea", timeout=30000)
        except Exception:
            await browser_context.close()
            return "❌ ChatGPT page didn't load properly. Are you logged in?"

        # Fill the prompt and press Enter
        await page.fill("textarea", prompt)
        await page.press("textarea", "Enter")

        try:
            # Wait for ChatGPT's response to appear
            await page.wait_for_selector(".markdown", timeout=30000)
            elements = await page.query_selector_all(".markdown")
            answer_text = await elements[-1].inner_text() if elements else "⚠️ No answer received."
        except Exception as e:
            answer_text = f"❌ Error while waiting for response: {e}"

        await browser_context.close()
        return answer_text

if __name__ == "__main__":
    q = "What's the video about?"
    t = "This is a sample transcript from a video..."
    result = asyncio.run(chat_with_gpt(q, t))
    print(result)
