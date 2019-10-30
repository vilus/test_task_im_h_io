# -*- coding: utf-8 -*-
import allure
import pytest

from selenium.webdriver.common.keys import Keys

from pages.recoomend_popup.main import RatingPopup, make_request_body, EXPECTED_OK_RESPONSE
from libs.helpers import case_id
from libs.ctx_mng import catch_xhr


# TODO: add and skip all other cases from documentation
pytestmark = pytest.mark.case_id('3.')


@case_id('3.1.1.')
def test_default_popup_view(selenium, page_url):
    popup = RatingPopup(selenium, page_url).open_with_show()
    popup.assert_view()


@case_id('3.1.2.')
def test_close_default_popup(selenium, page_url):
    popup = RatingPopup(selenium, page_url).open_with_show()

    with catch_xhr(selenium) as xhr:
        popup.close()

    assert xhr.body is None, 'Unexpected XHR'

    popup.assert_closed()
    popup.assert_present_cookie()


@case_id('3.1.3.')
@pytest.mark.parametrize('grade', ['7', '8', '10'])
def test_positive_choice(grade, selenium, page_url):
    popup = RatingPopup(selenium, page_url).open_with_show()

    with catch_xhr(selenium) as xhr:
        popup.make_choice(grade)

    with allure.step('проверяем обработку запроса'):
        assert xhr.body == make_request_body(grade), 'Unexpected XHR body'
        assert xhr.status == 200, 'Unexpected XHR status code'
        assert xhr.response == EXPECTED_OK_RESPONSE, 'Unexpected XHR response'

    popup.assert_closed()
    popup.assert_present_cookie()


@case_id('3.1.4.')
@pytest.mark.parametrize('grade', ['0', '3', '6'])
def test_negative_choice(grade, selenium, page_url):
    popup = RatingPopup(selenium, page_url).open_with_show()

    with catch_xhr(selenium) as xhr:
        popup.make_choice(grade)

    assert xhr.body is None, 'Unexpected XHR'

    popup.assert_feedback_title_displayed()
    # TODO: add `popup.assert_not_displayed_choice`


@pytest.mark.skip(reason='Not Implemented yet')
@case_id('3.2.3.1.')
def test_send_empty_feedback(selenium, page_url):
    raise NotImplementedError


@case_id('3.2.3.2.')
def test_send_feedback(selenium, page_url):
    grade = '0'
    feedback = 'Hello World!11'

    popup = RatingPopup(selenium, page_url).open_with_show()
    popup.make_choice(grade)

    popup.types_to_feedback(feedback)
    popup.types_to_feedback(Keys.BACKSPACE*2)

    with catch_xhr(selenium) as xhr:
        popup.send()

    with allure.step('проверяем обработку запроса'):
        assert xhr.body == make_request_body(grade, feedback[:-2]), 'Unexpected XHR body'
        assert xhr.status == 200, 'Unexpected XHR status code'
        assert xhr.response == EXPECTED_OK_RESPONSE, 'Unexpected XHR response'

    popup.assert_closed()
    popup.assert_present_cookie()
