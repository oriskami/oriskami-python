import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_router_data_update(self):
        response = oriskami.RouterData.update("0", is_active="true")
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertEqual(response.data[0].is_active, "true")
        response = oriskami.RouterData.update("0", is_active="false")
        self.assertEqual(response.data[0].is_active, "false")

    def test_router_data_list(self):
        response = oriskami.RouterData.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(len(response.data), 1)
        self.assertTrue(hasattr(response.data[0], "is_active"))
