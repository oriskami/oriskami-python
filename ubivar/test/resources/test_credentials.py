import os
import ubivar
import warnings
import unittest
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase, unittest.TestCase):

    def test_api_key(self):
        response = ubivar.Event.list()
        self.assertTrue(hasattr(response, "data"))

    def test_api_key_invalid(self):
        good_api_key = ubivar.api_key  
        ubivar.api_key = "invalid_api_key_string"
        self.assertRaises(ubivar.error.APIError, ubivar.Event.list)
        ubivar.api_key = good_api_key

    def test_api_unauthorized_resource(self):
        good_api_key = ubivar.api_key  
        ubivar.api_key = os.environ.get('UBIVAR_TEST_TOKEN_PYTHON_2')
        self.assertRaises(ubivar.error.APIError, ubivar.FilterWhitelist.list)
        ubivar.api_key = good_api_key

    def test_api_unauthorized_action(self):
        good_api_key = ubivar.api_key  
        ubivar.api_key = os.environ.get('UBIVAR_TEST_TOKEN_PYTHON_2')
        self.assertRaises(ubivar.error.APIError, ubivar.Event.delete, "1")
        ubivar.api_key = good_api_key

    def test_api_unauthorized_ip(self):
        good_api_key = ubivar.api_key  
        ubivar.api_key = os.environ.get('UBIVAR_TEST_TOKEN_PYTHON_3')
        self.assertRaises(ubivar.error.APIError, ubivar.Event.list)
        ubivar.api_key = good_api_key
