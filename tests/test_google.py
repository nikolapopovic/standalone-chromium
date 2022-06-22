import pytest


def test_google():
    assert "Googleeee" in pytest.webdriver.title
