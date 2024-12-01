from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD


def admin_login(driver):
    driver.get(f"{BASE_URL}/admin/login/")
    driver.find_element(By.NAME, 'username').send_keys(ADMIN_USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(ADMIN_PASSWORD)
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()


def log_in(driver, username, password):
    """Log in with username and password."""
    try:
        driver.get(f"{BASE_URL}/accounts/login/?next=/")
        username_field = driver.find_element(By.XPATH, '//td//input[@name="username"]')
        password_field = driver.find_element(By.XPATH, '//td//input[@name="password"]')
        login_button = driver.find_element(By.XPATH, '//form//button[@type="submit"]')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 10).until(EC.url_to_be(f"{BASE_URL}{reverse('renthub:home')}"))

    except Exception as e:
        raise RuntimeError(f"An error occurred during login: {e}")


