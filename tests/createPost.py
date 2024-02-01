# Import the playwright module and the constants file
from playwright.sync_api import Playwright, sync_playwright, expect
from constants import URL

# Import the abspath function from the os.path module
from os.path import abspath

# Define the file name and location of the post banner image
fileName = "tests/postBanner.jpg"
fileLocation = abspath(fileName).replace("\\", "\\")
# The replace method is used to escape the backslashes in the file path


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
    page.get_by_placeholder("post banner").set_input_files(fileLocation)
    # Click on the fourth textbox on the page
    page.get_by_role("textbox").nth(4).click()
    # Fill the textbox with the text "Lorem ipsum dolor sit amet, consectetur adipiscing elit, ..."
    page.get_by_role("textbox").nth(4).fill(
        """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. In pellentesque massa placerat duis ultricies. Molestie nunc non blandit massa. Morbi tincidunt augue interdum velit euismod in pellentesque. Posuere lorem ipsum dolor sit amet consectetur. Eu mi bibendum neque egestas congue quisque. In metus vulputate eu scelerisque felis imperdiet. Ac auctor augue mauris augue neque gravida in fermentum et. Parturient montes nascetur ridiculus mus mauris vitae. Donec ac odio tempor orci dapibus ultrices. Adipiscing vitae proin sagittis nisl. Libero id faucibus nisl tincidunt eget nullam non nisi est. Ullamcorper a lacus vestibulum sed arcu non. Vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere. Mi eget mauris pharetra et ultrices neque ornare aenean euismod. Duis ut diam quam nulla porttitor massa id. Integer enim neque volutpat ac tincidunt. Justo laoreet sit amet cursus sit amet dictum sit.
    
Rhoncus est pellentesque elit ullamcorper dignissim cras. Elit ullamcorper dignissim cras tincidunt lobortis feugiat. Neque sodales ut etiam sit amet nisl. Viverra aliquet eget sit amet tellus cras adipiscing enim eu. Gravida cum sociis natoque penatibus et. Tellus elementum sagittis vitae et leo. Morbi tincidunt augue interdum velit euismod in pellentesque massa. Condimentum lacinia quis vel eros donec ac odio tempor. Auctor augue mauris augue neque gravida in fermentum. Viverra mauris in aliquam sem fringilla. Sed ullamcorper morbi tincidunt ornare massa. Amet mauris commodo quis imperdiet massa tincidunt. Amet massa vitae tortor condimentum lacinia quis vel eros donec.
    
Elementum nisi quis eleifend quam adipiscing vitae proin. Posuere morbi leo urna molestie at elementum eu facilisis sed. Hendrerit dolor magna eget est lorem ipsum dolor sit amet. Eu consequat ac felis donec et. Feugiat vivamus at augue eget arcu dictum varius. Nulla aliquet porttitor lacus luctus accumsan. Porta nibh venenatis cras sed. Nam at lectus urna duis convallis convallis tellus. Sed adipiscing diam donec adipiscing tristique risus nec feugiat in. Ut etiam sit amet nisl. Congue quisque egestas diam in arcu cursus euismod quis viverra.
    
Sit amet massa vitae tortor condimentum. Dignissim diam quis enim lobortis scelerisque fermentum dui faucibus. Augue neque gravida in fermentum et sollicitudin ac orci phasellus. Quam viverra orci sagittis eu volutpat odio facilisis mauris. Platea dictumst vestibulum rhoncus est pellentesque. Vitae semper quis lectus nulla at volutpat. Pretium viverra suspendisse potenti nullam ac tortor vitae. Faucibus interdum posuere lorem ipsum dolor sit amet. Mi quis hendrerit dolor magna eget est. Vitae et leo duis ut diam quam. Lectus magna fringilla urna porttitor rhoncus dolor purus. Massa enim nec dui nunc mattis enim. Sed elementum tempus egestas sed sed. Adipiscing elit ut aliquam purus sit amet luctus venenatis. Mauris in aliquam sem fringilla ut morbi. Nulla posuere sollicitudin aliquam ultrices sagittis orci a scelerisque purus. Dapibus ultrices in iaculis nunc sed. Nisl pretium fusce id velit. Elementum eu facilisis sed odio morbi quis commodo. Porttitor massa id neque aliquam vestibulum.
    
Aliquam vestibulum morbi blandit cursus risus at ultrices. Amet nisl suscipit adipiscing bibendum est ultricies integer quis auctor. Sagittis nisl rhoncus mattis rhoncus urna neque viverra justo nec. Felis donec et odio pellentesque diam volutpat. Mauris a diam maecenas sed enim ut. Mauris pellentesque pulvinar pellentesque habitant. Purus semper eget duis at. Semper auctor neque vitae tempus. Ullamcorper sit amet risus nullam eget. Ut morbi tincidunt augue interdum velit euismod in.
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
