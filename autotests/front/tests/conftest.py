# -*- coding: utf-8 -*-
import base64

import allure
import pytest


def pytest_addoption(parser):
    parser.addoption('--wait-timeout', default=5, help='TODO')
    parser.addoption('--page-url', default='http://127.0.0.1:58001', help='TODO')
    parser.addoption('--case-id', action='store', default='all', help='only run tests matching the case id from doc')


@pytest.fixture
def page_url(request):
    return request.config.getoption('--page-url')


@pytest.fixture
def selenium(selenium, request):
    selenium.set_window_size(1024, 768)  # TODO: via capability (and mb cmdline)
    selenium.implicitly_wait(request.config.getoption('--wait-timeout'))
    return selenium


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "case_id(number): mark test to run only on named environment"
    )


def pytest_runtest_setup(item):
    if item.config.getoption("--case-id") == 'all':
        return

    cases = [mark.args[0] for mark in item.iter_markers(name="case_id")]
    if cases:
        if item.config.getoption("--case-id") not in cases:
            pytest.skip("test requires case_id in {!r}".format(cases))


def pytest_selenium_capture_debug(item, report, extra):
    for log_type in extra:
        if log_type["name"] == "Screenshot":
            content = base64.b64decode(log_type["content"].encode("utf-8"))
            allure.attach(content, f'{item.name}.png', allure.attachment_type.PNG)
