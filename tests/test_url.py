# -*- coding:utf-8 -*-

import pytest

from pageloader.url import UrlConverter


def test_to_filename():
    expected = 'hexlet-io-courses.html'
    url = UrlConverter('https://hexlet.io/courses')
    result = url.get_filename()
    assert expected == result


def test_to_resource_dirname():
    expected = 'hexlet-io-courses_files'
    url = UrlConverter('https://hexlet.io/courses')
    result = url.get_dirname()
    assert expected == result


def test_to_resource():
    expected = 'assets-application.css'
    url = UrlConverter('/assets/application.css')
    result = url.get_resourcename()
    assert expected == result
