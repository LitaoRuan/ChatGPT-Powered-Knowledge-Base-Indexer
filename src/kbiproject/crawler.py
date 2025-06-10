import asyncio
import os
import re
from playwright.async_api import async_playwright, Page

def load_urls_from_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


async def fetch_title(page: Page, url: str) -> str:
    await page.goto(url)
    title = await page.title()
    print(f"URL: {url} | Title: {title}")
    return title


async def extract_text_from_tags(page: Page, url: str) -> list[str]:
    await page.goto(url)
    elements = await page.query_selector_all('#mw-content-text h1, #mw-content-text h2, #mw-content-text h3, #mw-content-text p, #mw-content-text li')
    text_content = []
    for element in elements:
        # Skip elements inside the Table of Contents
        # This correctly checks if the element is inside #toc
        is_inside_toc = await element.evaluate("el => el.closest('#toc') !== null")
        if is_inside_toc:
            continue


        tag = await element.evaluate("el => el.tagName")
        text = (await element.inner_text()).strip()

        if not text:
            continue

        if tag == "H1":
            text_content.append(f"# {text}\n")
        elif tag == "H2":
            text_content.append(f"## {text}\n")
        elif tag == "H3":
            text_content.append(f"### {text}\n")
        else:
            text_content.append(text)
    return text_content


def sanitize_filename(title: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", title).strip()


def save_text_to_file(title: str, content: list[str]):
    os.makedirs("data", exist_ok=True)
    filename = sanitize_filename(title) + ".txt"
    filepath = os.path.join("data", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in content:
            f.write(line + "\n")
    print(f"Saved: {filepath}")


async def main():
    urls = load_urls_from_file("urls.txt")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for url in urls:
            title = await fetch_title(page, url)
            text_content = await extract_text_from_tags(page, url)
            save_text_to_file(title, text_content)

        await browser.close()
        print("All pages processed and saved individually.")

asyncio.run(main())
