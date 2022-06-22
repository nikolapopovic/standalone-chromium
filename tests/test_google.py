import pytest


def test_google():
    assert "Google" in pytest.webdriver.title
