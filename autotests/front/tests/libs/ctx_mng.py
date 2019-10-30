# -*- coding: utf-8 -*-
import json
import time

from contextlib import contextmanager

import allure


class XHRState(object):
    def __init__(self, body=None, state=None):
        self._body = body
        self.state = state

    @property
    def body(self):
        try:
            return json.loads(self._body)
        except TypeError:
            return

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def status(self):
        if self.state is None:
            return
        return self.state.get('status')

    @property
    def response(self):
        if self.state is None:
            return

        res = self.state.get('response')
        if res is None:
            return

        return json.loads(res)


@allure.step('ловим ajax')
@contextmanager
def catch_xhr(driver):
    # temporary solution

    script = '''
window._xhr_body = undefined;
(function(xhr) {
    var send = xhr.send;
    xhr.send = function() {
        var rsc = this.onreadystatechange;
        this.onreadystatechange = function() {
                window._xhr_state = arguments[0];  // todo: as array
                return rsc.apply(this, arguments);
        };
        window._xhr_body = arguments[0];  // todo: as array
        return send.apply(this, arguments);
    };
})(XMLHttpRequest.prototype);
    '''
    driver.execute_script(script)

    res = XHRState()

    try:
        yield res
    finally:
        res.body = wait_until(lambda: driver.execute_script('return window._xhr_body;'))

        get_xhr_state = '''
        if ( window._xhr_state !==  undefined ) {
            var curr_target = window._xhr_state["currentTarget"]  // todo: check for key_error
            if ( curr_target['readyState'] === curr_target['DONE'] ) {
                return window._xhr_state["currentTarget"]
            }
        }
        '''
        res.state = wait_until(lambda: driver.execute_script(get_xhr_state))


def wait_until(func, timeout=2, period=1):
    # TODO: as contextmanager
    deadline = time.time() + timeout
    while time.time() < deadline:
        res = func()
        if res:
            return res
        time.sleep(period)
    return False
