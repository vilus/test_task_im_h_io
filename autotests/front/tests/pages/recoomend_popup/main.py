# -*- coding: utf-8 -*-
from pypom import Page  # , Region
from selenium.webdriver.common.by import By


class RatingPopup(Page):
    container = (By.XPATH, '//div[@class="NPS"]')

    def is_displayed(self):
        return self.is_element_displayed(*self.container)

    def is_present(self):
        return self.is_element_present(*self.container)

    def set_prevent_cookie(self):
        # TODO: via driver method
        self.driver.execute_script('document.cookie = "NPS_sended=1; expires = Thu, 01 Jan 2030 00:00:00 GMT; path=/;"')

    def unset_prevent_cookie(self):
        # TODO: via driver method
        self.driver.execute_script('document.cookie = "NPS_sended=; expires = Thu, 01 Jan 1970 00:00:00 GMT; path=/;"')

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
