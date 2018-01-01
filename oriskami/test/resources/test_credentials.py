import os
import oriskami
import warnings
import unittest
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase, unittest.TestCase):

    def test_api_key(self):
        response = oriskami.Event.list()
        self.assertTrue(hasattr(response, "data"))

    def test_api_key_invalid(self):
        good_api_key = oriskami.api_key  
        oriskami.api_key = "invalid_api_key_string"
        self.assertRaises(oriskami.error.APIError, oriskami.Event.list)
        oriskami.api_key = good_api_key

    def test_api_unauthorized_resource(self):
        good_api_key = oriskami.api_key  
        oriskami.api_key = os.environ.get('ORISKAMI_TEST_TOKEN_PYTHON_2')
        self.assertRaises(oriskami.error.APIError, oriskami.FilterWhitelist.list)
        oriskami.api_key = good_api_key

    def test_api_unauthorized_action(self):
        good_api_key = oriskami.api_key  
        oriskami.api_key = os.environ.get('ORISKAMI_TEST_TOKEN_PYTHON_2')
        self.assertRaises(oriskami.error.APIError, oriskami.Event.delete, "1")
        oriskami.api_key = good_api_key

    def test_api_unauthorized_ip(self):
        good_api_key = oriskami.api_key  
        oriskami.api_key = os.environ.get('ORISKAMI_TEST_TOKEN_PYTHON_3')
        self.assertRaises(oriskami.error.APIError, oriskami.Event.list)
        oriskami.api_key = good_api_key
