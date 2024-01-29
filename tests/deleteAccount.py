from playwright.sync_api import Playwright, sync_playwright, expect
from constants import URL


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)
    page.get_by_role("button", name="").click()
    page.get_by_placeholder("username").click()
    page.get_by_placeholder("username").fill("testuser")
    page.get_by_placeholder("password").click()
    page.get_by_placeholder("password").fill("testuser")
    page.get_by_role("button", name="Login").click()
    page.locator("div:nth-child(3) > a").first.click()
    page.get_by_role("link", name="settings").click()
    page.get_by_role("button", name=" delete account").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
