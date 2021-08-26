import os
import re
from urllib.parse import urlparse


class UrlConverter:
    """Class for URL-converting ."""
    def __init__(self, url):
        self.url = url

    def _create_path(self):
        """Create path from url path."""
        parsed_url = urlparse(self.url)
        netloc = parsed_url.netloc.strip('/')
        path = parsed_url.path.strip('/')
        path_to = os.path.join(netloc, path)
        return re.sub(r'[^a-zA-Z^а-яА-Я0-9]', '-', path_to)

    def get_filename(self):
        """Get file name from url.(html)"""
        return '{name}.html'.format(name=self._create_path())

    def get_dirname(self):
        """Get resource dir name from url."""
        path = self._create_path()
        return '{name}_files'.format(name=path)

    def get_resourcename(self):
        """Get resource file name from url.(Any extension)"""
        path, ext = os.path.splitext(self.url)
        self.url = path
        return '{name}{ext}'.format(name=self._create_path(), ext=ext)
