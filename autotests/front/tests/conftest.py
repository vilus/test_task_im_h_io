# -*- coding: utf-8 -*-
import pytest


def pytest_addoption(parser):
    parser.addoption('--wait-timeout', default=10, help='TODO')
    parser.addoption('--page-url', default='http://127.0.0.1:58001', help='TODO')
    parser.addoption("--case-id", action="store", default='all', help="only run tests matching the case id from doc")


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


# TODO: show case_id in report
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("failures") else "w"
#         with open("failures", mode) as f:
#             # let's also access a fixture for the fun of it
#             if "tmpdir" in item.fixturenames:
#                 extra = " (%s)" % item.funcargs["tmpdir"]
#             else:
#                 extra = ""
#
#             f.write(rep.nodeid + extra + "\n")
