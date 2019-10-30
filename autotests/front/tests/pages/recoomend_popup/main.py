# -*- coding: utf-8 -*-
import allure

from pypom import Page  # , Region
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WAIT_TIMEOUT = 5  # TODO: move to common place
EXPECTED_OK_RESPONSE = {'status': 'ok'}


def make_request_body(user_action, feedback=None):
    res = {'user_action': user_action}
    if feedback is not None:
        res['feedback'] = feedback
    return res


class RatingPopup(Page):
    container = (By.XPATH, '//div[@class="NPS"]')
    cross = (By.XPATH, '//div[@class="NPS__close"]')
    default_msg = (By.XPATH, '//div[@class="NPS__message"]')
    not_like_title = (By.XPATH, '//div[@class="NPS__not-like-title"]')
    like_title = (By.XPATH, '//div[@class="NPS__like-title"]')
    grade_buttons = (By.XPATH, '//div[@class="NPS__buttons"]//div[contains(@class, "NPS__button n")]')
    grade_button_tmpl = (By.XPATH, '//div[@class="NPS__buttons"]//div[contains(@class, "NPS__button n") and text()={}]')
    feedback_title = (By.XPATH, '//div[@class="NPS__feedback-title"]')
    feedback_textarea = (By.XPATH, '//textarea[@class="NPS__feedback-textarea"]')
    send_btn = (By.XPATH, '//button[@class="NPS__feedback-send"]')

    cookie_name = 'NPS_sended'

    @allure.step('всплывающее окно показано?')
    def is_displayed(self):
        return self.is_element_displayed(*self.container)

    @allure.step('устанавливаем куку, запрещающую показ всплывающего окна')
    def set_prevent_cookie(self):
        # TODO: via driver method
        self.driver.execute_script('document.cookie = "NPS_sended=1; expires = Thu, 01 Jan 2030 00:00:00 GMT; path=/;"')

    @allure.step('удаляем куку, запрещающую показ всплывающего окна')
    def unset_prevent_cookie(self):
        # TODO: via driver method
        self.driver.execute_script('document.cookie = "NPS_sended=; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/;"')

    @allure.step('открываем страницу с показом всплывающего окна (в зависимости от куки)')
    def open_with_show(self, set_cookie=False):
        self.open()

        if set_cookie:
            self.set_prevent_cookie()
        else:
            self.unset_prevent_cookie()

        self.driver.execute_script('''
            win = open('/');
            win.Math.random = function() {return 0;};
            win.focus();
        ''')

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self

    @allure.step('закрываем всплывающее окно')
    def close(self):
        self.find_element(*self.cross).click()

    @allure.step('получаем кнопку с оценкой')
    def get_button_by_text(self, grade):
        return self.find_element(self.grade_button_tmpl[0], self.grade_button_tmpl[1].format(grade))

    @allure.step('выбираем оценку')
    def make_choice(self, grade):
        btn = self.get_button_by_text(grade)
        btn.click()

    @allure.step('проверям, что всплывающее окно не отображается')
    def assert_closed(self):
        wait = WebDriverWait(self.driver, WAIT_TIMEOUT)
        try:
            wait.until(EC.invisibility_of_element(self.container))
        except TimeoutException:
            raise AssertionError('popup was not closed')

    @allure.step('проверяем отображение кнопок с оценками')
    def assert_displayed_choice_buttons(self):
        assert EC.visibility_of_all_elements_located(self.grade_buttons)(self.driver), 'grade buttons is not displayed'
        # TODO: add checking buttons label (0-10)

    @allure.step('проверям видимость элементов окна опросника')
    def assert_displayed_choice(self):
        # TODO: customize wait timeout
        assert self.is_element_displayed(*self.cross), 'close button is not displayed'
        assert self.is_element_displayed(*self.default_msg), 'message is not displayed'
        assert self.is_element_displayed(*self.like_title), 'likely label is not displayed'
        assert self.is_element_displayed(*self.not_like_title), 'not likely label is not displayed'
        self.assert_displayed_choice_buttons()

    def assert_view(self):
        self.assert_displayed_choice()

        likely_txt = 'Extremely likely'
        not_likely_txt = 'Not at all likely'
        msg_txt = 'How likely are you to recommend our website to a friend?'

        # TODO: add wrapper around "element" with helpers like as assert_text
        with allure.step('проверяем текст окна опросника'):
            assert self.find_element(*self.like_title).text == likely_txt
            assert self.find_element(*self.not_like_title).text == not_likely_txt
            assert self.find_element(*self.default_msg).text == msg_txt

    @allure.step('проверяем отображение загаловка окна отзыва')
    def assert_feedback_title_displayed(self):
        assert self.is_element_displayed(*self.feedback_title), 'feedback title is not displayed'

    @allure.step('проверяем куку')
    def assert_present_cookie(self):
        cookie = self.driver.get_cookie(self.cookie_name)
        assert cookie is not None, 'prevent cookie is not present'

        expiry = cookie.get('expiry')
        assert expiry is not None, 'prevent cookie has no expiry'

        # TODO: check expiry is in future (after specified)

    @allure.step('вводим отзыв')
    def types_to_feedback(self, text):
        area = self.find_element(*self.feedback_textarea)
        # need focus?
        area.send_keys(text)

    @allure.step('отправляем отзыв')
    def send(self):
        self.find_element(*self.send_btn).click()
