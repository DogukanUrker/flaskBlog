# Import the playwright module and the constants file
from playwright.sync_api import Playwright, sync_playwright, expect
from constants import URL


# Define a function that takes a playwright object as an argument
def run(playwright: Playwright) -> None:
    # Launch a chromium browser in non-headless mode
    browser = playwright.chromium.launch(headless=False)
    # Create a new browser context
    context = browser.new_context()
    # Create a new page in the context
    page = context.new_page()
    # Navigate to the URL defined in the constants file
    page.goto(URL)
    # Click on the button with the name ""
    page.get_by_role("button", name="").click()
    # Click on the input field with the placeholder "username"
    page.get_by_placeholder("username").click()
    # Fill the input field with the value "TestUser"
    page.get_by_placeholder("username").fill("TestUser2")
    # Click on the input field with the placeholder "email"
    page.get_by_placeholder("email").click()
    # Fill the input field with the value "testuser@flaskblog.com"
    page.get_by_placeholder("email").fill("testuser2@flaskblog.com")
    # Click on the input field with the placeholder "password" (exact match)
    page.get_by_placeholder("password", exact=True).click()
    # Fill the input field with the value "testuser"
    page.get_by_placeholder("password", exact=True).fill("testuser2")
    # Click on the input field with the placeholder "confirm your password"
    page.get_by_placeholder("confirm your password").click()
    # Fill the input field with the same value as the password
    page.get_by_placeholder("confirm your password").fill("testuser2")
    # Click on the button with the name "Signup"
    page.get_by_role("button", name="Signup").click()
    # Click on the first link on the page
    page.get_by_role("link").first.click()

    # Close the browser context and the browser
    context.close()
    browser.close()


# Use the sync_playwright context manager to run the function
with sync_playwright() as playwright:
    run(playwright)
