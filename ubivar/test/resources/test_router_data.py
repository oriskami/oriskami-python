import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_router_data_update(self):
        response = ubivar.RouterData.update("0", is_active="true")
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertEqual(response.data[0].is_active, "true")
        response = ubivar.RouterData.update("0", is_active="false")
        self.assertEqual(response.data[0].is_active, "false")

    def test_router_data_list(self):
        response = ubivar.RouterData.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(len(response.data), 1)
        self.assertTrue(hasattr(response.data[0], "is_active"))
