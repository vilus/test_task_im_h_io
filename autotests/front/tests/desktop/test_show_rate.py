# -*- coding: utf-8 -*-
import pytest

from pages.recoomend_popup.main import RatingPopup


pytestmark = pytest.mark.case_id('2.')


@pytest.mark.case_id('2.1.1.')
def test_prevent_show_by_cookie(selenium, page_url):
    selenium.implicitly_wait(1)
    for _ in range(10):
        popup = RatingPopup(selenium, page_url).open_with_show(set_cookie=True)
        assert not popup.is_present(), "Popup prevent by cookie, should not be present"


@pytest.mark.case_id('2.2.1.')
def test_exactly_show(selenium, page_url):
    for _ in range(10):
        popup = RatingPopup(selenium, page_url).open_with_show()
        assert popup.is_displayed(), "Should be displayed, show rate is 100%, without cookie"
