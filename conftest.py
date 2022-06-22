from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest


@pytest.fixture(autouse=True)
def driver_init():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("http://google.com/")
    pytest.webdriver = driver
    yield
    driver.quit()
    del pytest.webdriver
