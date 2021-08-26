import os
import tempfile

import pytest
import requests
import requests_mock

from pageloader.loader import PageLoader, LoaderError

RESOURCE_URL = 'https://test.test/user/test/main-page/'

@pytest.fixture
def simple_page_content():
    with open('tests/fixtures/simple_page.html') as file:
        yield file.read()


@pytest.fixture
def page_with_links_content():
    with open('tests/fixtures/page_with_links.html') as file:
        yield file.read()


def test_save_url(simple_page_content): # noqa WPS210
    with requests_mock.Mocker() as mock:
        mock.get(RESOURCE_URL, text=simple_page_content)

        with tempfile.TemporaryDirectory() as tmpdirname:
            pageloader = PageLoader(RESOURCE_URL, tmpdirname)
            pageloader.load()
            assert len(os.listdir(tmpdirname)) != 0

            files_path = [
                os.path.join(tmpdirname, file_name)
                for file_name in os.listdir(tmpdirname)
            ]
            file_path, = list(filter(os.path.isfile, files_path))

            with open(file_path, 'r') as file_descriptor:
                file_content = file_descriptor.read()
                assert file_content == simple_page_content


def test_save_url_with_recieve_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(LoaderError):
            pageloader = PageLoader(RESOURCE_URL, tmpdirname)
            pageloader.load()


def test_save_url_with_tmpdir_err(simple_page_content):
    with requests_mock.Mocker() as mock:
        mock.get(RESOURCE_URL, text=simple_page_content)
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(LoaderError):
                fake_dir = '{tmpdir}_fake_34213'.format(tmpdir=tmpdirname)
                pageloader = PageLoader(RESOURCE_URL, fake_dir)
                pageloader.load()


EXPECTED_LINKS = { # noqa WPS407
    '/assets/js/main.js': 'assets-js-main.js',
    '/css/styles.css': 'css-styles.css',
    '/image.png': 'image.png',
}


def test_get_resource_links(page_with_links_content):
    resource_dir_name = 'test-resource-dir_files'
    pageloader = PageLoader('url', 'output_dir')
    links, replace_content = pageloader._get_resource_links(
        page_with_links_content, resource_dir_name,
    )

    assert EXPECTED_LINKS == links
    for path in links.values():
        expected_link = os.path.join(resource_dir_name, path)
        assert expected_link in replace_content


@pytest.mark.parametrize(
    'link,expected',
    [
        ('/assets/main.js', True),
        ('/assets/styles.css', True),
        ('/static/logo.png', True),
        ('https://cdn2.domain.io/dist.js', False),
        ('/user/info', False),
        ('', False),
        (' ', False),
    ],
)
def test_need_to_be_downloaded(link, expected):
    pageloader = PageLoader('link', 'sadsadsad')
    result = pageloader._need_to_be_downloaded(link)
    assert result == expected
