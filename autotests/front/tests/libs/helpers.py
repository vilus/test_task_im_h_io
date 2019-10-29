# -*- coding: utf-8 -*-
import allure
import pytest


def case_id(c_id):
    deco2 = pytest.mark.case_id(c_id)
    deco1 = allure.tag(c_id)

    def final_decorator(func):
        return deco2(deco1(func))

    return final_decorator
