import os
import pathlib

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pytest
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(autouse=True)
def driver_init():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--window-position=0,0")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException:
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get("http://google.com/")
    pytest.webdriver = driver
    yield
    driver.quit()
    del pytest.webdriver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Pytest hook for taking a screenshot if the test fails/xfails."""

    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = f"{report.nodeid.replace('::', '_').rsplit('/', 1)[-1]}.png"
            destination_file = os.path.join(report_directory, file_name)
            pytest.webdriver.save_screenshot(destination_file)
            html = (
                f'<div><img src="{file_name}" alt="{report.nodeid}" style="width:600px;height=400px" '
                f'onclick="window.open(this.src)" align="right"/></div> '
            )
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Pytest hook to automatically include html-reports argument to pytest command when running the tests
    and to create reports directory under ui_tests if directory does not already exist."""

    root_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.exists(f"{root_dir}/reports"):
        os.makedirs(f"{root_dir}/reports")
    config.option.htmlpath = f"{root_dir}/reports/report.html"
