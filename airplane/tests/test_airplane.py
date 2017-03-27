import os, shutil

from django.conf import settings
from django.template import Context, Template
from django.test import TestCase, override_settings
import six

import airplane
from airplane.templatetags.airplanetags import _convert_url
from mock import patch
from wrench.contexts import temp_directory

# ============================================================================
# Test Objects
# ============================================================================

class FakeRequests(object):
    ok = True
    content = [six.b('pretend content'), ]

    def iter_content(self, **kwargs):
        return iter(self.content)


def fake_get(*args, **kwargs):
    return FakeRequests()


def fake_bad_get(*args, **kwargs):
    r = FakeRequests()
    r.ok = False
    return r


class AirplaneTests(TestCase):
    def setUp(self):
        self.cache1 = '.airplane_cache'
        self.cache1_path = os.path.join(settings.BASE_DIR, self.cache1)
        self.cache2 = '.airplane_cache2'
        self.cache2_path = os.path.join(settings.BASE_DIR, self.cache2)

    def tearDown(self):
        self._remove_local_caches()

    def _remove_local_caches(self):
        if os.path.exists(self.cache1_path):
            shutil.rmtree(self.cache1_path)

        if os.path.exists(self.cache2_path):
            shutil.rmtree(self.cache2_path)

    def _render(self,url, expected):
        # renders a template with our keyword in it
        t = """{% load airplanetags %}{% airplane '""" + url + """' %}"""

        template = Template(t)
        context = Context({})
        result = template.render(context)
        self.assertEqual(expected, result.strip())

    def _check_build_cache(self, url, expected, dir_name):
        # test with a mocked request that works
        with patch('requests.get') as mock_requests:
            mock_requests.side_effect = fake_get

            # render the tag
            self._render(url, expected)

            # check that the directory got a file
            os.path.exists(os.path.join(dir_name, expected))

    def test_airplane(self):
        url = 'http://foo.com'
        expected = '/static/' + _convert_url(url)

        # test pass through, DEBUG=False, no AIRPLANE_MODE set
        self._render(url, url)

        # test pass through, DEBUG=True, no AIRPLANE_MODE set
        with override_settings(DEBUG=True):
            self._render(url, url)

        # test absolute path cache creation and fetching
        with temp_directory() as td:
            with override_settings(
                    DEBUG=True,
                    AIRPLANE_CACHE=td,
                    AIRPLANE_MODE=airplane.BUILD_CACHE):

                # test with a mocked request that works
                self._check_build_cache(url, expected, td)

                # test with a mocked request that fails (404s etc)
                with patch('requests.get') as mock_requests:
                    mock_requests.side_effect = fake_bad_get

                    # render the tag
                    with self.assertRaises(IOError):
                        self._render(url, expected)

        # test cache creation with a local directory that needs creating
        self._remove_local_caches()

        # test with the default cache name
        with override_settings(
                DEBUG=True,
                AIRPLANE_MODE=airplane.BUILD_CACHE):

            self._check_build_cache(url, expected, self.cache1)

            # check that the directory got a file
            os.path.exists(os.path.join(self.cache1, expected))

        # test with a non-default cache name that is local
        with override_settings(
                DEBUG=True,
                AIRPLANE_CACHE=self.cache2,
                AIRPLANE_MODE=airplane.BUILD_CACHE):

            self._check_build_cache(url, expected, self.cache2)

            # check that the directory got a file
            os.path.exists(os.path.join(self.cache1, expected))
