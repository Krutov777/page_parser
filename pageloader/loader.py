"""Module with requests."""
import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import Bar  # type: ignore

from pageloader.storage import ContentStorage
from pageloader.url import UrlConverter


class LoaderError(Exception):
    """Base class for exceptions in this module."""
    pass


class PageLoader():
    """Page loader."""
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)

    def _recieve_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as recieve_err:
            self.logger.error(
                'Recieve resourece{url} error: {error}'.format(
                    url=self.url,
                    error=recieve_err
                    ))
            raise LoaderError() from recieve_err
        return response.content

    def _need_to_be_downloaded(self, link):
        """Check needable downloaded resource."""
        if link is None:
            return False
        return link.startswith('/') and os.path.splitext(link)[-1] != ''

    def _get_resource_links(self, page_content, resource_dir_name):
        """Find resource links."""
        soup = BeautifulSoup(page_content, 'html.parser')

        links = {}
        tag_url_attributers = [ # noqa WPS407
            ('script', 'src'),
            ('link', 'href'),
            ('img', 'src'),
        ]
        for tag, attr in tag_url_attributers:
            for node in soup.find_all(tag):
                link = node.get(attr)
                url = UrlConverter(link)
                if self._need_to_be_downloaded(link):
                    resource_path = url.get_resourcename()
                    node[attr] = '{dir}/{path}'.format(
                        dir=resource_dir_name,
                        path=resource_path,
                    )
                    links[link] = resource_path

        return links, str(soup)

    def _save_content(self, content_for_save, output_dir):
        try:
            storage = ContentStorage(content_for_save, output_dir)
            storage.save()
        except OSError as save_err:
            self.logger.error('Save error: {error}'.format(error=save_err))
            raise LoaderError() from save_err

    def _create_resources_directory(
        self,
        content_for_save,
        path_to_resource_dir
            ):
        try:
            storage = ContentStorage(content_for_save, path_to_resource_dir)
            storage.create_dir()
        except OSError as create_dir_err:
            self.logger.error(
                'Create resource dir error: {err}'.format(
                    err=create_dir_err,
                ),
            )
            raise LoaderError() from create_dir_err

    def _download_resources(
        self,
        links,
        path_to_resources_dir,
        on_progress=lambda: None
    ):
        for link, name_for_save in links.items():
            full_path = urljoin(self.url, link)
            self.url = full_path
            file_content = self._recieve_content()
            path_to_file = os.path.join(path_to_resources_dir, name_for_save)
            self._save_content(file_content, path_to_file)
            on_progress()

    def load(self):
        """Save page with resources from url."""
        self.logger.info('Recieving page content')
        page_content = self._recieve_content()
        url = UrlConverter(self.url)
        resource_dir_name = url.get_dirname()
        self.logger.debug('Start search resources on page')
        links, content_for_save = self._get_resource_links(
            page_content,
            resource_dir_name
            )
        with Bar('Progress', max=len(links) + 2) as progress:
            self.logger.debug('Saving page')
            file_name = url.get_filename()
            path_to_save_file = os.path.join(self.output_dir, file_name)
            self._save_content(content_for_save, path_to_save_file)
            progress.next()

            self.logger.debug('Create resources directory')
            path_to_resources_dir = os.path.join(
                self.output_dir,
                resource_dir_name,
                )
            self._create_resources_directory(
                page_content,
                path_to_resources_dir
                )
            progress.next()

            self.logger.debug('Saving resources')
            self._download_resources(
                links,
                path_to_resources_dir,
                on_progress=progress.next,
            )
