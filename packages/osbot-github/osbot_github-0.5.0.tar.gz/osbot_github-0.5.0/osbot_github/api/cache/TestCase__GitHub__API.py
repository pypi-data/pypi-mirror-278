from unittest import TestCase

from dotenv import load_dotenv

from osbot_github.api.cache.GitHub__API__Cache import GitHub__API__Cache


class TestCase__GitHub__API(TestCase):
    cache : GitHub__API__Cache

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.cache = GitHub__API__Cache().patch_apply()

    @classmethod
    def tearDownClass(cls):
        cls.cache.patch_restore()