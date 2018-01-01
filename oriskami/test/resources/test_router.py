import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_router_retrieve(self):
        response = oriskami.Router.retrieve("0")

        self.assertTrue(hasattr(response.data, "__iter__"))

        router = response.data[0]
        self.assertTrue(hasattr(router, "parameters"))
        self.assertTrue(hasattr(router, "data"))
        self.assertTrue(hasattr(router, "flows"))
        self.assertTrue(hasattr(router, "test"))

