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
    # Click on the button with the name ""
    page.get_by_role("button", name="").click()
    # Click on the input field with the placeholder "username"
    page.get_by_placeholder("username").click()
    # Fill the input field with the value "TestUser"
    page.get_by_placeholder("username").fill("TestUser")
    # Click on the input field with the placeholder "password"
    page.get_by_placeholder("password").click()
    # Fill the input field with the value "testuser"
    page.get_by_placeholder("password").fill("testuser")
    # Click on the button with the name "Login"
    page.get_by_role("button", name="Login").click()
    # Navigate to the first post in the database
    page.goto(f"{URL}/post/1")
    # Click on the input field with the placeholder "What are your thoughts?"
    page.get_by_placeholder("What are your thoughts?").click()
    # Fill the input field with the value "Wow that's really fun to read! 💖"
    page.get_by_placeholder("What are your thoughts?").fill(
        "Wow that's really fun to read! 💖"
    )
    # Click on the button with the name ""
    page.get_by_role("button", name="").click()

    # Close the browser context and the browser
    context.close()
    browser.close()


# Use the sync_playwright context manager to run the function
with sync_playwright() as playwright:
    run(playwright)
