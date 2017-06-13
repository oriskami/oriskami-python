import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_router_retrieve(self):
        response = ubivar.Router.retrieve("0")

        self.assertTrue(hasattr(response.data, "__iter__"))

        router = response.data[0]
        self.assertTrue(hasattr(router, "parameters"))
        self.assertTrue(hasattr(router, "data"))
        self.assertTrue(hasattr(router, "flows"))
        self.assertTrue(hasattr(router, "test"))

