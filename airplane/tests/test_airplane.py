import os, shutil
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.template import Context, Template
from django.test import TestCase, override_settings

import airplane
from airplane.utils import convert_url
from context_temp import temp_directory
from waelstow import capture_stdout

# ============================================================================
# Test Objects
# ============================================================================

class FakeRequests(object):
    ok = True
    content = [b'pretend content', ]

    def iter_content(self, **kwargs):
        return iter(self.content)


def fake_get(*args, **kwargs):
    return FakeRequests()


def fake_bad_get(*args, **kwargs):
    r = FakeRequests()
    r.ok = False
    return r


class AirplaneTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cache1 = '.airplane_cache'
        cls.cache1_path = os.path.join(settings.BASE_DIR, cls.cache1)
        cls.cache2 = '.airplane_cache2'
        cls.cache2_path = os.path.join(settings.BASE_DIR, cls.cache2)
        cls.url = 'http://foo.com'
        cls.expected_filename = convert_url(cls.url)
        cls.expected_url = '/static/' + cls.expected_filename

    def tearDown(self):
        self._remove_local_caches()

    def assertFile(self, dir_name, filename):
        self.assertTrue(os.path.exists(os.path.join(dir_name, filename)))

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

    def _check_build_cache(self, url, expected_url, dir_name, 
            expected_filename):
        # test with a mocked request that works
        with patch('requests.get') as mock_requests:
            mock_requests.side_effect = fake_get

            # render the tag
            self._render(url, expected_url)

            # check that the directory got a file
            self.assertFile(dir_name, expected_filename)

    def test_when_off(self):
        # test pass through, DEBUG=False, no AIRPLANE_MODE set
        self._render(self.url, self.url)

        # test pass through, DEBUG=True, no AIRPLANE_MODE set
        with override_settings(DEBUG=True):
            self._render(self.url, self.url)


    def test_with_abspath(self):
        # test absolute path cache creation and fetching
        with temp_directory() as td:
            with override_settings(
                    DEBUG=True,
                    AIRPLANE_CACHE=td,
                    AIRPLANE_MODE=airplane.BUILD_CACHE):

                # test with a mocked request that works
                self._check_build_cache(self.url, self.expected_url, td, 
                    self.expected_filename)

                # test with a mocked request that fails (404s etc)
                with patch('requests.get') as mock_requests:
                    mock_requests.side_effect = fake_bad_get

                    # render the tag
                    with self.assertRaises(IOError):
                        self._render(self.url, self.expected_url)

    def test_with_localdir(self):
        # test cache creation with a local directory that needs creating
        self._remove_local_caches()

        # test with the default cache name
        with override_settings(
                DEBUG=True,
                AIRPLANE_MODE=airplane.BUILD_CACHE):

            self._check_build_cache(self.url, self.expected_url, 
                self.cache1_path, self.expected_filename)

        # test with a non-default cache name that is local
        with override_settings(
                DEBUG=True,
                AIRPLANE_CACHE=self.cache2,
                AIRPLANE_MODE=airplane.BUILD_CACHE):

            self._check_build_cache(self.url, self.expected_url, 
                self.cache2_path, self.expected_filename)

    def test_auto_mode(self):
        with override_settings(
                DEBUG=True,
                AIRPLANE_MODE=airplane.AUTO_CACHE):

            with patch('requests.get') as mock_requests:
                mock_requests.side_effect = fake_get

                # render the tag, then do it again, request should only be
                # called once (second time is through the cache)
                self._render(self.url, self.expected_url)
                self._render(self.url, self.expected_url)
                self.assertEqual(len(mock_requests.call_args_list), 1)

    def test_schemaless(self):
        with override_settings(
                DEBUG=True,
                AIRPLANE_MODE=airplane.BUILD_CACHE):

            with patch('requests.get') as mock_requests:
                mock_requests.side_effect = fake_get

                # render the tag
                url = '//foo.com'
                expected_filename = convert_url(url)
                expected_url = '/static/' + expected_filename
                self._render(url, expected_url)

                # verify requests was called with the inserted schema
                mock_requests.assert_called_once_with('https:' + url,
                    stream=True)

    def test_commands(self):
        # test aircache command
        with temp_directory() as td:
            with override_settings(
                    DEBUG=True,
                    AIRPLANE_CACHE=td):

                with patch('requests.get') as mock_requests:
                    mock_requests.side_effect = fake_get

                    url = 'http://foo.com/thing'
                    call_command('aircache', url)

                    filename = convert_url(url)

                    # check that the directory got a file
                    self.assertTrue(os.path.exists(os.path.join(td, filename)))

                # run airinfo and make sure it doesn't blow up
                with capture_stdout():
                    with override_settings(AIRPLANE_MODE=airplane.BUILD_CACHE):
                        call_command('airinfo')

                    with override_settings(AIRPLANE_MODE=airplane.USE_CACHE):
                        call_command('airinfo')

                    with override_settings(AIRPLANE_MODE=airplane.AUTO_CACHE):
                        call_command('airinfo')

                    with override_settings(AIRPLANE_MODE=0):
                        call_command('airinfo')
