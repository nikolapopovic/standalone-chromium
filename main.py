from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
