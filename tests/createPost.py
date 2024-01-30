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
    # Click on the button with the name ""
    page.get_by_role("button", name="").click()
    # Click on the input field with the placeholder "post title"
    page.get_by_placeholder("post title").click()
    # Fill the input field with the value "Lorem Ipsum"
    page.get_by_placeholder("post title").fill("Lorem Ipsum")
    # Click on the input field with the placeholder "tags"
    page.get_by_placeholder("tags").click()
    # Fill the input field with the values "lorem, ipsum"
    page.get_by_placeholder("tags").fill("lorem, ipsum")
    # Select the option "Other" from the dropdown menu with the id "postCategory"
    page.locator("#postCategory").select_option("Other")
    # Click on the input field with the placeholder "post banner"
    page.get_by_placeholder("post banner").click()
    # Upload the file "postbanner.jpg" to the input field
    page.get_by_placeholder("post banner").set_input_files("postbanner.jpg")
    # Click on the fourth textbox on the page
    page.get_by_role("textbox").nth(4).click()
    # Fill the textbox with the text "Lorem ipsum dolor sit amet, consectetur adipiscing elit, ..."
    page.get_by_role("textbox").nth(4).fill(
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nec nam aliquam sem et tortor. Lacus sed turpis tincidunt id aliquet risus feugiat in. Metus aliquam eleifend mi in nulla posuere sollicitudin. Eget nulla facilisi etiam dignissim diam quis enim lobortis scelerisque. Neque ornare aenean euismod elementum nisi. Dui accumsan sit amet nulla facilisi morbi tempus. Massa tincidunt dui ut ornare lectus. Rutrum tellus pellentesque eu tincidunt tortor aliquam. Sit amet luctus venenatis lectus magna. Tempus imperdiet nulla malesuada pellentesque elit eget. Luctus venenatis lectus magna fringilla urna porttitor rhoncus dolor purus. At varius vel pharetra vel turpis nunc.
        """
    )
    # Click on the button with the name "Post"
    page.get_by_role("button", name="Post").click()

    # Close the browser context and the browser
    context.close()
    browser.close()


# Use the sync_playwright context manager to run the function
with sync_playwright() as playwright:
    run(playwright)
