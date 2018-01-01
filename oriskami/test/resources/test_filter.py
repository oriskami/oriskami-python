import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_filters_list(self):
        response = oriskami.Filters.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filters")

    def test_filters_update(self):
        response = oriskami.Filters.update("0", is_active="false")
        self.assertEqual(response.data[0]["is_active"], "false")
        self.assertEqual(response.object, "filters")

        response = oriskami.Filters.update("0", is_active="true")
        self.assertEqual(response.data[0]["is_active"], "true")
        self.assertEqual(response.object, "filters")
