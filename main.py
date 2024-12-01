import subprocess
import sys
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import Browser
from common_steps import admin_login
from port import kill_port
from server import start_django_server, stop_django_server
from settings import BASE_URL
from temp_data import generate_unique_username, generate_email_from_username, generate_secure_password, \
    generate_random_number_string, generate_random_string, generate_unique_thaicitizenshipid, create_temp_image_file, \
    del_temp_image_file


def go_website():
    driver.get(BASE_URL)
    time.sleep(5)  # Pause for presentation


def choose_room_type():
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#carouselExample .carousel-item.active .button-wrapper a"))
    )
    ActionChains(driver).move_to_element(button).perform()
    button.click()
    time.sleep(3)
    try:
        alert_message = driver.find_element(By.XPATH, "//p[contains(text(), 'No rooms available of this type')]")
        time.sleep(3)
        if alert_message.is_displayed():
            driver.back()
            time.sleep(1)

            driver.execute_script(
                "$('#carouselExample').carousel('next');"
            )
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#carouselExample .carousel-item.active .button-wrapper a"))
            )
            ActionChains(driver).move_to_element(button).perform()
            next_button.click()
            time.sleep(3)
    except:
        pass


def choose_room():
    view_details_button = driver.find_element(By.CSS_SELECTOR, ".custom-card .btn.btn-primary")
    view_details_button.click()
    time.sleep(3)


def rent():
    proceed_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-bs-target='#exampleModalLong']")))
    ActionChains(driver).move_to_element(proceed_button).perform()
    time.sleep(3)
    proceed_button.click()
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "agreeTerms")))
    ActionChains(driver).move_to_element(checkbox).perform()
    time.sleep(2)
    checkbox.click()
    confirm_button = driver.find_element(By.ID, "confirmAgreement")
    time.sleep(2)
    confirm_button.click()
    time.sleep(2)


def sign_up(username, email, password, phone_number, first_name, last_name, thai_citizenship_id, temp_image):
    sign_up_link = driver.find_element(By.LINK_TEXT, "Sign-up")
    sign_up_link.click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'signupForm')))
    driver.find_element(By.ID, 'id_username').send_keys(username)
    driver.find_element(By.ID, 'id_email').send_keys(email)
    driver.find_element(By.ID, 'id_first_name').send_keys(first_name)
    driver.find_element(By.ID, 'id_last_name').send_keys(last_name)
    driver.find_element(By.ID, 'id_phone_number').send_keys(phone_number)
    driver.find_element(By.ID, 'id_password1').send_keys(password)
    driver.find_element(By.ID, 'id_password2').send_keys(password)

    for i in range(13):
        num_block = driver.find_element(By.ID, f'id_thai_citizenship_id_{i}')
        ActionChains(driver).move_to_element(num_block).perform()
        num_block.send_keys(thai_citizenship_id[i])

    image = driver.find_element(By.ID, 'id_thai_citizenship_id_image')
    ActionChains(driver).move_to_element(image).perform()
    image.send_keys(temp_image)

    sign_up_button = driver.find_element(By.XPATH, "//button[text()='Sign Up']")
    ActionChains(driver).move_to_element(sign_up_button).perform()
    sign_up_button.click()
    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.alert_is_present())  # Wait for the alert
    alert = Alert(driver)  # Switch to the alert
    alert.accept()
    time.sleep(3)

    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(3)


if __name__ == "__main__":
    # go to this project directory and run:
    # python3 main.py

    try:
        # -r requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        # kill port if any
        kill_port()

        # Assume you already cloned Renthub-Connect Project
        server_process = start_django_server()

        # Initialize the WebDriver
        driver = Browser.get_browser()

        # Get data from admin
        admin_login(driver)
        driver.get(f"{BASE_URL}/admin/renthub/rental")

        usernames_elements = driver.find_elements(By.CSS_SELECTOR, ".username-class")  # Replace with actual selector
        citizenship_ids_elements = driver.find_elements(By.CSS_SELECTOR,
                                                        ".citizenship-id-class")  # Replace with actual selector
        usernames = [username.text for username in usernames_elements]
        thai_citizenship_ids = [citizenship_id.text for citizenship_id in citizenship_ids_elements]

        # Prepare info
        username = generate_unique_username(usernames)
        email = generate_email_from_username(username)
        password = generate_secure_password()
        phone_number = generate_random_number_string(10)
        first_name = generate_random_string(5)
        last_name = generate_random_string(5)
        thai_citizenship_id = generate_unique_thaicitizenshipid(thai_citizenship_ids)
        temp_image = create_temp_image_file()

        logout_button = driver.find_element(By.CSS_SELECTOR, "form#logout-form button[type='submit']")
        logout_button.click()

        # 1. Go the website (http://localhost:8000/)
        go_website()

        # 2. Click a room type
        choose_room_type()

        # 3. Click a room
        choose_room()

        # 4. Rent
        rent()

        # 5. Sign up
        sign_up(username, email, password, phone_number, first_name, last_name, thai_citizenship_id, temp_image)

        # go back to rent
        choose_room_type()
        choose_room()
        rent()

        # 6. Submit payment
        file_input = driver.find_element(By.ID, 'myFile')
        file_input.send_keys(temp_image)  # Provide the path to the image

        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'send-button')))
        ActionChains(driver).move_to_element(send_button).perform()
        time.sleep(3)

        send_button.click()

        time.sleep(3)

        # 7. See My Rentals
        my_rentals_link = driver.find_element(By.XPATH, "//a[@href='/payment/']")
        my_rentals_link.click()
        time.sleep(3)

    finally:
        # clean_up
        admin_login(driver)
        driver.get(f"{BASE_URL}/admin/renthub/renter")
        time.sleep(1)
        rows = driver.find_elements(By.CSS_SELECTOR, 'tr')
        target_row = None
        for row in rows:
            if username in row.text:
                target_row = row
                break
        if target_row:
            checkbox = target_row.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
            checkbox.click()
            action_dropdown = driver.find_element(By.NAME, 'action')
            action_dropdown.click()
            action_dropdown.find_element(By.XPATH, '//option[@value="delete_selected"]').click()
            go_button = driver.find_element(By.NAME, 'index')
            go_button.click()

            confirm_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"][value="Yes, I’m sure"]'))
            )
            confirm_button.click()

        del_temp_image_file(temp_image)

        # Close the driver
        driver.quit()

        stop_django_server(server_process)
        # kill port
        kill_port()
