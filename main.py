# I will run a selenium test file & let it run as I present:

from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# (run project server)
# Initialize the WebDriver (use the same WebDriver as your project)
driver = webdriver.Chrome()  # Or use the path to your specific WebDriver

# URL of your application
app_url = "http://localhost:8000"  # Change this to your app's URL


try:
    # Open the application
    driver.get(app_url)
    time.sleep(10)  # Pause for presentation

# (navigate from home ->room type -> a room -> try to rent )

    # Log in (example)
    driver.find_element(By.ID, "username").send_keys("demo_user")
    time.sleep(10)
    driver.find_element(By.ID, "password").send_keys("demo_pass")
    time.sleep(10)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(10)

    # Navigate to another page
    driver.find_element(By.ID, "profile-link").click()
    time.sleep(5)

    # Any additional steps… (after logged in submit a rent submit -> see successful image)
    # Showcase specific features
finally:
    # Close the driver
    driver.quit()
