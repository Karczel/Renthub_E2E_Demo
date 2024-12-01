import time
from browser import Browser

# (run project server in CMD)

# Initialize the WebDriver
driver = Browser.get_browser()

# 1. Go the website (http://localhost:8000/)

# URL of your application
app_url = "http://localhost:8000"  # Change this to your app's URL


try:
    # Open the application
    driver.get(app_url)
    time.sleep(10)  # Pause for presentation

    # 2. Click a room type

    # 3. Click a room

    # 4. Rent

    # 5. Sign up

    # 6. Submit payment

    # 7. See My Rentals

finally:
    # Close the driver
    driver.quit()
