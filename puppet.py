import asyncio
from pyppeteer import launch

async def get_html(url, save_file):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.flashscorekz.com/', {'waitUntil': 'domcontentloaded'})
    content = await page.content()
    with open(save_file, 'w', encoding='utf-8') as file:
        file.write(content)
    await browser.close()
    return content

asyncio.get_event_loop().run_until_complete(get_html('https://www.flashscorekz.com/', 'flashscore.txt'))


